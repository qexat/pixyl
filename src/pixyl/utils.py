import collections.abc
import itertools
import typing

T = typing.TypeVar("T")


def batched(
    iterable: collections.abc.Iterable[T],
    n: int,
) -> collections.abc.Iterator[tuple[T, ...]]:
    """
    Batch data into tuples of length n. The last batch may be shorter.

    Recipe stolen from: <https://docs.python.org/3/library/itertools.html>
    """

    if n < 1:
        raise ValueError("n must be higher or equal to 1")

    iterator = iter(iterable)  # we don't consume the original iterable

    while batch := tuple(itertools.islice(iterator, n)):
        yield batch


def fps(string: str) -> int:
    if (r := int(string)) <= 0:
        raise ValueError
    return r
