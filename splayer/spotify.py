import spotipy
from spotipy.exceptions import SpotifyException
import subprocess
import time
from pathlib import Path
from .auth import get_auth
from .config import load_config


def start_spotify():
    subprocess.Popen(["spotify"])
    time.sleep(1)


def ensure_device():
    device = get_target_device()
    if device in [d["id"] for d in get_devices()]:
        return device
    start_spotify()
    for _ in range(5):
        time.sleep(2)
        if device in [d["id"] for d in get_devices()]:
            return device
    return None


def spotify_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except SpotifyException as e:
        if e.http_status == 404:
            if "NO_ACTIVE_DEVICE" in str(e):
                print("No active Spotify device found")
                print("Run Spotify or set device with: splayer device --force")
                return None
        if e.http_status == 403:
            print("Spotify error: forbidden request")
            print("If this is a playlist action, re-run `splayer auth` to refresh scopes or clear the cached token in %APPDATA%\\splayer\\token.cache")
            return None
        print(f"Spotify error: {e}")
        return None


def get_client():
    return spotipy.Spotify(auth_manager=get_auth())


def get_forced_device():
    config = load_config()
    return config.get("forced_device_id")


def get_devices():
    sp = get_client()
    return sp.devices()["devices"]


def get_active_device():
    for device in get_devices():
        if device["is_active"]:
            return device

    return None


def get_target_device():
    forced = get_forced_device()
    if forced:
        return forced
    active = get_active_device()
    if active:
        return active["id"]
    return None


def transfer_playback():
    device_id = get_target_device()
    if device_id:
        get_client().transfer_playback(device_id=device_id, force_play=False)
    return device_id
