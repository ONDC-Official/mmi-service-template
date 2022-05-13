import os

import requests

from main.config import get_config_by_name

KNOWLARITY_URl = "https://kpi.knowlarity.com/Basic/v1/account/call/makecall"

def call_patron_with_given_number(customer_phone_number,seller_phone_number):
    params = {"k_number": get_config_by_name("knowlarity_number"),
              "agent_number": seller_phone_number,
              "customer_number": customer_phone_number}
    headers = {"x-api-key": get_config_by_name("knowlarity_api_key"),
               "Authorization": get_config_by_name("knowlarity_authorization_header_key")}
    response = requests.post(KNOWLARITY_URl,headers=headers,json=params)
    return response.json()


def call_patron(**kwargs):
    return call_patron_with_given_number(**kwargs)
