import subprocess
from typing import Callable, Coroutine

from pydantic import BaseModel

CalledProcess = subprocess.Popen
NoneCoro = Coroutine[None, None, None]
PerLineFn = Callable[[CalledProcess, str], NoneCoro]


class Static:
    def __init__(self) -> None:
        raise NotImplementedError


class SubprocessPopenArgs(BaseModel):
    stdout: int = subprocess.PIPE
    text: bool = True
    shell: bool = True


class SubprocessCalledFns(BaseModel):
    per_line: PerLineFn | None = None
    keyboard_interrupt: Callable[[CalledProcess], NoneCoro] | None = None


class SubprocessUtils(Static):
    @staticmethod
    async def call(
        cmd: str,
        *,
        called_fns: SubprocessCalledFns | None = None,
        popen_args: SubprocessPopenArgs | None = None
    ) -> CalledProcess:
        """
        Opens a new process and iterates over it's output lines.

        If called_fns.keyboard_interrupt is specified, on KeyboardInterrupt
        error no process kill is performed, an error is not raised. The
        specified function is firstly called, then the process object is
        returned as it is. Otherwise (no such function is specified), the
        process is killed and the KeyboardInterrupt is raised.

        Args:
            cmd:
                String command to be executed.
            called_fns(optional):
                Specify which functions to be called during the process
                execution. No functions are called by default.
            popen_args(optional):
                Redefine args supplied to subprocess.Popen. Defaults to
                standard calling procedure. No recommended to be supplied in
                most cases.

        Returns:
            Finished Process, with any return code.

        Raises:
            KeyboardInterrupt:
                The execution of a process was interrupted by keyboard. The
                process will be automatically killed, unless
                CalledFns.keyboard_interrupt is specified.
        """
        popen_args = \
            popen_args if popen_args is not None else SubprocessPopenArgs()
        called_fns = \
            called_fns if called_fns is not None else SubprocessCalledFns()

        with subprocess.Popen(
            cmd,
            stdout=popen_args.stdout,
            text=popen_args.text,
            shell=popen_args.shell
        ) as process:
            try:
                if process.stdout is not None and called_fns.per_line:
                    for line in process.stdout:
                        await called_fns.per_line(process, line)
            except KeyboardInterrupt:
                if called_fns.keyboard_interrupt:
                    await called_fns.keyboard_interrupt(process)
                    return process
                process.kill()
                raise KeyboardInterrupt()

        return process
