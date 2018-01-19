import aiohttp
import time
from typing import Dict, Any, Tuple
from .bases import PublicEndpoint, SignedEndpoint, ProtectedEndpoint, Queryer

class PublicGet(PublicEndpoint):
    REQ_TYPE = "get"

class SignedGet(SignedEndpoint):
    REQ_TYPE = "get"

class ProtectedGet(ProtectedEndpoint):
    REQ_TYPE = "get"


def get_factory(endpoint: str=None,
                session: aiohttp.ClientSession=None,
                secrets: Dict[str, str]=None,
                request_params: Dict[str, Any]=None,
                security_type: str="public",
                version: str="1") -> Queryer:
    method = None
    if security_type == "public":
        if version == "3":
            method = PublicGet(endpoint, session, request_params=request_params)
    elif security_type == "signed":
        if version == "3":
            method = SignedGet(endpoint, secrets["api_key"], secrets["api_secret"], session, request_params=request_params)
    else:
        if version == "3":
            method = ProtectedGet(endpoint, secrets["api_key"], session, request_params=request_params)
    return method

