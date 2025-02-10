import datetime

from qwdataapi import auth, store_data_locally

auth("", "")

store_data_locally(
    tickers=["BTCUSDT"],
    store_dir="./tmp/data",
    start_time=datetime.datetime(2021, 1, 1),
    end_time=datetime.datetime(2022, 1, 2),
    data_type="klines",
    data_frequency="1m",
    asset_class="um")
