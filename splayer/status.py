from .spotify import get_client, get_forced_device
from .playlist import get_current_playlist, get_playlist_info


def get_status():
    sp = get_client()

    playback = sp.current_playback()

    if not playback:
        return {
            "playing": False,
            "device": None,
            "track": None,
            "playlist": None
        }

    item = playback.get("item")

    track = None

    if item:
        track = {
            "name": item["name"],
            "artist": ", ".join(
                artist["name"]
                for artist in item["artists"]
            ),
            "album": item["album"]["name"],
            "uri": item["uri"],
            "duration": item["duration_ms"],
            "progress": playback["progress_ms"]
        }

    current_playlist = get_current_playlist(playback)

    if current_playlist:
        current_playlist = get_playlist_info(current_playlist["uri"], sp)

    return {
        "playing": playback["is_playing"],
        "device": playback["device"],
        "track": track,
        "volume": playback["device"]["volume_percent"],
        "playlist": current_playlist
    }


def print_status():

    status = get_status()

    print(
        "Playing:",
        "Yes" if status["playing"] else "No"
    )

    if status["device"]:
        print("Device:", status["device"]["name"])
        print("Type:", status["device"]["type"])
        print("Volume:", f'{status["volume"]}%')
    else:
        print("Device: None")

    if status["track"]:
        track = status["track"]
        print("Track:",f'{track["artist"]} - {track["name"]}')
        print(f'Track URI: {track["uri"]}')
        print("Album:",track["album"])
    else:
        print("Track: None")

    if status["playlist"]:
        playlist = status["playlist"]
        print("Playlist:", playlist["name"])
        print(f'Playlist URI: {playlist["uri"]}')
    else:
        print("Playlist: None")

    forced = get_forced_device()

    if forced:
        print("Forced device:", forced)
