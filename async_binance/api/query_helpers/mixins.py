import hmac
import hashlib

from typing import Dict, Any
from urllib.parse import urlencode


class ReqParamVerifyMixin:
    INVALID_REQ_PARAMS = ("data", "headers", "params", "json")

    def _check_req_params(self, request_params:Dict[str, Any]):
        for item in self.INVALID_REQ_PARAMS:
            if item in request_params:
                raise ValueError("Invalid Param")

    def _get_req_params(self, global_req_params:Dict[str, Any],request_params:Dict[str, Any]=None):
        if request_params:
            req_params_copy = {**global_req_params}
            self._check_req_params(request_params)
            req_params_copy.update(request_params)
            return req_params_copy
        return global_req_params

class SignatureGenerateMixin:
    def _gen_api_sig(self, params: Dict[str, Any]=None)->str:
        encoded_params = urlencode(params)
        return self._gen_param_sig(encoded_params)

    def _gen_param_sig(self, endpoint: str) -> str:
        """
            a new feature of v1.1 creates an HMAC hash from a given endpoint
            the endpoint needs to already be formatted with all its necessary arguments already urlencoded
        """
        return hmac.new(self._api_secret.encode(),
                        endpoint.encode(),
                        hashlib.sha256).hexdigest()