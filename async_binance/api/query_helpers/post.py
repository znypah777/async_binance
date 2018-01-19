import aiohttp
from typing import Dict, Any
from .bases import PublicEndpoint, ProtectedEndpoint, SignedEndpoint, Queryer


class PublicPost(PublicEndpoint):
    REQ_TYPE = "post"


class SignedPost(SignedEndpoint):
    REQ_TYPE = "post"


class ProtectedPost(ProtectedEndpoint):
    REQ_TYPE = "post"

def post_factory(endpoint: str=None,
                 session: aiohttp.ClientSession=None,
                 secrets: Dict[str, str]=None,
                 security_type: str="public",
                 request_params:Dict[str, Any]=None,
                 version: str="1") -> Queryer:
    post_method = None
    if security_type == "public":
        if version == "1":
            post_method = PublicPost(endpoint, session, request_params=request_params)
    elif security_type == "signed":
        if version == "1":
            post_method = SignedPost(endpoint,
                                     secrets["api_key"],
                                     secrets["api_secret"],
                                     session,
                                     request_params=request_params)
    else:
        if version == "1":
            post_method = ProtectedPost(endpoint, secrets["api_key"], session, request_params=request_params)
    return post_method