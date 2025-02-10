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
import pandas as pd
import snappy
import tqdm
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
    async def fetch_data(cls, exchange='binance', symbol='BTCUSDT', asset_type='spot', data_type='klines',
                         start='2023-08-01 00:00:00', end='2024-07-17 00:00:00', batch_size=50):
        """Fetch market data from the server."""

        def estimate_minutes(start_time, end_time):
            """Estimate the number of minutes between two timestamps."""
            start = pd.Timestamp(start_time)
            end = pd.Timestamp(end_time)
            return int((end - start).total_seconds() / 60) + 24 * 60

        def parse_minu_data(data: MinuDataMessage):
            """Parse a single minute data message into a dictionary."""
            return {
                'open_time': data.open_time,
                'open': data.open,
                'high': data.high,
                'low': data.low,
                'close': data.close,
                'volume': data.volume,
                'close_time': data.close_time,
                'quote_volume': data.quote_volume,
                'count': data.count,
                'taker_buy_volume': data.taker_buy_volume,
                'taker_buy_quote_volume': data.taker_buy_quote_volume,
                'ignore': data.ignore,
            }

        async with grpc.aio.insecure_channel(SERVER_HOST) as channel:
            stub = MarketDataServiceStub(channel)

            try:
                request = FetchDataRequest(
                    exchange=exchange.lower(),
                    symbol=symbol,
                    asset_type=asset_type.lower(),
                    start=start,
                    end=end,
                    auth_token=cls._auth_token,
                    batch_size=batch_size,
                    data_type=data_type,
                )

                total_minutes = estimate_minutes(start, end)
                progress_bar = tqdm.tqdm(total=total_minutes, desc='Fetching data')
                data_list = []

                async for response in stub.FetchData(request):
                    if not response.success:
                        print(f'Error from server: {response.message}')
                        return pd.DataFrame()

                    if not response.data:
                        print("Warning: Received empty data")
                        continue

                    try:
                        decompressed_data = snappy.uncompress(response.data)
                        batch_data = BatchMinuDataMessages()
                        batch_data.ParseFromString(decompressed_data)

                        if batch_data.data:
                            data_list.extend(batch_data.data)
                            progress_bar.update(len(batch_data.data))

                    except snappy.UncompressError as e:
                        print(f"Decompression error: {e}")
                    except Exception as e:
                        print(f"Error processing data: {e}")

                progress_bar.close()

                if not data_list:
                    print("Warning: No data received")
                    return pd.DataFrame()

                data_dict = [parse_minu_data(data) for data in data_list]
                df = pd.DataFrame(data_dict)

                if df.empty:
                    return df

                df = df.set_index('open_time')
                df.index = pd.to_datetime(df.index, unit='s')
                df['close_time'] = pd.to_datetime(df['close_time'], unit='s')
                return df

            except grpc.RpcError as e:
                print(f"gRPC error: {e}")
                return pd.DataFrame()
            except Exception as e:
                print(f"Unknown error: {e}")
                return pd.DataFrame()

    @classmethod
    def store_data_locally(cls,
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


def fetch_data(exchange='binance', symbol='BTCUSDT', asset_type='spot', data_type='klines',
               start='2023-08-01 00:00:00', end='2024-07-17 00:00:00', batch_size=50):
    """Wrapper function to fetch market data."""
    return asyncio.run(
        QWClient.fetch_data(exchange=exchange, symbol=symbol, asset_type=asset_type, data_type=data_type,
                            start=start, end=end, batch_size=batch_size))


def store_data_locally(
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
    return QWClient.store_data_locally(tickers=tickers, start_time=start_time, end_time=end_time,
                                       max_tickers=max_tickers, asset_class=asset_class, data_type=data_type,
                                       data_frequency=data_frequency, store_dir=store_dir)
