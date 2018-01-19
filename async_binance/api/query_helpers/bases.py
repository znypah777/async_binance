import aiohttp
import time
from typing import Dict, Any
from .mixins import ReqParamVerifyMixin, SignatureGenerateMixin

class ApiCaller:
    def __init__(self, session:aiohttp.ClientSession):
        self._session = session

    async def _query(self, query_type:str, endpoint:str, **kwargs: str) -> Dict[str, Any]:
        async with getattr(self._session, query_type)(endpoint, **kwargs) as resp:
            data = await resp.json()
            return data


class Queryer(ApiCaller, ReqParamVerifyMixin):

    REQ_TYPE="get"

    def __init__(self, url:str, session:aiohttp.ClientSession, request_params:Dict[str, Any]=None):
        self._url = url
        self._request_params = request_params or {}
        super().__init__(session)

    async def _execute_query(self, url: str, request_params:Dict[str, Any]=None, **kwargs: str) -> Dict[str, Any]:
        pass

    async def __call__(self, **kwargs:str):
        return await self._execute_query(self._url, **kwargs)


class PublicEndpoint(Queryer):
    pass


class ProtectedEndpoint(Queryer):
    API_KEY_HEADER = "X-MBX-APIKEY"

    def __init__(self, url: str, api_key: str, session: aiohttp.ClientSession, request_params:Dict[str, Any]=None):
        self._url = url
        self._api_key = api_key
        super().__init__(url, session, request_params=request_params)

    async def _execute_query(self, url:str, request_params:Dict[str, Any]=None, **kwargs: str) -> Dict[str, Any]:
        headers = {self.API_KEY_HEADER: self._api_key}
        req_params = self._get_req_params(self._request_params, request_params=request_params)
        return await self._query(self.REQ_TYPE, url, params=kwargs, headers=headers,**req_params)


class SignedEndpoint(Queryer, SignatureGenerateMixin):
    API_KEY_HEADER = "X-MBX-APIKEY"
    TIMESTAMP_PARAM = "timestamp"
    SIGNATURE_PARAM = "signature"

    def __init__(self, url: str, api_key: str, api_secret: str, session: aiohttp.ClientSession, request_params:Dict[str, Any]=None):
        self._url = url
        self._api_key = api_key
        self._api_secret = api_secret
        super().__init__(url, session, request_params=request_params)

    async def _execute_query(self, url:str, request_params:Dict[str, Any]=None, **kwargs: str) -> Dict[str, Any]:
        kwargs[self.TIMESTAMP_PARAM] = str(int(time.time() * 1000))
        kwargs[self.SIGNATURE_PARAM] = self._gen_api_sig(params=kwargs)
        headers = {self.API_KEY_HEADER: self._api_key}
        req_params = self._get_req_params(self._request_params, request_params=request_params)
        return await self._query(self.REQ_TYPE, url, params=kwargs, headers=headers,**req_params)


