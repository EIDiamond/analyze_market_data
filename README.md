## Description
This is an example tool to analyze market data such as candles and trades.

Find your own ideas and test it by using backtesting tool [backtesting/tinkoff_tests_py](https://github.com/EIDiamond/invest-tools/tree/main/backtesting/tinkoff_tests_py) project.

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
- `FROM_DAYS` - count of days for data providers 
- `FIGI` - stock figi for research
- `PROVIDER_NAME` - name of analyze provider to run 
(`RSI_CALCULATION` - is an example, you are free to add your own ideas)

### Section DATA_PROVIDER
- `ROOT_PATH` - path to root folder with downloaded market data by
[data_collectors/tinkoff_stream_py](https://github.com/EIDiamond/invest-tools/tree/main/data_collectors/tinkoff_stream_py) project

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

## Logging
All logs are written in `logs/analyze.log`.
Any kind of settings can be changed in main.py code

## Project change log
[Here](CHANGELOG.md)

## Disclaimer
The author is not responsible for any errors or omissions, or for the trade results obtained from the use of this tool. 
