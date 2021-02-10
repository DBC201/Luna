from luna_modules.kline_patterns import trends
from luna_modules.kline_patterns import kline_helpers


def is_hammer(klines):
    head_bottom = kline_helpers.kline_head_bottom(klines[-1])
    midpoint = kline_helpers.kline_midpoint(klines[-1])
    return trends.is_bear(klines) and head_bottom > midpoint


def is_hanging_man(klines):
    head_top = kline_helpers.kline_head_top(klines[-1])
    midpoint = kline_helpers.kline_midpoint(klines[-1])
    return trends.is_bull(klines) and head_top < midpoint



