# rtsp

Tools to work with RTSP streams.

## Installation

You may need `poetry`:
```bash
poetry install
```

## Usage

```bash
poetry run python -m rtsp <command>
```

Save a video (legacy, soon to be changed):
```bash
poetry run python -m rtsp save video <url> --creds <username>:<password>
```
videos are saved to the current working directory.

Save a frame:
```bash
poetry run python -m rtsp save frame <url> -o <out_path> -p <delay>
```
overwrites frame image at path (soon to be added to collect images).

Show low-res image to console:
```bash
poetry run python -m rtsp show console <url> -p <delay>
```
