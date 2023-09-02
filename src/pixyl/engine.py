# pyright: reportUnusedCallResult = false
import dataclasses
import io
import time
import typing

import coquille
from pixyl.constants import VALID_FACTORS
from pixyl.data import FrameSequence
from pixyl.data import Matrix
from pixyl.utils import batched


SizeFactor: typing.TypeAlias = typing.Literal[1, 2, 3, 4, 5]


@dataclasses.dataclass(slots=True)
class Engine:
    frame_buffer: io.StringIO = dataclasses.field(default_factory=io.StringIO)
    sequence_buffers: list[io.StringIO] = dataclasses.field(default_factory=list)

    def render_frame(self, frame: Matrix, factor: SizeFactor = 1) -> None:
        """
        Render and buffer an individual frame.
        """

        final_frame = (row for row in frame for _ in range(factor))

        for row_top, row_bottom in batched(final_frame, 2):
            for top, bottom in zip(row_top, row_bottom):
                self.frame_buffer.write(
                    f"\x1b[38;5;{top};48;5;{bottom}m▀" * factor,
                )
            self.frame_buffer.write("\x1b[39;49m\n")

    def sequence_frame(self) -> None:
        """
        Put the frame buffer in the sequence buffer list and reset it.
        """

        self.sequence_buffers.append(self.frame_buffer)
        self.frame_buffer = io.StringIO()

    def render(self, sequence: FrameSequence, factor: SizeFactor = 1) -> None:
        """
        Render and buffer a sequence of frame in order to be displayed.
        """

        if factor not in VALID_FACTORS:
            raise ValueError("invalid factor")

        for frame in sequence:
            self.render_frame(frame, factor)
            self.sequence_frame()
            self.sequence_buffers.append(self.frame_buffer)

    def display(self, fps: float = 6) -> None:
        """
        Display the currently buffered frame sequence.
        """

        if fps <= 0:
            raise ValueError(f"fps must be positive (not {fps})")

        non_empty_buffers = [
            buffer for buffer in self.sequence_buffers if buffer.getvalue()
        ]

        last_non_empty_buffer_height = (
            non_empty_buffers[-1].getvalue().count("\n") if non_empty_buffers else 0
        )

        with coquille.Coquille.new("hide_cursor"):
            for buffer in self.sequence_buffers:
                string = buffer.getvalue()
                height = string.count("\n")
                print(string, end=f"\r\x1b[{height}A")
                time.sleep(1 / fps)

            height = last_non_empty_buffer_height
            print(f"\x1b[{height}B")
