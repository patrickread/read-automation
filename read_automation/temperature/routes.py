import json
from . import temperature_blueprint
from read_automation.config import Configuration
from flask import request
from read_automation.utils.kasa import authenticate, get_device_by_alias, get_devices_list, set_device_status


@temperature_blueprint.route("/temperature", methods=["POST"])
def post_temp():
    input_device_name = __get_input_device_name(request)
    device_password = Configuration.FUNHOUSE_TO_PASSWORD.get(input_device_name)
    input_password = __get_password(request)

    if device_password is None or device_password != input_password:
        return {
            "error": "Input device name and password combination is invalid"
        }

    temperature = __get_temperature(request)

    token = authenticate(Configuration.TPLINK_USERNAME, Configuration.TPLINK_PASSWORD)
    devices = get_devices_list(token)
    device_alias = Configuration.FUNHOUSE_TO_DEVICE_ALIAS.get(input_device_name)

    if device_alias is None:
        return {
            "error": "Device alias not found"
        }

    device = get_device_by_alias(devices, device_alias)
    if device is None:
        return {
            "error": "Kasas device not found"
        }

    new_state = None
    if temperature < Configuration.MIN_TEMPERATURE:
        new_state = True
    elif temperature >= Configuration.MAX_TEMPERATURE:
        new_state = False

    if new_state is not None:
        print(json.dumps({
            "severity": "INFO",
            "message": (
                f"Updating device state to {new_state} for temperature: {temperature}"
            )
        }))
        set_device_status(token=token, device=device, turn_on=new_state)

    return {
        "new_state": new_state
    }


def __get_temperature(request) -> int:
    return __get_input_property(request, "temperature", "70")

def __get_input_device_name(request) -> str:
    return __get_input_property(request, "input_device_name", "funhouse")

def __get_password(request) -> str:
    return __get_input_property(request, "password")


def __get_input_property(request, property_key: str, default: str = None) -> str:
    request_json = request.get_json()
    if request.args and property_key in request.args:
        return request.args[property_key]
    elif request_json and property_key in request_json:
        return request_json[property_key]
    else:
        return default
