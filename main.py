import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv(dotenv_path="./.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])

print(client.get_asset_balance("USDT"))