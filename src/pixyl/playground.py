from typing import TextIO
from pixyl.pixyl import Engine, FrameSequence


def playground(file: TextIO, fps: float) -> int:
    try:
        engine = Engine()
        fs = FrameSequence.from_file(file, 16, 16)
        engine.render(fs, fps=fps)

        return 0
    finally:
        file.close()
