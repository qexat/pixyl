import os
import sys
import typing

import result

from pixyl.engine import Engine, SizeFactor
from pixyl.data import FrameSequence


def run_file(file: typing.BinaryIO, *, fps: float, factor: SizeFactor) -> int:
    engine = Engine()

    match FrameSequence.from_file(file):
        case result.Ok(fs):
            pass
        case result.Err(e):
            print(e.__class__.__name__, e, sep=": ", file=sys.stderr)
            return os.EX_DATAERR

    engine.render(fs, factor)

    try:
        engine.display(fps)
    except ValueError as e:
        print(e.__class__, e, sep=": ", file=sys.stderr)
        return os.EX_DATAERR

    return os.EX_OK
