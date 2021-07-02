class Ticker:
    """
    Contains data about ticker name, price at last hour and current price

    Ex: "BTCUSDT" 65000 66000

    :param identifier: ticker symbol (ex: "BTCUSDT")
    :type identifier: string
    :param initial_price: price of coin
    :type initial_price: float
    """

    def __init__(self, identifier, initial_price):
        self.identifier = identifier
        self.initial_price = initial_price
        self.current_price = self.initial_price
        self.reset()

    def reset(self):
        """
        Set all mail flags to false and reset the initial price

        :return: None
        """
        self.dumped = False
        self.pumped = False
        self.called_vitalik = False
        self.initial_price = self.current_price
