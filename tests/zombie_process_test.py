import shlex, subprocess
import time
import os

if __name__ == '__main__':
    processes = []
    listings = ["btcusdt", "ethusdt", "nanousdt"]
    env_path = "../.env.local"
    dump_path = '../trades'
    if not os.path.isdir(dump_path):
        os.mkdir(dump_path)
    ran = False
    while True:
        if not ran:
            for listing in listings:
                p = subprocess.Popen(
                    shlex.split(f"python3 ../luna_scripts/listing_scripts/log_listing.py {listing} {dump_path} {env_path} -d 3"),
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                processes.append(p)
            ran = True
        time.sleep(5)
        for p in processes:
            if p.poll() is None:
                del p
