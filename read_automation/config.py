import json
import os


class Configuration:
    TPLINK_USERNAME = os.environ["TPLINK_USERNAME"]
    TPLINK_PASSWORD = os.environ["TPLINK_PASSWORD"]

    MIN_TEMPERATURE = int(os.environ.get("MIN_TEMPERATURE", "67"))
    MAX_TEMPERATURE = int(os.environ.get("MAX_TEMPERATURE", "72"))

    FUNHOUSE_TO_DEVICE_ALIAS = json.loads(os.environ["FUNHOUSE_TO_DEVICE_ALIAS"])
    FUNHOUSE_TO_PASSWORD = json.loads(os.environ["FUNHOUSE_TO_PASSWORD"])
