def convert_socket_kline(socket_kline):  # sock['k'] as input
    converted = []
    converted.append(socket_kline['t'])
    converted.append(socket_kline['o'])
    converted.append(socket_kline['h'])
    converted.append(socket_kline['l'])
    converted.append(socket_kline['c'])
    converted.append(socket_kline['v'])
    converted.append(socket_kline['T'])
    converted.append(socket_kline['q'])
    converted.append(socket_kline['n'])
    converted.append(socket_kline['V'])
    converted.append(socket_kline['Q'])
    converted.append(socket_kline['B'])


def kline_head_length(kline):
    return abs(kline[4]-kline[1])  # abs(close-open)


def total_kline_length(kline):
    return abs(kline[2] - kline[3])  # high - low


def kline_head_bottom(kline):
    return min(kline[1], kline[4])  # min(open, close)


def kline_head_top(kline):
    return max(kline[1], kline[4])  # max (open, close)


def kline_midpoint(kline):
    return total_kline_length(kline)/2
