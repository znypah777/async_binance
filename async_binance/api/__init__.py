import aiohttp
import asyncio
from typing import Dict, Any
from .sections import market_endpoints, account_endpoints, public_endpoints

class RestClient:
    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 session: aiohttp.ClientSession,
                 base_url: str="https://api.binance.com",
                 request_params:Dict[str, Any]=None,
                 markets_version="1",
                 accounts_version="3",
                 public_version="1"):
        self._endpoints = {}
        self._endpoints.update(market_endpoints(base_url=base_url,
                                                secrets={"api_key": api_key, "api_secret": api_secret},
                                                session=session,
                                                request_params=request_params,
                                                version=markets_version))
        self._endpoints.update(account_endpoints(base_url=base_url,
                                                 secrets={"api_key": api_key, "api_secret": api_secret},
                                                 session=session,
                                                 request_params=request_params,
                                                 version=accounts_version))
        self._endpoints.update(public_endpoints(base_url=base_url,
                                                secrets={"api_key": api_key, "api_secret": api_secret},
                                                session=session,
                                                request_params=request_params,
                                                version=public_version))
    def __getattr__(self, item):
        return self._endpoints[item]