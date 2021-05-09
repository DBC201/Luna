import requests
from datetime import datetime

# https://www.gate.io/docs/apiv4/en

host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
url = '/spot/candlesticks'
query_param = '?currency_pair=MIR_USDT&interval=1m&limit=1000&from=1618815600&to=1618858800'

x = requests.get(host + prefix + url + query_param, headers=headers)
print(x.json())
for i in x.json():
    d = datetime.utcfromtimestamp(int(i[0])).strftime('%Y-%m-%d %H:%M:%S')
    print(d)
    print("opening: " + i[5])
    print("closing: " + i[2])
    print("highest: " + i[3])
    print("lowest: " + i[4])
    print()
