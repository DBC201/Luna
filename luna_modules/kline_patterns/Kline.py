class Kline:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def convert_socket_kline(socket_kline):  # sock['k'] as input
        """Convert socket_kline to regular kline

        Two different api methods give different formats, see kline_docs.txt

        :param socket_kline: data from socket
        :type socket_kline: dict
        :return: converted data
        :rtype: list
        """
        converted = []
        converted.append(float(socket_kline['t']))
        converted.append(float(socket_kline['o']))
        converted.append(float(socket_kline['h']))
        converted.append(float(socket_kline['l']))
        converted.append(float(socket_kline['c']))
        converted.append(float(socket_kline['v']))
        converted.append(float(socket_kline['T']))
        converted.append(float(socket_kline['q']))
        converted.append(float(socket_kline['n']))
        converted.append(float(socket_kline['V']))
        converted.append(float(socket_kline['Q']))
        converted.append(float(socket_kline['B']))
        return converted

    def head_length(self):
        return abs(self.data[4] - self.data[1])  # abs(close-open)

    def total_length(self):
        return abs(self.data[2] - self.data[3])  # high - low

    def head_bottom(self):
        return min(self.data[1], self.data[4])  # min(open, close)

    def head_top(self):
        return max(self.data[1], self.data[4])  # max (open, close)

    def midpoint(self):
        return self.data[3] + self.total_length() / 2  # low + total_length

    def is_red(self):
        return self.data[1] > self.data[4]  # open > close
