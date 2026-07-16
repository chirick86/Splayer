from spotipy.oauth2 import SpotifyOAuth

from .config import TOKEN_FILE, load_config, save_config, ensure_dir


SCOPES = [
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "playlist-read-private",
    "playlist-modify-private",
    "playlist-modify-public"
]


def setup(client_id, client_secret, redirect_uri):
    save_config({
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    })


def get_auth():

    config = load_config()

    if not config:
        raise Exception(
            "Spotify credentials not configured. Run: splayer auth"
        )

    ensure_dir()

    return SpotifyOAuth(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        redirect_uri=config["redirect_uri"],
        scope=" ".join(SCOPES),
        cache_path=TOKEN_FILE
    )


def authenticate():

    auth = get_auth()

    token = auth.get_access_token(
        as_dict=False
    )

    return token