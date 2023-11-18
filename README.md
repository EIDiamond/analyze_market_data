## Description
This is an example tool to analyze market data such as candles and trades.

Find your own ideas and test it by using backtesting tool [trade_backtesting](https://github.com/EIDiamond/trade_backtesting) project.

Best ideas can be a strategy for trading bot [invest-bot](https://github.com/EIDiamond/invest-bot) project

## Before Start
### Dependencies

- [Tinkoff Invest Python gRPC client](https://github.com/Tinkoff/invest-python)
<!-- termynal -->
```
$ pip install tinkoff-investments
```

- [matplotlib](https://matplotlib.org)
<!-- termynal -->
```
$ pip install -U matplotlib
```

- [pandas](https://pandas.pydata.org)
<!-- termynal -->
```
$ pip install pandas
```

### Run
Recommendation is to use python 3.10. 

Run `main.py`

## Configuration
Configuration can be specified via [settings.ini](settings.ini) file.

### Section ANALYZE
- `FROM_DAYS` - count of days for data providers from NOW (negative number are disable filtration by date) 
- `FIGI` - stock figi for research
- `PROVIDER_NAME` - name of analyze provider to run 
(`RSI_CALCULATION` - is an example, you are free to add your own ideas)

### Section DATA_PROVIDER
- `NAME` - name of data provider:
  - 'TinkoffDownloaded' for market data downloaded by
[tinkoff_market_data_collector](https://github.com/EIDiamond/tinkoff_market_data_collector) project
  - 'TinkoffHistoryData' for market data downloaded from 'https://invest-public-api.tinkoff.ru/history-data'
[More information](https://tinkoff.github.io/investAPI/get_history/)
  - 'TinkoffAPIGetAllCandles' is getting history candles from tinkoff api online. Requires API Token.

### Section DATA_PROVIDER_SETTINGS
- if name is `TinkoffDownloaded`
  - 'ROOT_PATH' - path to root folder with downloaded market data 
- if name is `TinkoffHistoryData`
  - 'ROOT_PATH' - path to root folder with downloaded market data
- if name is `TinkoffAPIGetAllCandles`
  - 'TOKEN' - token for [Тинькофф Инвестиции](https://www.tinkoff.ru/invest/) api.  
  
### Section PROVIDER_NAME (RSI_CALCULATION in example)
- Name of section must be the same as `ANALYZE`.`PROVIDER_NAME`, other section names will be ignored
- All settings in the section will be provided as *args to the init method of provider class 

## How to add a new analyze provider with your own best idea
- Write a new class (or classes) with your idea
- Put (create before) it to specific folder under `analyze` folder 
- The new class must have `IAnalyzeProvider` as super class
- Give a name for the new class for configuration (`PROVIDER_NAME`)
- Extend `AnalyzeProviderFactory` class by the name and return the new class by the name
- Specify new settings in `settings.ini` file. 
  - Put the new class name to `ANALYZE`.`PROVIDER_NAME`
  - Create separate section `PROVIDER_NAME` with args for `__init__` method

Enjoy it. 

## RSI_CALCULATION example
- Just an example how you can develop your own indicator and use it by tool. 

## Use case
1. Download market data using [tinkoff_market_data_collector](https://github.com/EIDiamond/tinkoff_market_data_collector) project
2. Research data and find an idea for trade strategy using [analyze_market_data](https://github.com/EIDiamond/analyze_market_data) project
3. Test and tune your trade strategy using [trade_backtesting](https://github.com/EIDiamond/trade_backtesting) project
4. Trade by [invest-bot](https://github.com/EIDiamond/invest-bot) and your own strategy.
5. Profit!

### Example
Your can find example in code:
- Let's imagine your have great idea to invent your own idicator. Rsi idicator was selected for example.
- RSI Calculation alghoritm has been written for [research tool](https://github.com/EIDiamond/analyze_market_data/blob/main/analyze/rsi_calculation/rsi_calculation_analyze.py)
- It has been tested by [backtesting](https://github.com/EIDiamond/trade_backtesting/blob/main/trade_system/strategies/rsi_example/rsi_strategy.py)
- And now you are able to make your desicion.


## Logging
All logs are written in `logs/analyze.log`.
Any kind of settings can be changed in main.py code

## Project change log
[Here](CHANGELOG.md)

## Disclaimer
The author is not responsible for any errors or omissions, or for the trade results obtained from the use of this tool. 
