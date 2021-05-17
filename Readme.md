# LUNA
[Luna](https://github.com/DBC201/Luna) is a program consisting of different modules and scripts for binance using python-binance library. However
the modules should work with the right input format which have been documented in their relative folder.

## Dependencies
- [python-binance](https://github.com/sammchardy/python-binance)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [websocket-client](https://pypi.org/project/websocket-client/)
- [mathplotlib](https://pypi.org/project/matplotlib/) (for graphing trade data)


- Run 'pipenv install' in root folder. This should install the required dependencies.
- In case of time sync error, sync your os time with internet time.
    - Screenshot for windows:
    ![windows time sync](./docs/pictures/sync%20internet%20time.png)
- At the time of this readme, Ubuntu repositories only have python up to 3.8. However this doesn't pose an issue and
most of the programs seem to work fine. If not one option could be [using deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa).

## Creators
- [Atilla Turkmen](https://github.com/atillaturkmen)
- [Deniz Cakiroglu](https://github.com/DBC201)
