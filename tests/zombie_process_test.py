import shlex, subprocess
import time
import os

import concurrent.futures


def initiate_log(symbol, dump_path):
    return subprocess.run(
        shlex.split(f"python3 ../luna_scripts/listing_log/binance_log.py {symbol} {dump_path} -d 3"),
        shell=True
    )


if __name__ == '__main__':
    listings = ["btcusdt", "ethusdt"]
    dump_path = '../trades'
    if not os.path.isdir(dump_path):
        os.mkdir(dump_path)
    ran = False
    while True:
        if not ran:
            with concurrent.futures.ThreadPoolExecutor() as thread:
                for listing in listings:
                    thread.submit(initiate_log, listing, dump_path)
            ran = True
        time.sleep(5)
