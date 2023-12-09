import argparse

parser = argparse.ArgumentParser(
    description="Run Advent of Code problem.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "-i",
    "--infile",
    action="store",
    help="Input file name (default: %(default)s)",
    default="example.txt",
)

parser.add_argument(
    "-l",
    "--log",
    action="store_true",
    help="Enable log (default: %(default)s)",
    default=False,
)