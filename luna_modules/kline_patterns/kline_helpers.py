def convert_socket_kline(socket_kline):  # sock['k'] as input
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


def kline_head_length(kline):
    return abs(kline[4]-kline[1])  # abs(close-open)


def total_kline_length(kline):
    return abs(kline[2] - kline[3])  # high - low


def kline_head_bottom(kline):
    return min(kline[1], kline[4])  # min(open, close)


def kline_head_top(kline):
    return max(kline[1], kline[4])  # max (open, close)


def kline_midpoint(kline):
    return kline[3] + total_kline_length(kline)/2  # low + total_length


def is_red(kline):
    return kline[1] > kline[4]  # open < close
