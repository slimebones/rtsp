import argparse
import asyncio

from rtspware.saver import VideoSaver


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--creds", type=str, dest="creds", required=True)

    namespace = parser.parse_args()

    username, password = namespace.creds.split(" ")

    asyncio.run(VideoSaver().save(username, password))


if __name__ == "__main__":
    main()
