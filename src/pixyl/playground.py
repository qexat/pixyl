from pixyl.pixyl import Engine, FrameSequence


def playground() -> int:
    engine = Engine()

    with open("examples/test.afs", "r") as test_afs:
        fs = FrameSequence.from_file(test_afs, 16, 16)

    engine.render(fs, fps=4)

    return 0
