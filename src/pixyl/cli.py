from argparse import ArgumentParser, Namespace

from pixyl.playground import playground


def parse_args(argv: list[str] | None = None) -> Namespace:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    playground_parser = subparsers.add_parser("playground")

    return parser.parse_args(argv)


def main_debug(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    match args.command:
        case "playground":
            return playground()
        case _:
            pass

    return 0


def main() -> int:
    return main_debug()
