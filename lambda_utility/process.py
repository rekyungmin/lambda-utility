from __future__ import annotations

__all__ = (
    "ProcessError",
    "optionize",
    "run_command",
)

import asyncio
import enum
import logging
import pathlib
import sys
from typing import Optional, Union

logger = logging.getLogger(__file__)


class ProcessError(Exception):
    def __init__(
        self,
        message: str,
        return_code: Optional[int] = None,
        stdin: Optional[str] = None,
        stdout: Optional[bytes] = None,
        stderr: Optional[bytes] = None,
    ):
        self.message = message
        self.return_code = return_code
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr


def optionize(*params: Union[str, tuple[str, Union[str, float, bool]]]) -> list[str]:
    """
    :example:
        >>> optionize("-y", ("-pix_fmt", "yuv420p"), ("-framerate", 29.97), ("-condition", True), ("-condition2", False), ("-condition3", None))
        ['-y', '-pix_fmt', 'yuv420p', '-framerate', '29.97', '-condition']
    """
    options = []
    for p in params:
        if isinstance(p, str):
            options.append(p)
        elif isinstance(p, (int, float, pathlib.PurePath)):
            options.append(str(p))
        elif isinstance(p, enum.Enum):
            options.append(str(p.value))
        else:
            if len(p) == 2 and (p[1] is None or p[1] is True or p[1] is False):
                if p[1] is True:
                    options.append(p[0])
                else:
                    continue
            else:
                options.extend(str(value) for value in p)
    return options


async def run_command(command: str, *params: str) -> tuple[bytes, bytes]:
    logger.debug("[Subprocess] run: '%s'", " ".join([command, *params]))
    if sys.version_info < (3, 10):
        loop = asyncio.get_running_loop()
        proc = await asyncio.create_subprocess_exec(
            command,
            *params,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            loop=loop,
        )
    else:
        proc = await asyncio.create_subprocess_exec(
            command,
            *params,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise ProcessError(
            "Encoding failed",
            proc.returncode,
            " ".join([command, *params]),
            stdout,
            stderr,
        )

    logger.debug("[Subprocess] stdout %s", stdout)
    logger.debug("[Subprocess] stderr %s", stderr)

    return stdout, stderr
