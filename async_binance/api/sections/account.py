import aiohttp
from typing import Dict, Any
from ..query_helpers.bases import Queryer
from ..query_helpers import get_factory, post_factory, delete_factory


def v3_account(base_url: str=None,
               secrets: Dict[str, str]=None,
               request_params:Dict[str, Any]=None,
               session:aiohttp.ClientSession=None) -> Dict[str, Queryer]:
    return {
        "new_order": post_factory(endpoint=f"{base_url}/api/v3/order",
                                  secrets=secrets,
                                  session=session,
                                  request_params=request_params,
                                  security_type="signed",
                                  version="3"),
        "test_new_order": post_factory(endpoint=f"{base_url}/api/v3/order/test",
                                       secrets=secrets,
                                       session=session,
                                       security_type="signed",
                                       request_params=request_params,
                                       version="3"),
        "check_order_status": get_factory(endpoint=f"{base_url}/api/v3/order",
                                          secrets=secrets,
                                          security_type="signed",
                                          request_params=request_params,
                                          version="3"),
        "cancel_order": delete_factory(endpoint=f"{base_url}/api/v3/order",
                                       secrets=secrets,
                                       session=session,
                                       security_type="signed",
                                       request_params=request_params,
                                       version="3"),
        "open_orders": get_factory(endpoint=f"{base_url}/api/v3/openOrders",
                                   secrets=secrets,
                                   session=session,
                                   security_type="signed",
                                   version="3"),
        "account_info": get_factory(endpoint=f"{base_url}/api/v3/account",
                                    secrets=secrets,
                                    session=session,
                                    security_type="signed",
                                    request_params=request_params,
                                    version="3")
    }

def account_endpoints(base_url: str=None,
                      secrets: Dict[str, str]=None,
                      session:aiohttp.ClientSession=None,
                      request_params:Dict[str, Any]=None,
                      version: str="3"):
    endpoints = None
    if version == "3":
        endpoints = v3_account(base_url=base_url, secrets=secrets, session=session, request_params=request_params)

    if endpoints is None:
        raise ValueError("Unknown Account Version")
    return endpoints




