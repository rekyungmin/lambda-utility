from __future__ import annotations

__all__ = ("Unzip",)

import functools
import io
import re
import zipfile
from collections.abc import Iterable, Callable
from types import TracebackType
from typing import Optional, Type, Union, BinaryIO

from lambda_utility.path import PathExt
from lambda_utility.typedefs import PathLike


class Unzip:
    __slots__ = (
        "zip_path",
        "zip_ref",
        "includes",
        "excludes",
    )
    zip_path: Union[BinaryIO, PathLike]
    zip_ref: zipfile.ZipFile
    includes: Iterable[Union[re.Pattern, Callable[[PathExt], bool]]]
    excludes: Iterable[Union[re.Pattern, Callable[[PathExt], bool]]]

    def __init__(
        self,
        zip_path: Union[BinaryIO, PathLike],
        *,
        includes: Optional[
            Iterable[Union[re.Pattern, Callable[[PathExt], bool]]]
        ] = None,
        excludes: Optional[
            Iterable[Union[re.Pattern, Callable[[PathExt], bool]]]
        ] = None,
    ):
        self.zip_path = zip_path if isinstance(zip_path, io.BytesIO) else str(zip_path)
        self.includes = includes if includes is not None else []
        self.excludes = excludes if excludes is not None else []

    def __enter__(self):
        self.zip_ref = zipfile.ZipFile(self.zip_path).__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.zip_ref.__exit__(exc_type, exc_value, traceback)

    def __call__(
        self,
        *,
        path: Optional[PathLike] = None,
        files: Optional[Iterable[PathLike]] = None,
        pwd: Optional[bytes] = None,
    ) -> list[str]:
        if path is not None:
            path = str(path)

        if files is None:
            files = self.get_valid_namelist()

        members: list[str] = list(map(str, files))
        self.zip_ref.extractall(path=path, members=members, pwd=pwd)
        return members

    @functools.lru_cache
    def get_valid_namelist(self) -> tuple[str, ...]:
        return tuple(
            zipped_file.filename
            for zipped_file in self.get_infolist()
            if not zipped_file.is_dir()
            and self.check_includes(zipped_file.filename)
            and not self.check_excludes(zipped_file.filename)
        )

    @functools.lru_cache
    def get_infolist(self) -> tuple[zipfile.ZipInfo, ...]:
        return tuple(self.zip_ref.infolist())

    def check_excludes(self, path: PathLike) -> bool:
        path = PathExt(path)
        for exclude in self.excludes:
            if isinstance(exclude, re.Pattern):
                if exclude.search(str(path)):
                    return True
            elif callable(exclude):
                if exclude(path):
                    return True
        return False

    def check_includes(self, path: PathLike) -> bool:
        path = PathExt(path)
        for include in self.includes:
            if isinstance(include, re.Pattern):
                if not include.search(str(path)):
                    return False
            elif callable(include):
                if not include(PathExt(path)):
                    return False
        return True

    def get_sequence_names(self, extension: str) -> tuple[str, ...]:
        extension = extension.lstrip(".")
        pattern = re.compile(fr"(\d+)(\.{extension})$", flags=re.IGNORECASE)

        sequence_names: dict[int, str] = {}

        for name in self.get_valid_namelist():
            m = pattern.search(name)
            if not m:
                continue

            num = int(m.group(1))
            if num in sequence_names:
                raise ValueError(
                    f"duplicate number -> {sequence_names[num]!r}, {name!r}"
                )

            sequence_names[num] = name

        sorted_result = sorted(sequence_names.items())
        return tuple(name for _, name in sorted_result)
