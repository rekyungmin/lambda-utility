from __future__ import annotations

__all__ = (
    "timeit_ctx_manager",
    "timeit_decorator",
)

import contextlib
import functools
import time
from typing import TypeVar, Any, cast, Optional, Callable


@contextlib.contextmanager
def timeit_ctx_manager(
    decimal_point_limit: Optional[int] = None, prefix: str = "", postfix: str = ""
):
    start = time.perf_counter()
    yield
    elapsed_time = time.perf_counter() - start
    if decimal_point_limit is None:
        print(prefix, elapsed_time, postfix, sep="")
    else:
        print(prefix, round(elapsed_time, decimal_point_limit), sep="")


F = TypeVar("F", bound=Callable[..., Any])


def timeit_decorator(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print(f"{func.__name__!r} function: {elapsed_time:.4f} seconds")
        return result

    return cast(F, wrapper)
