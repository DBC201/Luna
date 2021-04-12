import os
import shlex, subprocess
from binance.client import Client
from dotenv import load_dotenv

ENV_PATH = "../.env.local"
load_dotenv(dotenv_path=ENV_PATH)
client = Client(os.environ["api_key"], os.environ["api_secret"])


if __name__ == '__main__':
    symbol = "BTCUSDT"
    save_path = "../trades"
    process = subprocess.Popen(
        shlex.split(f"python ../luna_scripts/listing_scripts/log_listing.py {symbol} {save_path} {ENV_PATH}"),
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.wait()
    stdout, stderr = process.communicate()
    if stdout:
        print("stdout:", stdout.decode())

    if stderr:
        print("stderr:", stderr.decode())
