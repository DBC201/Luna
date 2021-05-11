import shlex, subprocess
import time
import os

if __name__ == '__main__':
    processes = []
    listings = ["btcusdt", "ethusdt", "nanousdt"]
    dump_path = '../trades'
    if not os.path.isdir(dump_path):
        os.mkdir(dump_path)
    ran = False
    while True:
        if not ran:
            for listing in listings:
                subprocess.Popen(
                    shlex.split(
                        f"python3 ../luna_scripts/listing_log/binance_log.py {listing} "
                        f"{dump_path} -d 3 > ../outputs/{listing}.txt"
                    )
                )
            ran = True
        time.sleep(5)
