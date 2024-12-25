import grpc
import asyncio
import warnings

warnings.filterwarnings("ignore")
from .proto.qwdata_pb2 import AuthRequest, FetchDataRequest, HelloRequest, MinuDataMessage, BatchMinuDataMessages
from .proto.qwdata_pb2_grpc import MarketDataServiceStub
import pandas as pd
import time
import snappy
import tqdm
import nest_asyncio

nest_asyncio.apply()
##pip install python-snappy

# server_host = 'localhost:50051'
server_host = '139.180.130.126:50051'


def get_mac_address():
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    return '%s:%s:%s:%s:%s:%s' % (mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:])


async def anext(aiter):
    return await aiter.__anext__()


class qwClient(object):
    _auth_token = 'default'
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = qwClient()
        return cls._instance

    @classmethod
    async def auth(cls, user, token):

        async with grpc.aio.insecure_channel(server_host) as channel:
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
        def estimate_minutes(start, end):
            start = pd.Timestamp(start)
            end = pd.Timestamp(end)
            # print(f'start: {start}, end: {end}')
            # print(f'end - start: {end - start}.total_seconds() ')
            return (end - start).total_seconds() / 60 + 24 * 60

        def get_minu_data_dict(data: MinuDataMessage):
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

        async with grpc.aio.insecure_channel(server_host) as channel:
            client = MarketDataServiceStub(channel)

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

                total_minutes = int(estimate_minutes(start, end))
                pbar = tqdm.tqdm(total=total_minutes, desc='Fetching data')
                datalist = []

                async for response in client.FetchData(request):
                    if not response.success:
                        print(f'\nError from server: {response.message}')
                        return pd.DataFrame()  # 返回空DataFrame而不是None

                    try:
                        if not response.data:  # 检查数据是否为空
                            print(f"Warning: Received empty data")
                            continue

                        decompressed_data = snappy.uncompress(response.data)
                        bdata = BatchMinuDataMessages()
                        bdata.ParseFromString(decompressed_data)

                        if bdata.data:  # 检查是否有数据
                            datalist.extend(bdata.data)
                            pbar.update(len(bdata.data))

                    except snappy.UncompressError as e:
                        print(f"解压缩错误: {e}")
                        continue
                    except Exception as e:
                        print(f"处理数据时出错: {e}")
                        continue

                pbar.close()

                if not datalist:  # 检查是否获取到任何数据
                    print("Warning: No data received")
                    return pd.DataFrame()

                data_dict = [get_minu_data_dict(data) for data in datalist]
                df = pd.DataFrame(data_dict)

                if df.empty:
                    return df

                df = df.set_index('open_time')
                df.index = pd.to_datetime(df.index, unit='s')
                df['close_time'] = pd.to_datetime(df['close_time'], unit='s')
                return df

            except grpc.RpcError as e:
                print(f'gRPC错误: {e}')
                return pd.DataFrame()
            except Exception as e:
                print(f'未知错误: {e}')
                return pd.DataFrame()


def auth(user, token):
    return asyncio.run(qwClient.auth(user, token))


def fetch_data(exchange='binance', symbol='BTCUSDT', asset_type='spot', data_type='klines', start='2023-08-01 00:00:00',
               end='2024-07-17 00:00:00', batch_size=50):
    return asyncio.run(
        qwClient.fetch_data(exchange=exchange, symbol=symbol, asset_type=asset_type, data_type=data_type, start=start,
                            end=end, batch_size=batch_size))
