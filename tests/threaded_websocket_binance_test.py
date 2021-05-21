from binance import ThreadedWebsocketManager
import time

start = None
stopped = False


def handle_socket_message(msg):
    global start, stopped
    if stopped:
        return
    res_time = float(msg['T']) / 1000
    if not start:
        start = res_time
    elif res_time - start > 3:
        start = None
        stopped = True
        return
    print(msg)
    # print(msg['s'], msg['p'])
    print(res_time - start)


def single_trade_test():
    twm = ThreadedWebsocketManager()
    twm.start()
    global stopped
    twm.start_trade_socket(symbol="BTCUSDT", callback=handle_socket_message)
    twm.start_trade_socket(symbol="ETHUSDT", callback=handle_socket_message)
    while not stopped:
        print(start)
        time.sleep(1)
    print("stopping...")
    twm.stop()
    while twm.is_alive():
        time.sleep(1)
    stopped = False


if __name__ == "__main__":
    single_trade_test()
    print("-----------------------------------------")

    single_trade_test()
