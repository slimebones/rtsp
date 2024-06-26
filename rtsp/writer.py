import contextlib
from threading import Thread
import cv2


class VideoWriter:
    """

    References:
        - https://stackoverflow.com/a/55150662
    """
    def __init__(self, url: str):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(url)

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc(*"X264")  # type: ignore
        self.output_video = cv2.VideoWriter(
            "output.mkv",
            self.codec,
            30,
            (self.frame_width, self.frame_height)
        )

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        # Display frames in main program
        if self.status:
            cv2.imshow("frame", self.frame)

        # Press Q on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord("q"):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # Save obtained frame into video output file
        self.output_video.write(self.frame)


if __name__ == "__main__":

    # TODO(ryzhovalex):
    #   to support h264 codec the ffmpeg and python-opencv needs rebuilding, so
    #   i've switched to openRTSP use

    url: str = "pleasedefine"
    video_stream_widget = VideoWriter(url)
    while True:
        with contextlib.suppress(AttributeError):
            # video_stream_widget.show_frame()
            video_stream_widget.save_frame()
