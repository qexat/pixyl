"""
Script to generate `test.pxsf`.
"""
import os

from pixyl.maker import create_pxsf


def main() -> None:
    data = [
        [
            [1, 1, 1, 1],
            [3, 3, 3, 3],
            [2, 2, 2, 2],
            [6, 6, 6, 6],
        ],
        [
            [3, 3, 3, 3],
            [2, 2, 2, 2],
            [6, 6, 6, 6],
            [4, 4, 4, 4],
        ],
        [
            [2, 2, 2, 2],
            [6, 6, 6, 6],
            [4, 4, 4, 4],
            [5, 5, 5, 5],
        ],
        [
            [6, 6, 6, 6],
            [4, 4, 4, 4],
            [5, 5, 5, 5],
            [0, 0, 0, 0],
        ],
        [
            [4, 4, 4, 4],
            [5, 5, 5, 5],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [5, 5, 5, 5],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
    ]

    file_path = os.path.join(os.path.dirname(__file__), "test.pxsf")

    with open(file_path, "wb") as file:
        create_pxsf(file, 7, 4, 4, data)


if __name__ == "__main__":
    main()
