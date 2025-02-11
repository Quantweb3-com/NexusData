import datetime

from qwdataapi import auth, fetch_data

auth("quantweb3", "$pbkdf2$131000$U2NvdHQ$rrcEv/zhCQVXN94pWH/tH5FITEQ")

fetch_data(
    tickers=["BTCUSDT"],
    store_dir="./tmp/data",
    start_time=datetime.datetime(2021, 1, 1),
    end_time=datetime.datetime(2022, 1, 2),
    data_type="klines",
    data_frequency="1m",
    asset_class="spot"
)
