class KlinePatterns:
    def __init__(self, klines):
        self.klines = klines
        self.__pattern_functions = {
            "hammer": self.is_hammer,
            "hanging_man": self.is_hanging_man,
            "morning_star": self.is_morning_star,
            "evening_star": self.is_evening_star,
            "bullish_engulf": self.is_bullish_engulf,
            "bearish_engulf": self.is_bearish_engulf,
            "piercing": self.is_piercing,
            "dark_cloud_cover": self.is_dark_cloud_cover
        }

    def is_hammer(self):
        head_bottom = self.klines[-1].head_bottom()
        midpoint = self.klines[-1].midpoint()
        return self.klines[-3].is_red() and head_bottom > midpoint

    def is_hanging_man(self):
        head_bottom = self.klines[-1].head_bottom()
        midpoint = self.klines[-1].midpoint()
        return (not self.klines[-3].is_red()) and head_bottom > midpoint

    def is_morning_star(self):
        first_length = self.klines[-3].head_length()
        middle_length = self.klines[-2].head_length()
        final_length = self.klines[-1].head_length()
        first_red = self.klines[-3].is_red()
        third_green = not self.klines[-1].is_red()
        return first_red and third_green and middle_length < first_length and middle_length < final_length

    def is_evening_star(self):
        first_length = self.klines[-3].head_length()
        middle_length = self.klines[-2].head_length()
        final_length = self.klines[-1].head_length()
        first_green = not self.klines[-3].is_red()
        third_red = self.klines[-1].is_red()
        return first_green and third_red and middle_length < first_length and middle_length < final_length

    # below 4 functions are independent from the previous trend and just tell where the last candle is headed
    def is_bullish_engulf(self):
        prev_length = self.klines[-2].head_length()
        final_length = self.klines[-1].head_length()
        final_green = not self.klines[-1].is_red()
        return final_green and prev_length < final_length

    def is_bearish_engulf(self):
        prev_length = self.klines[-2].head_length()
        final_length = self.klines[-1].head_length()
        final_red = self.klines[-1].is_red()
        return final_red and prev_length < final_length

    def is_piercing(self):
        prev_length = self.klines[-2].head_length()
        final_length = self.klines[-1].head_length()
        final_green = not self.klines[-1].is_red()
        return final_green and prev_length/2 < final_length

    def is_dark_cloud_cover(self):
        prev_length = self.klines[-2].head_length()
        final_length = self.klines[-1].head_length()
        final_red = self.klines[-1].is_red()
        return final_red and prev_length/2 < final_length

    def add_new_kline(self, kline):
        self.klines.append(kline)

    def pop_kline(self, index=-1):
        return self.klines.pop(index)

    def get_patterns(self):
        patterns = {}
        for key in self.__pattern_functions:
            patterns.update({key: self.__pattern_functions[key]()})
        return patterns
