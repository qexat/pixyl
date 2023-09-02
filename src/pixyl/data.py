# pyright: reportUnusedCallResult = false

from __future__ import annotations

import array
import collections.abc
import dataclasses
import functools
import io
import typing

import result

from pixyl.constants import HEADER_SEP, MAGIC_NUMBER, START_OF_CONTENT, START_OF_HEADING
from pixyl.utils import batched

T = typing.TypeVar("T")


@dataclasses.dataclass(slots=True)
class Matrix:
    data: array.array[int]
    width: int
    height: int

    @functools.cached_property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    # *- Magic methods -* #

    def __repr__(self) -> str:
        buffer = io.StringIO()
        spacing = self.width * 3

        print("╭", " " * spacing, "╮", sep="", file=buffer)

        for row in self:
            buffer.write("│ ")
            print(*row, sep=", ", end=" │\n", file=buffer)

        print("╰", " " * spacing, "╯", sep="", file=buffer)

        return buffer.getvalue()

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> collections.abc.Iterator[tuple[int, ...]]:
        yield from batched(self.data, self.width)

    # *- Predicates -* #

    def is_square(self) -> bool:
        return self.width == self.height

    # *- Methods -* #

    def clone(self) -> typing.Self:
        return self.__class__(self.data[:], self.width, self.height)

    # *- Type conversions -* #

    def as_list(self) -> list[list[int]]:
        return [list(row) for row in self]

    def as_flat_list(self) -> list[int]:
        return self.data.tolist()


class PxsfData(typing.NamedTuple):
    nb_frames: int
    width: int
    height: int
    content: bytes

    @property
    def size(self) -> int:
        return self.width * self.height

    def to_matrices(self) -> collections.abc.Iterator[Matrix]:
        for batch in batched(self.content, self.size):
            yield Matrix(array.array("B", batch), self.width, self.height)


@dataclasses.dataclass(slots=True)
class Parser:
    raw_source: bytes

    def parse_header(
        self,
        source: bytes,
    ) -> result.Result[tuple[int, int, int], ValueError]:
        parts = source.split(HEADER_SEP)

        if len(parts) != 3:
            return result.Err(ValueError("invalid header"))

        return result.Ok(tuple(map(int, parts)))

    def parse(self) -> result.Result[PxsfData, TypeError | ValueError]:
        if self.raw_source[0:4] != MAGIC_NUMBER:
            return result.Err(TypeError("not a pxsf file"))

        source = self.raw_source[4:]

        if (soh_index := source.find(START_OF_HEADING)) == -1:
            return result.Err(ValueError("no header found"))

        if (sot_index := source.find(START_OF_CONTENT)) == -1:
            return result.Err(ValueError("no data found"))

        if soh_index < sot_index:
            header_source = source[soh_index + 1 : sot_index]
            data_source = source[sot_index + 1 :]
        else:
            header_source = source[soh_index + 1 :]
            data_source = source[sot_index + 1 : soh_index]

        match self.parse_header(header_source):
            case result.Ok((nb_frames, width, height)):
                pass
            case err:
                return err

        return result.Ok(
            PxsfData(
                nb_frames,
                width,
                height,
                data_source,
            )
        )


class FrameSequence(list[Matrix]):
    @classmethod
    def from_file(
        cls,
        file: typing.BinaryIO,
    ) -> result.Result[typing.Self, TypeError | ValueError]:
        parser = Parser(file.read())

        parse_result = parser.parse()

        if isinstance(parse_result, result.Err):
            return parse_result

        data = parse_result.unwrap()

        return result.Ok(cls(data.to_matrices()))
