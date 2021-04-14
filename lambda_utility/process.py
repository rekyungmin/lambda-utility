from __future__ import annotations

__all__ = (
    "ProcessError",
    "run_command",
)

import asyncio
import sys
import logging
from typing import Optional

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
