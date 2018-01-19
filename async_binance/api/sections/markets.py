from ..query_helpers.bases import Queryer
from ..query_helpers import get_factory, post_factory, delete_factory
from typing import Dict, Union, Any


import aiohttp



def v1_markets(base_url: str=None,
               secrets: Dict[str, str]=None,
               request_params: Dict[str, Any]=None,
               session:aiohttp.ClientSession=None) -> Dict[str, Queryer]:
    return {
        "get_order_book": get_factory(endpoint=f"{base_url}/api/v1/depth",
                                      session=session,
                                      request_params=request_params,
                                      secrets=secrets),
        "recent_trades": get_factory(endpoint=f"{base_url}/api/v1/trades",
                                     session=session,
                                     request_params=request_params,
                                     secrets=secrets,
                                     security_type="protected"),
        "historical_trades": get_factory(endpoint=f"{base_url}/api/v1/historicalTrades",
                                         session=session,
                                         secrets=secrets,
                                         request_params=request_params,
                                         security_type="protected"),
        "aggregate_trades": get_factory(endpoint=f"{base_url}/api/v1/aggTrades",
                                        session=session,
                                        secrets=secrets,
                                        security_type="protected"),
        "candle_sticks": get_factory(endpoint=f"{base_url}/api/v1/klines",
                                     session=session,
                                     secrets=secrets,
                                     request_params=request_params,
                                     security_type="protected")
    }


def market_endpoints(base_url: str=None,
                     secrets: Dict[str, str]=None,
                     session:aiohttp.ClientSession=None,
                     request_params: Dict[str, Any]=None,
                     version: str="1"):
    endpoints = None
    if version == "1":
        endpoints = v1_markets(base_url=base_url, secrets=secrets, session=session, request_params=request_params)
    if endpoints is None:
        raise ValueError("Unknown Market Version")
    return endpoints
    