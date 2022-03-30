import json
import os

import requests
from cachetools import cached, LRUCache, TTLCache

from main.config import get_config_by_name

MMI_ENDPOINT = "https://outpost.mapmyindia.com/api"
MMI_AUTO_COMPLETE_ENDPOINT = "https://atlas.mapmyindia.com/api/places/search/json"
MMI_EXPLORE_API = "https://explore.mappls.com"

@cached(TTLCache(maxsize=1024, ttl=1800))
def fetch_tokens():
    params = {
        "grant_type": "client_credentials",
        "client_id": get_config_by_name("MMI_CLIENT_ID"),
        "client_secret": get_config_by_name("MMI_CLIENT_SECRET"),
    }
    response = requests.post(f"{MMI_ENDPOINT}/security/oauth/token",params)
    json_response = response.json()
    return json_response["access_token"]



def get_auto_complete_by_query(query):
    params = {"query": query}
    headers = {"Authorization": f"Bearer {fetch_tokens()}"}
    response = requests.get(MMI_AUTO_COMPLETE_ENDPOINT,params=params,headers=headers)
    json_response = response.json()
    return json_response["suggestedLocations"]


def get_place_info_for_eloc(eloc):
    headers = {"Authorization": f"Bearer {fetch_tokens()}"}
    response = requests.get(f"{MMI_EXPLORE_API}/apis/O2O/entity/{eloc}",headers=headers)
    json_response = response.json()
    return json_response


