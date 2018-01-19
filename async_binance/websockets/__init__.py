import aiohttp
from .streams import stream_endpoints

class WebSocketClient:
    def __init__(self, session:aiohttp.ClientSession, base_url:str="wss://stream.binance.com:9443"):
        self._endpoints = stream_endpoints(session=session, base_endpoint=base_url)



    def __getattr__(self, item):
        return self._endpoints[item]




