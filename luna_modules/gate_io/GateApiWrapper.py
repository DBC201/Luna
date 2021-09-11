import requests


def get_first_thousand_orders(symbol, last_id="1"):
    return requests.get(
        "https://api.gateio.ws/api/v4/spot/trades",
        params={
            "currency_pair": symbol,
            "limit": "1000",
            "last_id": last_id
        }
    ).json()


def get_all_tickers():
    return requests.get("https://api.gateio.ws/api/v4/spot/currency_pairs").json()
