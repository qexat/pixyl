from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from io import StringIO
from itertools import islice
from typing import Generic
from typing import Literal
from typing import Self
from typing import TypeVar

_T = TypeVar("_T")
_U = TypeVar("_U")


class _ValueError(ValueError):
    @classmethod
    def _incorrect_size(cls, w: int, h: int, qual: Literal["small", "big"]) -> Self:
        return cls(f"iterable is too {qual} to build a {w}x{h} matrix from")

    @classmethod
    def too_small_iterable(cls, width: int, height: int) -> Self:
        return cls._incorrect_size(width, height, "small")

    @classmethod
    def too_big_iterable(cls, width: int, height: int) -> Self:
        return cls._incorrect_size(width, height, "big")

    @classmethod
    def from_unsatisfied_guard(cls, el_pos: tuple[int, int]) -> Self:
        return cls(f"element at {el_pos} does not satisfy the guard function")


class Matrix(Generic[_T]):
    @staticmethod
    def unflatten(
        flat_iterable: Iterable[_T],
        /,
        width: int,
        height: int,
    ) -> list[list[_T]]:
        if width <= 0:
            raise ValueError("width must be strictly positive")
        elif height <= 0:
            raise ValueError("height must be strictly positive")

        matrix_area = width * height

        flat_list: list[_T] = list(flat_iterable)
        flat_list_len: int = len(flat_list)

        if flat_list_len < matrix_area:
            raise _ValueError.too_small_iterable(width, height)
        elif flat_list_len > matrix_area:
            raise _ValueError.too_big_iterable(width, height)

        return [list(batch) for batch in batched(flat_iterable, width)]

    def __init__(self, iterable: Iterable[_T], /, width: int, height: int) -> None:
        self.__flattened = list(iterable)
        self.__matrix = Matrix.unflatten(self.__flattened, width, height)
        self.__width = width
        self.__height = height

    def __repr__(self) -> str:
        buffer = StringIO()
        spacing = self.width * 3 - 2

        for i, row in enumerate(self):
            if i == 0:
                print("╭", " " * spacing, "╮", file=buffer)
            print("│ ", end="", file=buffer)
            print(*row, sep=", ", end=" │\n", file=buffer)

            if i == self.height - 1:
                print("╰", " " * spacing, "╯", file=buffer)

        return buffer.getvalue()

    def __len__(self) -> int:
        return len(self.__flattened)

    def __iter__(self):
        yield from self.__matrix

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    def is_square(self) -> bool:
        return self.width == self.height

    def flatten(self) -> list[_T]:
        return self.__flattened

    def clone(self) -> Self:
        return type(self)(self.flatten(), self.width, self.height)

    def map(
        self,
        function: Callable[[_T], _U],  # type: ignore
        guard: Callable[[_T], bool] = lambda _: True,
    ):
        """
        KNOWN ISSUE: return type is INCORRECT, it should be Self[_U]
        """

        flattened_src = self.flatten()
        flattened_dest: list[_U] = []

        for flat_index, el in enumerate(flattened_src):
            if not guard(el):
                pos_x, pos_y = divmod(flat_index, self.width)
                raise _ValueError.from_unsatisfied_guard((pos_x, pos_y))
            flattened_dest.append(function(el))

        return type(self)(flattened_dest, self.width, self.height)


def batched(iterable: Iterable[_T], n: int) -> Iterator[tuple[_T, ...]]:
    """
    Batch data into tuples of length n. The last batch may be shorter.

    Recipe stolen from: <https://docs.python.org/3/library/itertools.html>
    """
    if n < 1:
        raise ValueError("n must be higher or equal to 1")

    iterator = iter(iterable)  # we don't consume the original iterable

    while batch := tuple(islice(iterator, n)):
        yield batch


def fps(string: str) -> int:
    if (r := int(string)) <= 0:
        raise ValueError
    return r
