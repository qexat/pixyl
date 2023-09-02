# pyright: reportUnusedCallResult = false

import argparse
from pixyl.constants import VALID_FACTORS

from pixyl.runner import run_file
from pixyl.utils import fps


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=argparse.FileType("rb"))
    parser.add_argument("--fps", type=fps, default=10)
    parser.add_argument("--factor", type=int, choices=VALID_FACTORS, default=1)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    exit_code = run_file(args.file, fps=args.fps, factor=args.factor)
    args.file.close()

    return exit_code
