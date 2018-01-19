import aiohttp
import asyncio
import random
from typing import Iterable
class _StreamEndpoint:
    def __init__(self, base_endpoint: str=None,target_endpoint: str=None, session: aiohttp.ClientSession=None):
        self._session = session
        self._target_endpoint = f"{base_endpoint}{target_endpoint}"
        self._auto_reconnect = False
        self._retries = 0
        self._delay = list(range(1,30))

    async def _stream(self):
        ws = await self._session.ws_connect(self._target_endpoint)
        while True:
            msg = await ws.receive()
            yield msg
            if msg.type == aiohttp.WSMsgType.CLOSE:
                break
        await ws.close()

    async def _reconnect_stream(self):
        retry_count = 0
        delay = 0
        while True:
            if retry_count >= self._retries:
                break
            if delay:
                await asyncio.sleep(delay)
                delay = 0
            async for msg in self._stream():
                if msg.type == aiohttp.WSMsgType.CLOSE:
                    delay = random.choice(self._delay)
                    retry_count+=1
                else:
                    if retry_count:
                        retry_count = 0
                    yield msg

    async def __aiter__(self):
        async_gen = self._reconnect_stream if self._auto_reconnect else self._stream
        return async_gen()


class SingleStreamEndpoint(_StreamEndpoint):
    def __call__(self, auto_reconnect:bool=True, retries:int=5, **kwargs:str):
        self._auto_reconnect = auto_reconnect
        self._retries = retries
        self._target_endpoint = self._target_endpoint.format(**kwargs)
        return self


class MultiStreamEndpoint(_StreamEndpoint):
    def __call__(self, streams:Iterable[str], auto_reconnect:bool=True, retries:int=5):
        self._auto_reconnect = auto_reconnect
        self._retries = retries
        joined_targets = "/".join(streams)
        self._target_endpoint = f"{self._target_endpoint}={joined_targets}"
        return self


def stream_endpoints(session:aiohttp.ClientSession=None, base_endpoint:str=None, version:str=None):
    return {
        "aggregate_trade": SingleStreamEndpoint(base_endpoint=base_endpoint,
                                                target_endpoint="/ws/{symbol}@aggTrade",
                                                session=session),
        "multi_stream": MultiStreamEndpoint(base_endpoint=base_endpoint,
                                            target_endpoint="/stream?streams",
                                            session=session),
        "candles_stream": SingleStreamEndpoint(base_endpoint=base_endpoint,
                                               target_endpoint="/ws/{symbol}@kline_{interval}",
                                               session=session),
        "ticker_stream":  SingleStreamEndpoint(base_endpoint=base_endpoint,
                                               target_endpoint="/ws/{symbol}@ticker",
                                               session=session),
        "all_ticker_stream": SingleStreamEndpoint(base_endpoint=base_endpoint,
                                                  target_endpoint="/ws/!ticker@arr",
                                                  session=session)
    }

