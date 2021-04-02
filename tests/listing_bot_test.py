import shlex, subprocess
from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env.local")

if __name__ == '__main__':
    client = Client(os.environ["api_key"], os.environ["api_secret"])
    print(client.get_asset_balance("BTC")["free"])
    bot = subprocess.Popen(
        shlex.split("python ../luna_scripts/listing_scripts/listing_bot.py BTC USDT 1000 ../../.env.local"),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    bot.wait()
    stdout, stderr = bot.communicate()
    if stderr:
        print(stderr.decode())
    print(client.get_asset_balance("BTC")["free"])
