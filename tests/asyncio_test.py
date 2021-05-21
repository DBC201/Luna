import asyncio
from binance import AsyncClient, BinanceSocketManager
import time


async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket("BTCUSDT")
    # then start receiving messages
    start = None
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            res_time = float(res['T'])/1000
            if not start:
                start = res_time
            elif res_time-start > 3:
                break
            print(start, res_time, res_time - start)
    await client.close_connection()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())