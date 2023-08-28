import argparse
import asyncio

from rtspware.saver import VideoSaver


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("--creds", type=str, dest="creds", required=True)

    namespace = parser.parse_args()

    url = namespace.url
    username, password = namespace.creds.split(" ")

    asyncio.run(VideoSaver().save(url, username, password))


if __name__ == "__main__":
    main()
