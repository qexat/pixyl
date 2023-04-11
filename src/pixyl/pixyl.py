from enum import IntEnum
from functools import cached_property
from io import StringIO
import time
from typing import Literal, Self, TextIO

from pixyl.utils import Matrix, batched


PixelColorInt = Literal[0, 1, 2, 3, 4, 5, 6, 7, 9]

VALID_COLORS = {0, 1, 2, 3, 4, 5, 6, 7, 9}


class PixelColor(IntEnum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    NONE = 9


class Frame:
    def __init__(self, pixels: Matrix[PixelColor]) -> None:
        self.__matrix = pixels

    @cached_property
    def matrix(self) -> Matrix[PixelColor]:
        return self.__matrix.clone()

    @property
    def width(self) -> int:
        return self.matrix.width

    @property
    def height(self) -> int:
        return self.matrix.height

    @property
    def size(self) -> tuple[int, int]:
        return self.matrix.size

    @classmethod
    def from_int_matrix(cls, matrix: Matrix[int]) -> Self:
        # matrix.map() returns Matrix[PixelColor] but is incorrectly typed as returning Matrix[int]
        transformed_flat: Matrix[PixelColor] = matrix.map(PixelColor, lambda pci: pci in VALID_COLORS)  # type: ignore
        return cls(transformed_flat)

    def __repr__(self) -> str:
        buffer = StringIO()

        for row_top, row_bottom in batched(self.__matrix, 2):
            for top, bottom in zip(row_top, row_bottom):
                buffer.write(f"\x1b[3{top};4{bottom}m▀")
            buffer.write("\n\x1b[39;49m")

        return buffer.getvalue()


class FrameSequence(list[Frame]):
    @classmethod
    def from_file(cls, file: TextIO, width: int, height: int) -> Self:
        raw_contents = file.read().splitlines()

        matrices: list[Matrix[int]] = [
            Matrix("".join(frame_rows), width, height).map(int, str.isdigit)
            for frame_rows in batched(raw_contents, height)
        ]  # type: ignore

        return cls(Frame.from_int_matrix(matrix) for matrix in matrices)


class Engine:
    def render(self, sequence: FrameSequence, *, fps: float = 6) -> None:
        if fps <= 0:
            raise ValueError(f"{fps} is not a valid fps value")

        *frames, last_frame = sequence
        for frame in frames:
            print(frame, end=f"\x1b[{frame.height // 2}A")
            time.sleep(1 / fps)
        print(last_frame)
