# QWDataAPI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-1.0.7-green)

QWDataAPI is a powerful cryptocurrency market data fetching tool that provides high-quality historical and alternative
data from [Quantweb3.ai](https://quantweb3.ai/).

## Features ✨

- 🚀 High-performance data retrieval
- 📊 Minute-level candlestick data
- 💫 Support for major exchanges
- 🔄 Asynchronous processing for large datasets
- 📈 Complete market depth information

## Quick Start 🚀

### Installation

``` bash
pip install qwdataapi
```

### Basic Usage

``` python
from qwdataapi import auth, fetch_data
```

1. Authentication (Get credentials at https://quantweb3.ai/subscribe)

``` python
auth('your_username', 'your_token')
```

2. Fetch Data

``` python
df = fetch_data(
symbol='BTCUSDT', # Trading pair
start='2024-01-01 00:00:00' # Start time
)
```

3. View Data

``` python
print(df.head())
```

### Advanced Usage

Fetch data with custom parameters

``` python 
df = fetch_data(
symbol='BTCUSDT', # Trading pair
exchange='binance', # Exchange
asset_type='spot', # Asset type: spot/futures
start='2024-01-01 00:00:00', # Start time
end='2024-01-02 00:00:00', # End time
batch_size=50 # Batch size
)
```

#### Function Parameters 📋

- **exchange** (`str`): The name of the exchange, defaults to `'binance'`.
- **symbol** (`str`): The trading pair, for example `'BTCUSDT'`, defaults to `'BTCUSDT'`.
- **asset_type** (`str`): The type of asset. Defaults to `'spot'` for spot trading. `'coinm'` represents coin-based
  futures trading, while `'usdm'` represents USD-based futures trading.
- **data_type** (`str`): The type of data. Defaults to `'klines'`, which represents candlestick data.
- **start** (`str`): The start time of the data, formatted as `'YYYY-MM-DD HH:MM:SS'`, defaults to
  `'2023-08-01 00:00:00'`.
- **end** (`str`): The end time of the data, formatted the same as the start time, defaults to `'2024-07-17 00:00:00'`.
- **batch_size** (`int`): The size of the data batch for each request, a number between 40 and 100, defaults to 50.

Save data

``` python
df.to_csv('btc_data.csv')
```

## Data Structure 📊

The returned DataFrame contains the following columns:

| Column                 | Description            |
|------------------------|------------------------|
| open_time              | Opening time (index)   |
| open                   | Opening price          |
| high                   | Highest price          |
| low                    | Lowest price           |
| close                  | Closing price          |
| volume                 | Trading volume         |
| close_time             | Closing time           |
| quote_volume           | Quote currency volume  |
| count                  | Number of trades       |
| taker_buy_volume       | Taker buy volume       |
| taker_buy_quote_volume | Taker buy quote volume |

## Authentication 🔑

1. Visit [Quantweb3.ai Subscription Page](https://quantweb3.ai/subscribe)(**Note: New users get a 7-day free trial**)
2. Register and obtain authentication credentials
3. Use the `auth()` function to authenticate

### How to get free data service?

> **Note**: Open an account using one of the above links and provide a screenshot to get **1 year's** of free data service(**Anyone**).

- **Bison Bank**: [Sign up](https://m.bison.com/#/register?invitationCode=1002)
- **OKX**: [Sign up](http://www.okx.com/join/80353297)
- **Bybit**: [Sign up](https://partner.bybit.com/b/90899)
- **ZFX**: [Sign up](https://zfx.link/46dFByp)

## Examples 📝

You can view the demo on Google Colab by
clicking [here](https://colab.research.google.com/drive/1GiC43LmyWGk3S2xCmvLlGzW_1GrMgGyD?usp=sharing).

### Fetch Bitcoin Daily Data and Plot

``` python
import pandas as pd
import matplotlib.pyplot as plt
from qwdataapi import auth, fetch_data
```

Authenticate

``` python 
auth('your_username', 'your_token')
```

Fetch data

``` python 
Fetch data
df = fetch_data(
symbol='BTCUSDT',
start='2024-01-01',
end='2024-01-07'
)
```

Plot price chart

```
plt.figure(figsize=(15, 7))
plt.plot(df.index, df['close'])
plt.title('BTC/USDT Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid(True)
plt.show()
```

## Dependencies 📦

- python-snappy >= 0.7.2
- grpcio >= 1.64.1
- pandas >= 1.5.3
- protobuf >= 4.25.3
- tqdm >= 4.65.0

## FAQ ❓

**Q: How to handle authentication errors?**  
A: Ensure your username and token are correct, and check your network connection.

**Q: What is the data update frequency?**  
A: Hstorical data is updated daily.

## Contributing 🤝

Issues and Pull Requests are welcome!

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contact 📧

- Website: [quantweb3.ai](https://quantweb3.ai)
- Email: quantweb3.ai@gmail.com
- X: https://x.com/quantweb3_ai
- Telegram: https://t.me/+6e2MtXxoibM2Yzlk

## Changelog 📝