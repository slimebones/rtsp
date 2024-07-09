from pathlib import Path
import shutil
import tempfile
import time

from rtsp.rotation import Rotation

TEXT_ABOVE_1KB = """
MIT License

Copyright (c) 2024 Alexander Ryzhov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

TEXT_BELOW_1KB = "hello"

def test_rotation():
    target_dir = Path(tempfile.gettempdir(), "test_rotation")
    target_dir.mkdir(parents=True, exist_ok=True)
    rotation = None

    try:
        rotation = Rotation(
            target_dir,
            "2KB",
            "real*")
        rotation.start()

        with Path(target_dir, "real1.txt").open("w+") as f:
            f.write(TEXT_ABOVE_1KB)
        time.sleep(1)
        assert len(list(target_dir.glob("real*"))) == 1

        with Path(target_dir, "real2.txt").open("w+") as f:
            f.write(TEXT_BELOW_1KB)
        time.sleep(1)
        assert len(list(target_dir.glob("real*"))) == 2

        with Path(target_dir, "real3.txt").open("w+") as f:
            f.write(TEXT_ABOVE_1KB)
        time.sleep(1)
        assert len(list(target_dir.glob("real*"))) == 2
        for p in target_dir.glob("real*"):
            # assert first file "real1" were deleted
            assert p.stem in ["real2", "real3"]
    finally:
        if rotation is not None:
            rotation.stop()
        if target_dir.is_dir():
            shutil.rmtree(target_dir)
