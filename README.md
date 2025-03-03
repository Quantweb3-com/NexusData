# NexusData

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-1.0.7-green)

NexusData revolutionizes decentralized market analysis by transforming complex data workflows into a single line of code. Designed for traders and developers, our platform seamlessly aggregates high-fidelity coin spots/contracts bar data from top exchanges like Binance and OKX, delivering:

- **Zero-Learning-Code**: Extract, clean, and structure raw data with one intuitive function
- **Turbocharged Security**: Local data vaulting ensures enterprise-grade protection + sub-millisecond access
- **Future-Proof Scalability:** Modular architecture primed for expanding exchange integrations 
- **Trade smarter:** build faster – where simplicity meets institutional-grade data resilience.

## Quick Start 🚀

### Installation

``` bash
pip install nexusdata
```

### Basic Usage

``` python
from nexusdata import auth, fetch_data
```

1. Authentication (Get credentials at https://quantweb3.ai/subscribe)

``` python
auth('your_username', 'your_token')
```

2. Fetch Data
Store the data in a local specified directory (csv format)
``` python
fetch_data()
```
### Advanced Usage

Fetch data with custom parameters

``` python 
fetch_data(
    tickers=["BTCUSDT"],
    store_dir="./tmp/data",
    start_time=datetime.datetime(2021, 1, 1),
    end_time=datetime.datetime(2022, 1, 2),
    data_type="klines",
    data_frequency="1m",
    asset_class="um"
)
```

#### Function Parameters 📋

- **tickers** (`list[str]`):  
  A list of trading pairs to fetch data for.  
  _Example_: `["BTCUSDT"]`.

- **store_dir** (`str`):  
  The directory path where the fetched data will be stored.  
  _Example_: `"./tmp/data"`.

- **start_time** (`datetime.datetime`):  
  The starting timestamp for the data retrieval.  
  _Example_: `datetime.datetime(2021, 1, 1)`.

- **end_time** (`datetime.datetime`):  
  The ending timestamp for the data retrieval.  
  _Example_: `datetime.datetime(2022, 1, 2)`.

- **data_type** (`str`):  
  The type of data to fetch. Defaults to `"klines"`, which represents candlestick (OHLCV) data.

- **data_frequency** (`str`):  
  The frequency at which the data is sampled.  
  _Example_: `"1m"` for one-minute intervals.

- **asset_class** (`str`):  
  The asset class identifier. For instance, `"um"` might indicate a specific market type.  
  _Note_: The accepted values should be defined by your application context.

## Data Structure 📊

The returned DataFrame contains the following columns:

| Column                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Open time                     | The moment when the candlestick period started.                           |
| Open                          | The opening price for the period.                                          |
| High                          | The highest price reached during the period.                               |
| Low                           | The lowest price reached during the period.                                |
| Close                         | The closing price at the end of the period.                                |
| Volume                        | The total traded quantity during the period.                               |
| Close time                    | The moment when the candlestick period ended.                              |
| Quote asset volume            | The traded volume in terms of the quote asset during the period.           |
| Number of trades              | The total number of trades executed during the period.                     |
| Taker buy base asset volume   | The amount of the base asset bought by takers during the period.             |
| Taker buy quote asset volume  | The amount of the quote asset used for taker buy orders during the period.   |
| Ignore                        | A field reserved for future use and typically disregarded.                 |

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
* You can view the demo on Google Colab by
clicking [here](https://colab.research.google.com/drive/1GiC43LmyWGk3S2xCmvLlGzW_1GrMgGyD?usp=sharing).
* You can also look at the [example](./example) folder in the directory

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
