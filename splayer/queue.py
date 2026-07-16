from .catalog import resolve_track_uris_for_add
from .spotify import get_client, get_target_device, spotify_call


def show_queue():
    sp = get_client()
    queue = sp.queue()

    current = queue.get("currently_playing")

    if current:
        print(f'Now: {current["artists"][0]["name"]} - {current["name"]}')
    else:
        print("Now: None")

    items = queue.get("queue", [])

    if not items:
        print("Queue is empty")
        return

    print("\nQueue:")

    for i, track in enumerate(items, 1):
        print(f'{i}. {track["artists"][0]["name"]} - {track["name"]}')


def add_queue(track_ref):
    sp = get_client()
    device = get_target_device()
    track_uris = resolve_track_uris_for_add(track_ref, sp=sp)

    for track_uri in track_uris:
        if device:
            spotify_call(sp.add_to_queue, track_uri, device_id=device)
        else:
            spotify_call(sp.add_to_queue, track_uri)

    print(f'Added {len(track_uris)} track(s) to queue')
