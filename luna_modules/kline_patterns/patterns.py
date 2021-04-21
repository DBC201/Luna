import os, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT)
from luna_modules.kline_patterns import kline_helpers


def is_hammer(klines):
    head_bottom = kline_helpers.kline_head_bottom(klines[-1])
    midpoint = kline_helpers.kline_midpoint(klines[-1])
    return kline_helpers.is_red(klines[-2]) and head_bottom > midpoint


def is_hanging_man(klines):
    head_bottom = kline_helpers.kline_head_bottom(klines[-1])
    midpoint = kline_helpers.kline_midpoint(klines[-1])
    return (not kline_helpers.is_red(klines[-2])) and head_bottom > midpoint


def is_morning_star(klines):
    first_length = kline_helpers.kline_head_length(klines[-3])
    middle_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    first_red = kline_helpers.is_red(klines[-3])
    third_green = not kline_helpers.is_red(klines[-1])
    return first_red and third_green and middle_length < first_length and middle_length < final_length


def is_evening_star(klines):
    first_length = kline_helpers.kline_head_length(klines[-3])
    middle_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    first_green = not kline_helpers.is_red(klines[-3])
    third_red = kline_helpers.is_red(klines[-1])
    return first_green and third_red and middle_length < first_length and middle_length < final_length

# below 4 functions are independent from the previous trend and just tell where the last candle is headed
def is_bullish_engulf(klines):
    prev_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    final_green = not kline_helpers.is_red(klines[-1])
    return final_green and prev_length < final_length


def is_bearish_engulf(klines):
    prev_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    final_red = kline_helpers.is_red(klines[-1])
    return final_red and prev_length < final_length


def is_piercing(klines):
    prev_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    final_green = not kline_helpers.is_red(klines[-1])
    return final_green and prev_length/2 < final_length


def is_dark_cloud_cover(klines):
    prev_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    final_red = kline_helpers.is_red(klines[-1])
    return final_red and prev_length/2 < final_length


def pattern_matches(klines):
    matches = []
    if is_hammer(klines):
        matches.append("hammer")
    if is_hanging_man(klines):
        matches.append("hanging man")
    if is_bearish_engulf(klines):
        matches.append("bearish engulf")
    if is_bullish_engulf(klines):
        matches.append("bullish engulf")
    if is_evening_star(klines):
        matches.append("evening star")
    if is_morning_star(klines):
        matches.append("morning star")
    if is_piercing(klines):
        matches.append("piercing")
    if is_dark_cloud_cover(klines):
        matches.append("dark cloud cover")
    return matches
