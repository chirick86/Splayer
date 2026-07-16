import re

from .spotify import get_client, spotify_call


_SPOTIFY_URI_RE = re.compile(r"^spotify:(artist|album|track):([A-Za-z0-9]+)$")
_SPOTIFY_URL_RE = re.compile(
    r"^(?:https?://)?open\.spotify\.com/(?:intl-[a-z]{2}/)?(artist|album|track)/([A-Za-z0-9]+)(?:/)?(?:[?#].*)?$",
    re.IGNORECASE,
)


def parse_spotify_reference(reference):
    value = reference.strip()

    uri_match = _SPOTIFY_URI_RE.match(value)
    if uri_match:
        entity_type, entity_id = uri_match.groups()
        return {
            "type": entity_type,
            "id": entity_id,
            "uri": value,
            "source": "uri",
        }

    url_match = _SPOTIFY_URL_RE.match(value)
    if url_match:
        entity_type, entity_id = url_match.groups()
        return {
            "type": entity_type,
            "id": entity_id,
            "uri": f"spotify:{entity_type}:{entity_id}",
            "source": "url",
        }

    return None


def ensure_spotify_uri(reference, allowed_types=None):
    parsed = parse_spotify_reference(reference)
    if not parsed or parsed["source"] != "uri":
        raise ValueError("Only a Spotify URI is accepted")

    if allowed_types and parsed["type"] not in allowed_types:
        allowed = ", ".join(allowed_types)
        raise ValueError(f"Only Spotify {allowed} URI is accepted")

    return parsed["uri"]


def _search_items(entity_type, query, sp=None, limit=10):
    sp = sp or get_client()
    result = spotify_call(sp.search, q=query, type=entity_type, limit=limit)
    if not result:
        return []

    bucket = result.get(f"{entity_type}s", {})
    return bucket.get("items", [])


def _choose_best_match(items, query):
    if not items:
        return None

    query_lower = query.strip().lower()
    for item in items:
        if item.get("name", "").strip().lower() == query_lower:
            return item

    return items[0]


def _collect_album_track_uris(album_uri, sp=None):
    sp = sp or get_client()
    parsed = parse_spotify_reference(album_uri)
    if not parsed or parsed["type"] != "album":
        raise ValueError("Expected Spotify album URI or URL")

    uris = []
    results = spotify_call(sp.album_tracks, album_uri, limit=50, offset=0)

    while results:
        for item in results.get("items", []):
            uri = item.get("uri")
            if uri:
                uris.append(uri)

        if not results.get("next"):
            break

        results = spotify_call(sp.next, results)

    return uris


def _collect_artist_track_uris(artist_uri, sp=None, limit=10):
    sp = sp or get_client()
    artist = _fetch_exact_entity(artist_uri, "artist", sp=sp)
    if not artist:
        return []

    results = _search_items(
        "track", f'artist:"{artist["name"]}"', sp=sp, limit=limit)
    uris = []
    seen = set()

    for track in results:
        uri = track.get("uri")
        if uri and uri not in seen:
            seen.add(uri)
            uris.append(uri)

    return uris


def resolve_track_uris_for_add(reference, sp=None, artist_limit=10):
    sp = sp or get_client()
    parsed = parse_spotify_reference(reference)

    if parsed:
        if parsed["type"] == "track":
            return [parsed["uri"]]
        if parsed["type"] == "album":
            uris = _collect_album_track_uris(parsed["uri"], sp=sp)
            if not uris:
                raise ValueError("No tracks found in album")
            return uris
        if parsed["type"] == "artist":
            uris = _collect_artist_track_uris(
                parsed["uri"], sp=sp, limit=artist_limit)
            if not uris:
                raise ValueError("No tracks found for artist")
            return uris

    tracks = _search_items("track", reference, sp=sp, limit=1)
    if not tracks:
        raise ValueError(f"No Spotify track found for: {reference}")

    uri = tracks[0].get("uri")
    if not uri:
        raise ValueError("Found track has no URI")

    return [uri]


def print_default_search(query):
    sp = get_client()
    result = spotify_call(sp.search, q=query,
                          type="artist,album,track", limit=10)

    if not result:
        print("No results found")
        return

    artists = result.get("artists", {}).get("items", [])
    albums = result.get("albums", {}).get("items", [])
    tracks = result.get("tracks", {}).get("items", [])

    if artists:
        print("Artists:")
        for index, artist in enumerate(artists, 1):
            print(f'{index}. {artist["name"]} | URI: {artist["uri"]}')

    if albums:
        if artists:
            print()
        print("Albums:")
        for index, album in enumerate(albums, 1):
            artist_names = ", ".join(artist["name"]
                                     for artist in album.get("artists", []))
            print(
                f'{index}. {album["name"]} - {artist_names} | URI: {album["uri"]}')

    if tracks:
        if artists or albums:
            print()
        print("Tracks:")
        for index, track in enumerate(tracks, 1):
            artist_names = ", ".join(artist["name"]
                                     for artist in track.get("artists", []))
            print(
                f'{index}. {track["name"]} - {artist_names} | URI: {track["uri"]}')

    if not artists and not albums and not tracks:
        print("No results found")


def resolve_spotify_uri(reference, entity_type, sp=None):
    parsed = parse_spotify_reference(reference)
    if parsed:
        if parsed["type"] != entity_type:
            raise ValueError(
                f"Expected a Spotify {entity_type} URI, URL, or name")
        return parsed["uri"]

    items = _search_items(entity_type, reference, sp=sp)
    match = _choose_best_match(items, reference)
    if not match:
        raise ValueError(f"No Spotify {entity_type} found for: {reference}")

    return match["uri"]


def _fetch_exact_entity(reference, entity_type, sp=None):
    parsed = parse_spotify_reference(reference)
    if not parsed or parsed["type"] != entity_type:
        raise ValueError(
            f"Expected a Spotify {entity_type} URI, URL, or name")

    sp = sp or get_client()
    getter = {
        "artist": sp.artist,
        "album": sp.album,
        "track": sp.track,
    }[entity_type]
    return spotify_call(getter, parsed["uri"])


def _format_duration(duration_ms):
    if duration_ms is None:
        return "unknown"

    total_seconds = int(duration_ms) // 1000
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def print_artist_search(reference):
    sp = get_client()
    parsed = parse_spotify_reference(reference)

    if parsed and parsed["type"] == "artist":
        artist = _fetch_exact_entity(reference, "artist", sp=sp)
        if not artist:
            print("No artist found")
            return

        followers = artist.get("followers", {})
        followers_total = followers.get("total", "unknown")

        print(f'Artist: {artist["name"]}')
        print(f'URI: {artist["uri"]}')
        print(f'Followers: {followers_total}')
        print(f'Popularity: {artist.get("popularity", "unknown")}')
        genres = artist.get("genres", [])
        if genres:
            print("Genres:", ", ".join(genres))

        tracks = artist.get("tracks", {}).get("items", [])
        if tracks:
            print("Tracks:")
            for index, track in enumerate(tracks, 1):
                artists = ", ".join(a["name"]
                                    for a in track.get("artists", []))
                print(
                    f'{index}. {track["name"]} - {artists} | URI: {track["uri"]}')
        else:
            print("Tracks: not provided by artist endpoint")
        return

    items = _search_items("artist", reference, sp=sp)
    if not items:
        print("No artists found")
        return

    print(f'Artists for "{reference}":')
    for index, artist in enumerate(items, 1):
        print(f'{index}. {artist["name"]} | URI: {artist["uri"]}')


def print_album_search(reference):
    sp = get_client()
    parsed = parse_spotify_reference(reference)

    if parsed and parsed["type"] == "album":
        album = _fetch_exact_entity(reference, "album", sp=sp)
        if not album:
            print("No album found")
            return

        artists = ", ".join(artist["name"]
                            for artist in album.get("artists", []))
        print(f'Album: {album["name"]}')
        print(f'URI: {album["uri"]}')
        print(f'Artists: {artists}')
        print(f'Release date: {album.get("release_date", "unknown")}')
        print(f'Total tracks: {album.get("total_tracks", "unknown")}')

        track_items = album.get("tracks", {}).get("items", [])
        if track_items:
            print("Tracks:")
            for index, track in enumerate(track_items, 1):
                artists = ", ".join(a["name"]
                                    for a in track.get("artists", []))
                print(
                    f'{index}. {track["name"]} - {artists} | URI: {track["uri"]}')

        if album.get("tracks", {}).get("next"):
            print(
                "Note: album has more than 50 tracks; showing first page only to keep a single request")
        return

    items = _search_items("album", reference, sp=sp)
    if not items:
        print("No albums found")
        return

    print(f'Albums for "{reference}":')
    for index, album in enumerate(items, 1):
        artists = ", ".join(artist["name"]
                            for artist in album.get("artists", []))
        print(f'{index}. {album["name"]} - {artists} | URI: {album["uri"]}')


def print_track_search(reference):
    sp = get_client()
    parsed = parse_spotify_reference(reference)

    if parsed and parsed["type"] == "track":
        track = _fetch_exact_entity(reference, "track", sp=sp)
        if not track:
            print("No track found")
            return

        artists = ", ".join(artist["name"]
                            for artist in track.get("artists", []))
        album = track.get("album", {})
        print(f'Track: {track["name"]}')
        print(f'URI: {track["uri"]}')
        print(f'Artists: {artists}')
        print(f'Album: {album.get("name", "unknown")}')
        print(f'Duration: {_format_duration(track.get("duration_ms"))}')
        print(f'Popularity: {track.get("popularity", "unknown")}')
        return

    items = _search_items("track", reference, sp=sp)
    if not items:
        print("No tracks found")
        return

    print(f'Tracks for "{reference}":')
    for index, track in enumerate(items, 1):
        artists = ", ".join(artist["name"]
                            for artist in track.get("artists", []))
        album = track.get("album", {})
        print(
            f'{index}. {track["name"]} - {artists} ({album.get("name", "unknown")}) | URI: {track["uri"]}')


def print_uri_lookup(reference):
    parsed = parse_spotify_reference(reference)
    if not parsed or parsed["source"] != "uri":
        raise ValueError("Only a Spotify URI is accepted")

    if parsed["type"] == "artist":
        print_artist_search(parsed["uri"])
    elif parsed["type"] == "album":
        print_album_search(parsed["uri"])
    elif parsed["type"] == "track":
        print_track_search(parsed["uri"])
