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
                p = subprocess.Popen(
                    shlex.split(f"python3 ../luna_scripts/listing_log/binance_log.py {listing} {dump_path} -d 3"),
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                processes.append([listing, p])
            ran = True
        time.sleep(5)
        print(processes)
        for i in processes:
            name, p = i
            stdout, stderr = p.communicate()
            if stdout:
                print(name, "stdout:", stdout)

            if stderr:
                print(name, "stderr:", stderr)
            p.kill()
        p = None
        processes.clear()
