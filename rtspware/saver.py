from rtspware.subprocessutils import SubprocessUtils


class VideoSaver:
    async def save(
        self,
        url: str,
        username: str,
        password: str
    ) -> None:
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
