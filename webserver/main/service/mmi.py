import json
import logging
import os
import random
import requests
from cachetools import cached, LRUCache, TTLCache
from flask_restplus import abort
from retry import retry

from main.config import get_config_by_name

MMI_ENDPOINT = "https://outpost.mapmyindia.com/api"
MMI_AUTO_COMPLETE_ENDPOINT = "https://atlas.mapmyindia.com/api/places/search/json"
MMI_EXPLORE_API = "https://explore.mappls.com"
MMI_APIS_BASE_PATH = "https://apis.mapmyindia.com/advancedmaps/v1"
MMI_ATLAS_ENDPOINT = "https://atlas.mappls.com/api/places/geocode"


@cached(TTLCache(maxsize=1, ttl=600))
def fetch_tokens(random=1):
    params = {
        "grant_type": "client_credentials",
        "client_id": get_config_by_name("MMI_CLIENT_ID"),
        "client_secret": get_config_by_name("MMI_CLIENT_SECRET"),
    }
    response = requests.post(f"{MMI_ENDPOINT}/security/oauth/token", params)
    if response.status_code == 200:
        json_response = response.json()
        return json_response["access_token"]
    else:
        print(f"status code {response.content}")
        abort(429, "unable to fetch access tokens")


@retry(tries=4)
def get_auto_complete_by_query(query):
    params = {"query": query}
    headers = {"Authorization": f"Bearer {fetch_tokens(random=random.randint(1, 3))}"}
    response = requests.get(MMI_AUTO_COMPLETE_ENDPOINT, params=params, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        return json_response.get("suggestedLocations", {})
    else:
        print(f"status code {response.content}")
        print("failed fetching fresh token again")
        raise Exception()


def get_place_info_for_eloc(eloc):
    headers = {"Authorization": f"Bearer {fetch_tokens()}"}
    response = requests.get(f"{MMI_EXPLORE_API}/apis/O2O/entity/{eloc}", headers=headers)
    json_response = response.json()
    return json_response


def get_place_info_for_latlong(lat, long):
    params = {"lat": lat, "lng": long}
    response = requests.get(f"{MMI_APIS_BASE_PATH}/{get_config_by_name('MMI_ADVANCE_API_KEY')}/rev_geocode",
                            params=params)
    response = response.json()
    return response


def get_pin_info(pincode):
    headers = {"Authorization": f"Bearer {fetch_tokens()}"}
    params = {"address": pincode, "podFilter": "pincode"}
    response = requests.get(f"{MMI_ATLAS_ENDPOINT}",
                            headers=headers, params=params)
    response = response.json()
    return response
