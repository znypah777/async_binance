import aiohttp
from .bases import PublicEndpoint, SignedEndpoint, ProtectedEndpoint, Queryer
from typing import Dict, Any

class PublicDelete(PublicEndpoint):
    REQ_TYPE = "delete"


class SignedDelete(SignedEndpoint):
    REQ_TYPE = "delete"


class ProtectedDelete(ProtectedEndpoint):
    REQ_TYPE = "delete"


def delete_factory(endpoint: str=None,
                   session: aiohttp.ClientSession=None,
                   secrets: Dict[str, str] = None,
                   security_type: str="public",
                   request_params:Dict[str, Any]=None,
                   version: str="1") -> Queryer:
    method = None
    if security_type == "public":
        if version == "1":
            method = PublicDelete(endpoint, session, request_params=request_params)
    elif security_type == "signed":
        if version == "1":
            method = SignedDelete(endpoint,
                                  secrets["api_key"],
                                  secrets["api_secret"],
                                  session,
                                  request_params=request_params)
    else:
        if version == "1":
            method = ProtectedDelete(endpoint, secrets["api_key"], session, request_params=request_params)
    return method