from argparse import ArgumentParser, FileType, Namespace

from pixyl.playground import playground
from pixyl.utils import fps


def parse_args(argv: list[str] | None = None) -> Namespace:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    playground_parser = subparsers.add_parser("playground")
    playground_parser.add_argument("file", type=FileType("r"))
    playground_parser.add_argument("--fps", type=fps, default=10)

    return parser.parse_args(argv)


def main_debug(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    match args.command:
        case "playground":
            return playground(args.file, args.fps)
        case _:
            pass

    return 0


def main() -> int:
    return main_debug()
