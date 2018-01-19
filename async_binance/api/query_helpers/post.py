import aiohttp
import time
from typing import Dict, Any
from .bases import _PublicEndpoint, _ProtectedEndpoint, _SignedEndpoint, Queryer


# class PublicPost(_PublicEndpoint):
#     async def _execute_query(self, url: str, request_params:Dict[str, Any], **kwargs: str) -> Dict[str, Any]:
#         return await self._query("post", url, params=kwargs, **request_params)
#
#
# class SignedPost(_SignedEndpoint):
#     async def _execute_query(self, url: str, request_params:Dict[str, Any], **kwargs: str) -> Dict[str, Any]:
#         kwargs["timestamp"] = str(int(time.time() * 1000))
#         kwargs["signature"] = self._gen_api_sig(params=kwargs)
#         headers = {"X-MBX-APIKEY": self._api_key}
#         return await self._query("post", url, params=kwargs, headers=headers, **request_params)
#
#
# class ProtectedPost(_ProtectedEndpoint):
#     async def _execute_query(self, url: str, request_params:Dict[str, Any],**kwargs: str) -> Dict[str, Any]:
#         headers = {"X-MBX-APIKEY": self._api_key}
#         return await self._query("post", url, params=kwargs, headers=headers, **request_params)


class PublicPost(_PublicEndpoint):
    REQ_TYPE = "post"


class SignedPost(_SignedEndpoint):
    REQ_TYPE = "post"


class ProtectedPost(_ProtectedEndpoint):
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