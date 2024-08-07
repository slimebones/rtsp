"""
For most methods, we have to read VideoCapture constantly, but take an action
with the frame only in certain periods of time. So we use last_process_time
variable with conditions.
"""
import argparse
import sys
import climage
import asyncio
from datetime import datetime
from pathlib import Path
import time
from PIL import Image

import cv2
from loguru import logger
from pykit.log import log
from pykit.res import Res

from rtsp.subprocess_ext import SubprocessUtils

RUN_ACTIONS = [
    "save",
    "show"
]

SAVE_ACTION = [
    "video",
    "frame"
]

SHOW_ACTION = [
    "window",
    "console"
]

async def _save_video(url: str, username: str, password: str, rotation: str):
    # https://superuser.com/a/921385
    cmdargs: list[str] = [
        "openRTSP",
        # input buffer of 10 MB
        "-B 10000000",
        # output buffer 10MB (to file)
        "-b 10000000",
        # produce files in mp4 format
        "-4",
        # prefix output filenames with this text
        "-F main",
        # period to start a new output file
        "-P 3600",
        # request camera end stream over TCP, not UDP
        "-t",
        # username and password expected by camera
        f"-u {username} {password}",
        # frame rate set to 30
        "-f 30",
        # camera's RTSP URL
        url
    ]
    await SubprocessUtils.call(" ".join(cmdargs))

def save_frame(url: str, out: Path, period: float):
    cap = cv2.VideoCapture(url)
    last_process_time = 0.0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret and time.time() - last_process_time > period:
            log.info(f"({datetime.now().strftime('%H:%M:%S')}) save img to {out}")
            last_process_time = time.time()
            Image.fromarray(frame, "RGB").save(out)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def show_window_frame(url: str, period: float):
    cap = cv2.VideoCapture(url)
    last_process_time = 0.0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret and time.time() - last_process_time > period:
            log.info(f"({datetime.now().strftime('%H:%M:%S')}) show frame")
            last_process_time = time.time()
            cv2.imshow("frame", frame)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def show_console_frame(url: str, period: float):
    cap = cv2.VideoCapture(url)
    last_process_time = 0.0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret and time.time() - last_process_time > period:
            log.info(
                f"({time.strftime('%H:%M:%S', time.gmtime())}) show frame")
            last_process_time = time.time()
            img = Image.fromarray(frame, "RGB")
            console_out = climage.convert_pil(img, is_unicode=True)
            print(console_out)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break
    cap.release()

def _add_save_parsers(parser: argparse.ArgumentParser):
    subparser = parser.add_subparsers(dest="save_action")

    video = subparser.add_parser("video")
    video.add_argument("url", type=str)
    video.add_argument(
        "--creds",
        type=str,
        dest="creds",
        required=True,
        help="creds in format <username>:<password>")
    video.add_argument(
        "--rotation",
        type=str,
        dest="rotation",
        default="inf",
        help=
            "how often to delete accumulated data. For now only MB"
            " measurement is supported, e.g. \"10MB\". \"inf\" means"
            " no rotation is made")

    frame = subparser.add_parser("frame")
    frame.add_argument("url", type=str)
    frame.add_argument(
        "-o --out", type=Path, dest="out", default=Path("var/frame.png"))
    frame.add_argument(
        "-p --period", type=float, dest="period", default=1.0)

def _add_show_parsers(parser: argparse.ArgumentParser):
    subparser = parser.add_subparsers(dest="show_action")

    window = subparser.add_parser("window")
    window.add_argument("url", type=str)
    window.add_argument(
        "-p --period", type=float, dest="period", default=1.0)

    console = subparser.add_parser("console")
    console.add_argument("url", type=str)
    console.add_argument(
        "-p --period", type=float, dest="period", default=1.0)

async def main():
    logger.remove(0)
    logger.add(
        sys.stderr,
        format="{message}",
        colorize=True,
        level="DEBUG")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", action="store_true", dest="verbosity", default=False)
    action_subparsers = parser.add_subparsers(dest="action", required=True, )

    save_action_parser = action_subparsers.add_parser("save")
    _add_save_parsers(save_action_parser)
    show_action_parser = action_subparsers.add_parser("show")
    _add_show_parsers(show_action_parser)

    args = parser.parse_args()
    log.std_verbosity = 1 if args.verbosity else 0

    match args.action:
        case "save":
            match args.save_action:
                case "video":
                    url = args.url
                    username, password = args.creds.split(":")
                    rotation = args.rotation
                    await _save_video(url, username, password, rotation)
                case "frame":
                    save_frame(args.url, args.out, args.period)
        case "show":
            match args.show_action:
                case "window":
                    show_window_frame(args.url, args.period)
                case "console":
                    show_console_frame(args.url, args.period)

if __name__ == "__main__":
    asyncio.run(main())
