from binance import ThreadedWebsocketManager


def main():
    symbol = 'BTCUSDT'

    twm = ThreadedWebsocketManager()
    twm.start()

    def handle_socket_message(msg):
        print(msg)

    twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)


if __name__ == "__main__":
    main()
