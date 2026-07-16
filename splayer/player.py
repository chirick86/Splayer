from .spotify import get_client, ensure_device, spotify_call


def play():
    sp = get_client()
    device = ensure_device()
    if device:
        spotify_call(sp.start_playback, device_id=device)
    else:
        spotify_call(sp.start_playback)


def pause():
    sp = get_client()
    device = ensure_device()
    if device:
        spotify_call(sp.pause_playback, device_id=device)
    else:
        spotify_call(sp.pause_playback)


def toggle():
    sp = get_client()
    playback = sp.current_playback()
    if playback and playback["is_playing"]:
        pause()
    else:
        play()


def next_track():
    sp = get_client()
    device = ensure_device()
    if device:
        spotify_call(sp.next_track, device_id=device)
    else:
        spotify_call(sp.next_track)


def previous_track():
    sp = get_client()
    device = ensure_device()
    if device:
        spotify_call(sp.previous_track, device_id=device)
    else:
        spotify_call(sp.previous_track)


def set_volume(value):
    sp = get_client()
    device = ensure_device()
    spotify_call(sp.volume, value, device_id=device)


def change_volume(delta):
    sp = get_client()
    playback = sp.current_playback()

    if not playback or not playback["device"]:
        print("No active device")
        return

    set_volume(max(0, min(100, playback["device"]["volume_percent"] + delta)))


def print_volume():
    sp = get_client()
    playback = sp.current_playback()

    if not playback or not playback["device"]:
        print("No active device")
        return

    print(f'Volume: {playback["device"]["volume_percent"]}%')
