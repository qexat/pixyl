from pixyl.pixyl import Engine, FrameSequence


def playground() -> int:
    engine = Engine()

    with open("examples/test.afs", "r") as test_afs:
        fs = FrameSequence.from_file(test_afs, 8, 8)

    engine.render(fs, fps=3)

    return 0
