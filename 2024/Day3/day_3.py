# This is a template for an Advent of Code problem solution.
# Replace the part_1 and part_2 functions with your actual logic.
from hmac import new
import re
from tracemalloc import start

mult_expression = re.compile(r"((mul)\(([+-]?\d{1,3}),([+-]?\d{1,3})\))")


def part_1(data: str):
    matches = mult_expression.findall(data)
    sum = 0
    for _, inst, x, y in matches:
        # print(f"Instruction: {inst}, x: {x}, y: {y}")
        sum += int(x) * int(y)
    return sum


def part_2(data: str):
    sum = 0
    start = 0
    end = len(data) - 1
    active = True
    while end < len(data):
        new_start = start
        if active:
            try:
                inst = "don't()"
                end = data.index(inst, start)
                print(f"Found '{inst}' at index {end}")
                active = False
                new_start = end + len(inst)
            except ValueError:
                end = len(data)

            search = data[start : end + 1]
            print(f"Searching in: {search}")
            sum += part_1(search)
            start = new_start
            print(f"New start index: {start}")
        else:
            try:
                inst = "do()"
                start = data.index(inst, start) + len(inst)
                active = True
                print(f"Found '{inst}' at index {start}")
            except ValueError:
                continue
    return sum


if __name__ == "__main__":
    import argparse
    import os
    from pathlib import Path

    #  Use os to change directory to ensure we are in /Users/tomfuller/advent/{year}/Day{day}
    current_path = Path(__file__).resolve().parent
    os.chdir(current_path)

    # Get command line arguments
    parser = argparse.ArgumentParser(
        description="Run Advent of Code problem.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="Enable log (default: %(default)s)",
        default=True,
    )
    parser.add_argument(
        "-i",
        "--infile",
        type=str,
        help="Input file to read data from (default: input.txt)",
        choices=["input.txt", "example.txt"],
        default="input.txt",
    )
    parser.add_argument(
        "-p",
        "--part",
        type=int,
        choices=[1, 2],
        help="Specify part to run (1 or 2, default: %(default)s)",
        default=2,
    )

    args = parser.parse_args()
    inFile = args.infile
    log = args.log
    part = args.part

    # Check if the input file exists
    if not os.path.exists(inFile):
        raise FileNotFoundError(f"Infile '{inFile}' does not exist in {current_path}.")

    # Read the input data
    with open(inFile) as f:
        data = f.read().strip()
        if log:
            print(f"Using {inFile} data...\n")

    # Run the specified part
    if log:
        print("Log enabled. Data length:", len(data), "\n")
        print(f"Part {part}:\n")
    if args.part == 1:
        result = part_1(data)
    elif args.part == 2:
        result = part_2(data)
    else:
        raise ValueError("Invalid part specified. Use 1 or 2.")
    if result is not None:
        print(f"Result for part {part}:\n {result}")
