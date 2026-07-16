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
