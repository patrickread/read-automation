from __future__ import annotations

import requests
from typing import Optional


BASE_URL = "https://wap.tplinkcloud.com"
BASE_HEADERS = {
    "Content-Type": "application/json",
}


def authenticate(username: str, password: str) -> str:
    payload = {
        "method": "login",
        "params": {
            "appType": "Kasa_Android",
            "cloudUserName": username,
            "cloudPassword": password,
            "terminalUUID": "a858b594-3068-45c5-9099-fcadbbd582de"
        }
    }

    response = requests.request(
        "POST", f"{BASE_URL}/", headers=BASE_HEADERS, json=payload
    )

    json_response = response.json()
    return json_response["result"]["token"]


def get_devices_list(token: str) -> list[dict]:
    url = f"{BASE_URL}?token={token}"

    response = requests.request(
        "POST",
        url,
        headers=BASE_HEADERS,
        json={
            "method": "getDeviceList"
        }
    )
    return response.json()["result"]["deviceList"]


def get_device_by_alias(devices_list: list[dict], alias: str) -> Optional[dict]:
    return next((device for device in devices_list if device["alias"] == alias), None)


def set_device_status(token: str, device: dict, turn_on: bool):
    url = f"{BASE_URL}?token={token}"

    device_id = device["deviceId"]
    new_request_data = (
        "{\"system\":{\"set_relay_state\":{\"state\": 1}}}"
         if turn_on
         else "{\"system\":{\"set_relay_state\":{\"state\": 0}}}"
    )
    payload = {
        "method": "passthrough",
        "params": {
            "deviceId": device_id,
            "requestData": new_request_data,
        }
    }

    response = requests.request("POST", url, headers=BASE_HEADERS, json=payload)
