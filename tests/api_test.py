from luna_modules.binance.BinanceApiWrapper import BinanceApiWrapper
from dotenv import load_dotenv
import os
import time

load_dotenv(dotenv_path="../.env.local")


def print_balances(api):
    print("btc:", api.get_balance("btc"))
    print("usdt:", api.get_balance("usdt"))
    print("-----------------------------------------------")


def test_with_keys():
    url = 'https://testnet.binance.vision/api'
    api = BinanceApiWrapper(os.environ["test_key"], os.environ["test_secret"], url=url)
    print_balances(api)
    order = api.market_buy("btc", "usdt", 100)
    print(order)
    print(order["executedQty"])
    print(float(order["transactTime"]) / 1000)
    print(time.time())
    print(len(order["executedQty"]) - order["executedQty"].find('.') - 1)
    print("-----------------------------------------------")
    print_balances(api)


def test_without_keys():
    api = BinanceApiWrapper()
    print(api.get_price_dict())


if __name__ == '__main__':
    test_with_keys()
    test_without_keys()
