def is_bear(klines):
    return klines[-1][4] < klines[0][1]  # close < open


def is_bull(klines):
    return klines[-1][4] > klines[0][1]  # close > open
