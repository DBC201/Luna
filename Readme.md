# LUNA

Luna is a program consisting of different modules and scripts for binance using python-binance library, however we tried
to make it modular as much as we could and luna_modules can be used anywhere with the right input format.

## Dependencies
- [python-binance](https://github.com/sammchardy/python-binance)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## For Windows
- Run 'pipenv install' in root folder. This should install the required dependencies.
- In case of time sync error, sync your os time with internet time.
    - ![windows time sync](./docs/pictures/sync%20internet%20time.png)
- The file for Twisted library is also included in this repo because I have
  had issues setting it up. I also had to install two dependencies from visual studio.
  Try to run pipenv first. If it doesn't work, you can try the solutions below.
    - https://wiki.python.org/moin/WindowsCompilers
        - Developer tools:
            ![mscv download](./docs/pictures/visual%20studio%20developer%20tools%20turkish.png)
        - Windows sdk:
            ![sdk_download](./docs/pictures/latest%20windows%2010%20sdk.png)
