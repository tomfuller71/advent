import argparse

parser = argparse.ArgumentParser(
    prog="day_{day}",
    description="Advent of Code challenge.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "-i", "--infile", type=str, default="input.txt", help="infile to use"
)
parser.add_argument(
    "-l", "--log", type=bool, default=False, help="Enable logging"
)