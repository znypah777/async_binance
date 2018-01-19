import aiohttp
import time
from typing import Dict, Any, Tuple
from .bases import _PublicEndpoint, _SignedEndpoint, _ProtectedEndpoint, Queryer



# class PublicGet(_PublicEndpoint):
#     async def _execute_query(self, url:str, **kwargs: str) -> Dict[str, Any]:
#         return await self._query("get", url, **kwargs)

# class PublicGet(_PublicEndpoint):
#     async def _execute_query(self, url:str, request_params:Dict[str, Any]=None, **kwargs: str) -> Dict[str, Any]:
#         if request_params:
#             req_params = {**self._request_params}
#             req_params.update(request_params)
#         return await self._query("get", url, params=kwargs, **request_params)
#
# class SignedGet(_SignedEndpoint):
#     async def _execute_query(self, url:str, request_params:Dict[str, Any], **kwargs: str) -> Dict[str, Any]:
#         kwargs["timestamp"] = str(int(time.time() * 1000))
#         kwargs["signature"] = self._gen_api_sig(params=kwargs)
#         headers = {"X-MBX-APIKEY": self._api_key}
#         return await self._query("get", url, params=kwargs, headers=headers,**request_params)
#
# class ProtectedGet(_ProtectedEndpoint):
#     async def _execute_query(self, url, request_params:Dict[str, Any]=None, **kwargs: str) -> Dict[str, Any]:
#         headers = {"X-MBX-APIKEY": self._api_key}
#         return await self._query("get", url, headers=headers, params=kwargs, **request_params)


class PublicGet(_PublicEndpoint):
    REQ_TYPE = "get"

class SignedGet(_SignedEndpoint):
    REQ_TYPE = "get"

class ProtectedGet(_ProtectedEndpoint):
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

