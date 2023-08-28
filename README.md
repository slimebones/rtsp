# RTSPWare

Some helper tools around RTSP protocol.

## Installation

For all methods, firstly install the project via PIP:
```bash
pip install rtspware
```

### Save a video from stream

You need to install [openRTSP](http://www.live555.com/openRTSP/), for example
for Arch Linux it is available under `live-media` library:
```bash
sudo pacman -S live-media
openRTSP --help
```

## Usage

### Save a video from stream

Basic call to save a video from RTSP stream to current directory with default
configuration:
```bash
rtspware <url> --creds "<username> <password>"
```

This will save incoming RTSP stream into mp4 files, with creating a new file
each hour.
