import aiohttp
import time
from .bases import _PublicEndpoint, _SignedEndpoint, _ProtectedEndpoint, Queryer
from typing import Dict, Any

# class PublicDelete(_PublicEndpoint):
#     async def _execute_query(self, url: str, request_params:Dict[str, Any], **kwargs: str) -> Dict[str, Any]:
#         return await self._query("delete", url, params=kwargs, **request_params)
#
#
# class SignedDelete(_SignedEndpoint):
#     async def _execute_query(self, url: str, request_params:Dict[str, Any], **kwargs: str) -> Dict[str, Any]:
#         kwargs["timestamp"] = str(int(time.time() * 1000))
#         kwargs["signature"] = self._gen_api_sig(params=kwargs)
#         headers = {"X-MBX-APIKEY": self._api_key}
#         return await self._query("delete", url, params=kwargs, headers=headers, **request_params)
#
#
# class ProtectedDelete(_ProtectedEndpoint):
#     async def _execute_query(self, url: str, request_params:Dict[str, Any], **kwargs: str) -> Dict[str, Any]:
#         headers = {"X-MBX-APIKEY": self._api_key}
#         return await self._query("delete", url, headers=headers, params=kwargs, **request_params)

class PublicDelete(_PublicEndpoint):
    REQ_TYPE = "delete"


class SignedDelete(_SignedEndpoint):
    REQ_TYPE = "delete"


class ProtectedDelete(_ProtectedEndpoint):
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