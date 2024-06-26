import argparse
import asyncio
from datetime import datetime
from pathlib import Path
import time
from PIL import Image

import cv2

from rtsp.saver import VideoSaver

RUN_ACTIONS = [
    "save",
]

SAVE_ACTION = [
    "video",
    "frame"
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

def show_video(url: str):
    cap = cv2.VideoCapture(url)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"({datetime.now().strftime("%H:%M:%S")}) show img")
            cv2.imshow("frame", frame)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser()
    action_subparsers = parser.add_subparsers(dest="action", required=True, )

    save_action_parser = action_subparsers.add_parser("save")

    save_action_subparsers = save_action_parser.add_subparsers(dest="save_action")

    video_save_parser = save_action_subparsers.add_parser("video")
    video_save_parser.add_argument("url", type=str)
    video_save_parser.add_argument(
        "--creds",
        type=str,
        dest="creds",
        required=True,
        help="creds in format <username>:<password>")

    frame_save_parser = save_action_subparsers.add_parser("frame")
    frame_save_parser.add_argument("url", type=str)
    frame_save_parser.add_argument(
        "-o --out", type=Path, dest="out", default=Path("var/frame.png"))
    frame_save_parser.add_argument(
        "--delay", type=float, dest="delay", default=1.0)

    args = parser.parse_args()

    match args.action:
        case "save":
            match args.save_action:
                case "video":
                    url = args.url
                    username, password = args.creds.split(":")
                    asyncio.run(VideoSaver().save(url, username, password))
                case "frame":
                    save_frame(args.url, args.out, args.delay)

if __name__ == "__main__":
    main()
