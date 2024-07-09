import contextlib
import glob
from multiprocessing import Process
import os
from pathlib import Path
import shutil
import time
from typing import Iterable
from pykit.err import ValueErr
from pykit.proc import ProcGroup

class Rotation:
    """
    Manages deletion of files inside a dir according to some rule.
    """
    def __init__(self, target_dir: Path, rule: str, file_glob: str):
        self._target_dir = target_dir
        self._rule = rule
        self._file_glob = file_glob
        self._proc = None

    def start(self):
        self._proc = Process(
            target=self._proc__main,
            args=(
                self._target_dir,
                self._parse_rule_to_max_size(self._rule),
                self._file_glob))
        self._proc.start()

    def stop(self):
        if self._proc is not None and self._proc.is_alive:
            self._proc.terminate()

    def _parse_rule_to_max_size(self, rule: str) -> int:
        if rule.endswith("KB"):
            return int(rule.replace("KB", "")) * 1024
        if rule.endswith("MB"):
            return int(rule.replace("MB", "")) * 1024 * 1024
        if rule.endswith("GB"):
            return int(rule.replace("GB", "")) * 1024 * 1024 * 1024
        raise ValueErr(f"rule {rule} has incorrect format")

    @staticmethod
    def _proc__main(target_dir: Path, max_size: int, file_glob: str):
        print(f"start rotation of max size {max_size} for glob {file_glob}")
        while True:
            paths = Path(target_dir).glob(file_glob)
            total_size = 0
            oldest_path: tuple[float, Path] | None = None
            for path in paths:
                total_size += os.path.getsize(path)
                t = get_file_creation_or_modification_time(path)
                if oldest_path is None or t < oldest_path[0]:
                    oldest_path = (t, path)
            # don't remove if create/modify less than epsilon
            # for now is not set
            remove_time_epsilon = 0
            if (
                total_size >= max_size
                and oldest_path is not None
                and time.time() - oldest_path[0] > remove_time_epsilon):
                    print(f"remove {oldest_path}")
                    oldest_path[1].unlink()
            time.sleep(1)

def get_file_creation_or_modification_time(path: Path):
    """
    Returns creation time, if available, otherwise the time of most recent
    content modification.
    """
    stat = path.stat()
    try:
        return stat.st_birthtime
    except AttributeError:
        return stat.st_mtime
