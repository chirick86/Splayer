from .spotify import get_client
from .config import load_config, update_config


def list_devices():

    sp = get_client()

    devices = sp.devices()["devices"]

    return devices


def get_current():

    devices = list_devices()

    for device in devices:
        if device["is_active"]:
            return device

    return None


def get_last():

    config = load_config()

    device_id = config.get("forced_device_id")

    if not device_id:
        return None

    sp = get_client()

    for device in sp.devices()["devices"]:
        if device["id"] == device_id:
            return device

    return None


def force_current():

    device = get_current()

    if not device:
        raise Exception("No active device")

    update_config({
        "forced_device_id": device["id"]
    })

    return device