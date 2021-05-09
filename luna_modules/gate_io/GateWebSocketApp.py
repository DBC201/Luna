# !/usr/bin/env python
# coding: utf-8

import hashlib
import hmac
import json
import time

from websocket import WebSocketApp


# https://www.gate.io/docs/apiv4/ws/index.html
class GateWebSocketApp(WebSocketApp):
    """Socket for Gate.io\n
    You should define on_message and on_open functions

    :param api_key: your api key, not necessary for price checking
    :type api_key: string
    :param api_secret: api secret
    :type api_secret: string
    :param url: "wss://api.gateio.ws/ws/v4/"
    :type url: string
    """
    def __init__(self, api_key, api_secret, url="wss://api.gateio.ws/ws/v4/", **kwargs):
        super(GateWebSocketApp, self).__init__(url, **kwargs)
        self._api_key = api_key
        self._api_secret = api_secret

    def _send_ping(self, interval, event, payload):
        while not event.wait(interval):
            self.last_ping_tm = time.time()
            if self.sock:
                try:
                    self.sock.ping()
                except Exception as ex:
                    break
                try:
                    self._request("spot.ping", auth_required=False)
                except Exception as e:
                    raise e

    def _request(self, channel, event=None, payload=None, auth_required=True):
        current_time = int(time.time())
        data = {
            "time": current_time,
            "channel": channel,
            "event": event,
            "payload": payload,
        }
        if auth_required:
            message = 'channel=%s&event=%s&time=%d' % (channel, event, current_time)
            data['auth'] = {
                "method": "api_key",
                "KEY": self._api_key,
                "SIGN": self.get_sign(message),
            }
        data = json.dumps(data)
        self.send(data)

    def get_sign(self, message):
        h = hmac.new(self._api_secret.encode("utf8"), message.encode("utf8"), hashlib.sha512)
        return h.hexdigest()

    def subscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "subscribe", payload, auth_required)

    def unsubscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "unsubscribe", payload, auth_required)
