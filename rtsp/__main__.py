import argparse
import climage
import asyncio
from datetime import datetime
from pathlib import Path
import time
from PIL import Image

import cv2
from pykit.res import Res

from rtsp.saver import VideoSaver

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

def save_frame(url: str, out: Path, period: float):
    cap = cv2.VideoCapture(url)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"({datetime.now().strftime("%H:%M:%S")}) save img to {out}")
            Image.fromarray(frame, "RGB").save(out)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break
        if period > 0.0:
            time.sleep(period)
    cap.release()
    cv2.destroyAllWindows()

def show_window_frame(url: str, period: float):
    cap = cv2.VideoCapture(url)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"({datetime.now().strftime("%H:%M:%S")}) show frame")
            cv2.imshow("frame", frame)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break
        if period > 0.0:
            time.sleep(period)
    cap.release()
    cv2.destroyAllWindows()

def show_console_frame(url: str, period: float):
    cap = cv2.VideoCapture(url)
    last_process_time = 0.0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret and time.time() - last_process_time:
            print(f"({datetime.now().strftime("%H:%M:%S")}) show frame")
            img = Image.fromarray(frame, "RGB")
            console_out = climage.convert_pil(img, is_unicode=True)
            print(console_out)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break
        if period > 0.0:
            time.sleep(period)
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
    parser = argparse.ArgumentParser()
    action_subparsers = parser.add_subparsers(dest="action", required=True, )

    save_action_parser = action_subparsers.add_parser("save")
    _add_save_parsers(save_action_parser)
    show_action_parser = action_subparsers.add_parser("show")
    _add_show_parsers(show_action_parser)

    args = parser.parse_args()

    match args.action:
        case "save":
            match args.save_action:
                case "video":
                    url = args.url
                    username, password = args.creds.split(":")
                    await VideoSaver().save(url, username, password)
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
