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
                bot = subprocess.Popen(
                    shlex.split(f"python ../luna_scripts/listing_log/binance_log.py {listing} {dump_path} -d 3"),
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                processes.append(bot)
                bot = None
            ran = True
        time.sleep(5)
        for p in processes:
            stdout, stderr = p.communicate()
            print(stdout, stderr)
            del p
        processes.clear()

