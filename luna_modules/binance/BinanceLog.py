from binance import ThreadedWebsocketManager
import time
import json
import datetime
import os


class BinanceLog:
    """Log price information and save to file

    :param symbols: list of symbol strings ["btcusdt, "ethusdt"]
    :type symbols: list
    """
    def __init__(self, symbols):
        self.__symbols = [symbol.upper() for symbol in symbols]
        self.__streams = [symbol+"@trades" for symbol in self.__symbols]
        self.__logs = {}
        self.__twm = ThreadedWebsocketManager()

    def clear_logs(self):
        """Clears the logs in memory

        :return None:
        """
        self.__logs.clear()
        for symbol in self.__symbols:
            self.__logs.update({symbol: []})

    def log(self, duration):
        """Log initialized symbols

        :param duration: duration in seconds
        :type duration: int
        :return None:
        """
        self.__twm.start()
        start_time = None

        def callback(data):
            global start_time
            print(start_time, data)
            if not start_time:
                start_time = data['T']/1000
            elif time.time()-start_time >= duration:
                self.__twm.stop()
            self.__logs[data['s']].append(data['p'])

        self.__twm.start_multiplex_socket(callback=callback, streams=self.__streams)

    def dump(self, path):
        """Dump logs in memory to json file

        :param path: path to be dumped at
        :type path: string
        :return None:
        """
        for symbol in self.__logs:
            log = self.__logs[symbol]
            start_time = log[0]['T']/1000
            time_str = datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d_%H.%M.%S')
            path = os.path.join(path, symbol + '_' + time_str + ".json")
            with open(path, 'w') as file:
                json.dump(log, file)
