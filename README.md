# Splayer

Splayer is a thin CLI wrapper around Spotipy for controlling Spotify playback and playlists from the terminal.

## Installation

1. Install Python 3.10+.
2. Clone this repository:

```bash
git clone https://github.com/chirick86/splayer.git
cd splayer
```

1. Install Splayer (with dependencies):

```bash
pip install .
```

1. Check that the command is available:

```bash
splayer --help
```

## Standard Help Output

### `splayer --help`

```text
usage: splayer [-h] [--version]
               {play,pause,toggle,next,n,previous,prev,vol,v,auth,a,search,s,list,l,queue,q,status,info,i,device,d} ...

Spotify command line player

positional arguments:
  {play,pause,toggle,next,n,previous,prev,vol,v,auth,a,search,s,list,l,queue,q,status,info,i,device,d}
    play                Start playback
    pause               Pause playback
    toggle              Toggle playback
    next (n)            Next track
    previous (prev)     Previous track
    vol (v)             Volume control
    auth (a)            Spotify authentication
    search (s)          Search Spotify catalog
    list (l)            Playlist operations
    queue (q)           Queue control
    status (info, i)    Show current Spotify status
    device (d)          Device management

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Tip: run 'splayer <command> -h' to see help for any command.
Playlist help examples: 'splayer list -h' or 'splayer list --help'
```

### `splayer list --help`

```text
usage: splayer list [-h] [--new NAME | --default PLAYLIST | --add QUERY |
                    --tracks PLAYLIST | --add-current PLAYLIST |
                    --add-track PLAYLIST TRACK_REF]
                    [playlist]

positional arguments:
  playlist              Play playlist by index, name, or URI when no option is used

options:
  -h, --help            show this help message and exit
  --new NAME            Create a private playlist
  --default PLAYLIST    Set default playlist by index, name, or URI
  --add QUERY           Add track(s) by name, URL, or URI; supports: splayer list <playlist> --add <query>
  --tracks PLAYLIST     Show tracks in a playlist by index, name, or URI
  --add-current PLAYLIST
                        Add the current track to a playlist
  --add-track PLAYLIST TRACK_REF
                        Add a track by name, URL, or URI to a playlist

Examples:
  splayer list BEST
  splayer list -h
  splayer list --help
```
