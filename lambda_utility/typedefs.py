__all__ = ("PathLike",)

from typing import Union

from lambda_utility.path import PathExt

PathLike = Union[str, PathExt]
