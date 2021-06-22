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
        self.__logs = {}
        for symbol in self.__symbols:
            self.__logs.update({symbol: []})
        self.__twm = None

    def clear_logs(self):
        """Clears the logs in memory

        :return: None
        """
        self.__logs.clear()
        for symbol in self.__symbols:
            self.__logs.update({symbol: []})

    def log(self, duration):
        """Log initialized symbols

        :param duration: duration in seconds
        :type duration: int
        :return: None
        """
        self.__twm = ThreadedWebsocketManager()
        self.__twm.start()
        start_time = None
        logs = self.__logs
        stop = False

        def callback(data):
            nonlocal start_time, logs, stop
            if not start_time:
                start_time = data['T']/1000
            elif time.time()-start_time >= duration:
                stop = True
            logs[data['s']].append(data)

        for symbol in self.__symbols:
            self.__twm.start_trade_socket(symbol=symbol, callback=callback)
        while not stop:
            time.sleep(1)
        self.stop()

    def stop(self):
        """Stop all threads

        :return: None
        """
        if self.__twm:
            self.__twm.stop()
            while self.__twm.is_alive():
                time.sleep(1)
            self.__twm = None

    def dump(self, path):
        """Dump logs in memory to json file

        :param path: path to be dumped at
        :type path: string
        :return: None
        """
        for symbol in self.__logs:
            log = self.__logs[symbol]
            if log:
                start_time = log[0]['T']/1000
                time_str = datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d_%H.%M.%S')
                file_path = os.path.join(path, symbol + '_' + time_str + ".json")
                with open(file_path, 'w') as file:
                    json.dump(log, file)
