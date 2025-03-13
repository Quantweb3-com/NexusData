import datetime

from nexusdata import auth, fetch_data

if __name__ == "__main__":
    auth("golandcxy@gmail.com", "$pbkdf2$131000$U2NvdHQ$SW4ws7mVgnSqZoD0pzNzPLEr8AU")

    fetch_data(
        max_tickers=1,
        store_dir="./tmp/data",
        start_time=datetime.datetime(2025, 3, 1),
        end_time=datetime.datetime(2025, 3, 10),
        data_type="klines",
        data_frequency="1m",
        asset_class="spot",
        platform="binance"
    )
