# LUNA
[Luna](https://github.com/DBC201/Luna) is a program consisting of different modules and scripts for binance using python-binance library. However
the modules should work with the right input format which have been documented in their relative folder.

## Dependencies
- [python-binance](https://github.com/sammchardy/python-binance)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## For Windows
- Run 'pipenv install' in root folder. This should install the required dependencies.
- In case of time sync error, sync your os time with internet time.
    ![windows time sync](./docs/pictures/sync%20internet%20time.png)
- The file for Twisted library is also included in this repo because I have
  had issues setting it up. I also had to install two dependencies from visual studio.
  Try to run pipenv first. If it doesn't work, you can try the solutions below.
    - https://wiki.python.org/moin/WindowsCompilers
        - Developer tools:
            ![mscv download](./docs/pictures/visual%20studio%20developer%20tools%20turkish.png)
        - Windows sdk:
            ![sdk_download](./docs/pictures/latest%20windows%2010%20sdk.png)
            
## For Ubuntu
- At the time of this readme, Ubuntu repositories only have python up to 3.8. However this doesn't pose an issue and
most of the programs seem to work fine. If not one option could be [using deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa).
- Pipenv file is only for windows only since it installs the twisted file manually. Hence pipenv install shouldn't be run.
Instead just install the listed dependencies manually by doing
    -  ```sudo apt install python3-pip``` (check if pip is installed)
    - ```pip3 install python-dotenv```
    - ```pip3 install python-binance```


## Creators
- [Atilla Turkmen](https://github.com/atillaturkmen)
- [Deniz Cakiroglu](https://github.com/DBC201)
