import os
import sys
import argparse
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Read api key and connect to binance client
load_dotenv(dotenv_path="../.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])

client.API_URL = 'https://testnet.binance.vision/api'  # Test url, delete for real life usage


def return_parser():
    parser = argparse.ArgumentParser(description="Auto buy listing")
    parser.add_argument("to_buy", type=str, help="Coin to buy (ex:BTC)")
    parser.add_argument("to_pay", type=str, help="Coin to pay with (ex:USDT)")
    parser.add_argument("amount_to_pay", type=float, help="Amount to pay")
    parser.add_argument("-s", "--stop-percentage", type=float, dest="stop_percentage", help="Percentage loss stop (1 by default)")
    return parser


def new_listing(to_buy, to_sell, amount_to_pay, stop_percentage):
    # Check if coin is listed
    symbol = to_buy+to_sell
    while True:
        try:
            client.get_symbol_info(symbol)
            break
        except BinanceAPIException as e:
            print("Coin not yet listed.")
    print("Coin listed!")

    client.order_market_buy(symbol=symbol, quoteOrderQty=amount_to_pay)

    in_price = client.get_symbol_ticker(symbol=symbol)["price"]  # price we paid
    amount_bought = client.get_asset_balance(asset=to_buy)["free"]
    print(f"Bought {amount_bought} {to_buy} at {in_price}")
    in_price = float(in_price)

    while True:
        current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
        profit = current_price - in_price
        print("In:", in_price, "Curr:", current_price, "Profit:", current_price-in_price)
        if profit == current_price * (stop_percentage/100) * -1:
            client.order_market_sell(symbol=symbol, quoteOrderQty=amount_bought)
            print(f"Sold with {profit} profit")
            break


def main(argv):
    parser = return_parser()
    args = parser.parse_args(argv)
    to_buy = args.to_buy
    to_pay = args.to_pay
    amount_to_pay = args.amount_to_pay
    stop_percentage = 1
    if args.stop_percentage:
        stop_percentage = args.stop_percentage
    new_listing(to_buy, to_pay, amount_to_pay, stop_percentage)


if __name__ == '__main__':
    main(sys.argv[1:])
