from binance import ThreadedWebsocketManager


def main():

    twm = ThreadedWebsocketManager()
    twm.start()

    def handle_socket_message(msg):
        print(msg)

    streams = ['BNBBTC@miniTicker', 'BNBBTC@bookTicker']
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)


if __name__ == "__main__":
    main()
