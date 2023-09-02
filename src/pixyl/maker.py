# pyright: reportUnusedCallResult = false

import io
import typing

from pixyl.constants import MAGIC_NUMBER, START_OF_CONTENT, START_OF_HEADING


def create_pxsf(
    file: typing.BinaryIO,
    nb_frames: int,
    width: int,
    height: int,
    data: list[list[list[int]]],
) -> None:
    buffer = io.BytesIO()

    header = b";".join(ord(f"{i}").to_bytes() for i in (nb_frames, width, height))
    contents = b"".join(b"".join(map(bytes, row)) for row in data)

    buffer.write(MAGIC_NUMBER)
    buffer.write(START_OF_HEADING.to_bytes())
    buffer.write(header)
    buffer.write(START_OF_CONTENT.to_bytes())
    buffer.write(contents)

    file.write(buffer.getvalue())
