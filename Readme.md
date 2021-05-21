# LUNA
Luna is a program consisting of different modules and scripts for binance using python-binance library. However
the modules should work with the right input format which have been documented in their relative folder. 
- [Github repo](https://github.com/DBC201/Luna)
- [demo website](https://bogdanoff.pw)

## Dependencies
- [python-binance](https://github.com/sammchardy/python-binance)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [websocket-client](https://pypi.org/project/websocket-client/)
- [mathplotlib](https://pypi.org/project/matplotlib/) 
  (for graphing trade data, not essential if you won't use [Luna to graph](luna_modules/trade_analysis))

## Installation
- You can use pipenv, if not you can install all dependencies one by one with pip. However if a dependency gets a breaking update,
  program might not work as intended. One can look at [Pipfile.lock](Pipfile.lock) to see latest version specifics.
- Run 'pipenv install' in root folder. This should install the required dependencies.
- In case of time sync error, sync your os time with internet time.
    - Screenshot for windows:
    
    ![windows time sync](./docs/pictures/sync%20internet%20time.png)

## Creators
- [Atilla Turkmen](https://github.com/atillaturkmen)
- [Deniz Cakiroglu](https://github.com/DBC201)
