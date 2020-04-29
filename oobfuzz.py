import argparse, sys


class OOBFuzz():

    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='OOBFuzz')
    parser.add_argument('')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    oobfuzz = OOBFuzz()
    oobfuzz.run()