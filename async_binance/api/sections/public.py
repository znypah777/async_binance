import aiohttp
from typing import Dict, Union, Any
from ..query_helpers.bases import Queryer
from ..query_helpers import get_factory, post_factory, delete_factory




def v1_public(base_url: str=None,
              secrets: Dict[str, str]=None,
              request_params:Dict[str, Any]=None,
              session:aiohttp.ClientSession=None) -> Dict[str, Queryer]:
    return {
        "ping": get_factory(endpoint=f"{base_url}/api/v1/ping",
                            session=session,
                            secrets=secrets,
                            request_params=request_params,
                            version="1"),
        "server_time": get_factory(endpoint=f"{base_url}/api/v1/time",
                                   session=session,
                                   secrets=secrets,
                                   request_params=request_params,
                                   version="1"),
        "exchange_info": get_factory(endpoint=f"{base_url}/api/v1/exchangeInfo",
                                     session=session,
                                     secrets=secrets,
                                     request_params=request_params,
                                     version="1"),
    }


def public_endpoints(base_url: str=None,
                     secrets: Dict[str, str]=None,
                     session:aiohttp.ClientSession=None,
                     request_params:Dict[str, Any]=None,
                     version: str="1"):
    endpoints = None
    if version == "1":
        endpoints = v1_public(base_url=base_url, secrets=secrets, session=session, request_params=request_params)

    if endpoints is None:
        raise ValueError("Unknown Public version")
    return endpoints