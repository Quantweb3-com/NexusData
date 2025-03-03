import grpc
import asyncio
import warnings
import ctypes
import os
from ctypes import c_char_p, c_int, POINTER
import datetime
from pathlib import Path
from typing import Literal, Optional, List

warnings.filterwarnings("ignore")
from .proto.qwdata_pb2 import AuthRequest, FetchDataRequest, HelloRequest, MinuDataMessage, BatchMinuDataMessages
from .proto.qwdata_pb2_grpc import MarketDataServiceStub
import nest_asyncio

nest_asyncio.apply()

# Server host configuration
SERVER_HOST = '139.180.130.126:50051'


def get_mac_address():
    """Retrieve the MAC address of the machine."""
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    return ':'.join([mac[i:i + 2] for i in range(0, 12, 2)])


async def anext(aiter):
    """Async iterator next function."""
    return await aiter.__anext__()


class QWClient:
    _auth_token = 'default'
    _instance = None

    @classmethod
    def instance(cls):
        """Singleton pattern to ensure only one instance of the client exists."""
        if cls._instance is None:
            cls._instance = QWClient()
        return cls._instance

    @classmethod
    async def authenticate(cls, user, token):
        """Authenticate the user with the server."""
        async with grpc.aio.insecure_channel(SERVER_HOST) as channel:
            stub = MarketDataServiceStub(channel)
            uuid = get_mac_address()
            response = await stub.Auth(AuthRequest(user=user, token=token, uuid=uuid))
            if response.success:
                print("Authentication successful!")
                cls._auth_token = response.temp_token
            else:
                print(f"Authentication failed: {response.message}")

    @classmethod
    def fetch_data(cls,
                   tickers: Optional[List[str]] = None,
                   start_time: Optional[datetime.datetime] = None,
                   end_time: Optional[datetime.datetime] = None,
                   max_tickers: int = 0,
                   asset_class: Literal["spot", "cm", "um"] = "spot",
                   data_type: str = "klines",
                   data_frequency: Literal["1s", "1m", "3m", "5m", "15m", "30m",
                   "1h", "2h", "4h", "6h", "8h", "12h",
                   "1d", "3d", "1w", "1mo"] = "1m",
                   store_dir: str = "./data"):
        """Save fetched data to the local storage using the authenticated token."""

        # Ensure the client is authenticated before saving data
        if cls._auth_token == 'default':
            raise RuntimeError("Client is not authenticated. Please authenticate first.")

        if data_type not in MAP_DATA_TYPES_BY_ASSET[asset_class]:
            raise ValueError(f"Data type {data_type} is not applicable for asset class {asset_class}")

        current_dir = Path(__file__).parent
        lib_dir = current_dir / "lib"
        if os.name != "nt":
            lib_path = lib_dir / "lib.so"
        else:
            lib_path = lib_dir / "lib.dll"
        lib = ctypes.CDLL(str(lib_path))
        lib.Dump.argtypes = [
            c_char_p,  # assetClass
            c_char_p,  # dataType
            c_char_p,  # dataFrequency
            POINTER(c_char_p),  # tickers
            c_int,  # tickersLen
            c_char_p,  # dateStart
            c_char_p,  # dateEnd
            c_int,  # maxTickers
            c_char_p,  # token
            c_int,  # timestamp
            c_char_p  # storeDir
        ]
        lib.Dump.restype = c_char_p

        def encode_string(s: Optional[str]) -> Optional[bytes]:
            """Encode a string to bytes."""
            return s.encode('utf-8') if s else None

        def to_c_str_array(strings: List[str]) -> POINTER(c_char_p):
            """Convert a list of strings to a C-style array of char pointers."""
            arr = (c_char_p * len(strings))()
            for i, s in enumerate(strings):
                arr[i] = s.encode('utf-8')
            return arr

        tickers_arr = to_c_str_array(tickers) if tickers else (c_char_p * 0)()
        result = lib.Dump(
            encode_string(asset_class),
            encode_string(data_type),
            encode_string(data_frequency),
            tickers_arr,
            len(tickers) if tickers else 0,
            encode_string(start_time.strftime('%Y-%m-%dT%H:%M:%SZ') if start_time else None),
            encode_string(end_time.strftime('%Y-%m-%dT%H:%M:%SZ') if end_time else None),
            max_tickers,
            encode_string(cls._auth_token),  # Use the authenticated token
            int(datetime.datetime.now().timestamp()),
            encode_string(store_dir)
        )
        if result:
            err_msg = ctypes.cast(result, c_char_p).value.decode('utf-8')
            raise RuntimeError(f"Dump operation failed, error: {err_msg}")


MAP_DATA_TYPES_BY_ASSET = {
    "spot": ("aggTrades", "klines", "trades"),
    "cm": (
        "aggTrades",
        "klines",
        "trades",
        "indexPriceKlines",
        "markPriceKlines",
        "premiumIndexKlines",
    ),
    "um": (
        "aggTrades",
        "klines",
        "trades",
        "indexPriceKlines",
        "markPriceKlines",
        "premiumIndexKlines",
        "metrics",
    ),
}


def auth(user, token):
    """Wrapper function to authenticate the user."""
    return asyncio.run(QWClient.authenticate(user, token))


def fetch_data(
        tickers: Optional[List[str]] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        max_tickers: int = 0,
        asset_class: Literal["spot", "cm", "um"] = "spot",
        data_type: str = "klines",
        data_frequency: Literal[
            "1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mo"] = "1m",
        store_dir: str = "./data"
):
    """
    Wrapper function to save data to local using the QWClient.
    """
    return QWClient.fetch_data(tickers=tickers, start_time=start_time, end_time=end_time,
                               max_tickers=max_tickers, asset_class=asset_class, data_type=data_type,
                               data_frequency=data_frequency, store_dir=store_dir)
