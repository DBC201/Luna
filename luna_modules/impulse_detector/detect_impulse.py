from luna_modules.kline_patterns.patterns import is_bullish_engulf
from luna_modules.kline_patterns.patterns import is_piercing


def is_impulse_wave(klines):
    return is_consecutive_bullish_engulf(klines) or is_triple_piercing(klines)


def is_consecutive_bullish_engulf(klines):
    return is_bullish_engulf(klines[:-1]) and is_bullish_engulf(klines)


def is_triple_piercing(klines):
    return is_piercing(klines[:-2]) and is_piercing(klines[:-1]) and is_piercing(klines)
