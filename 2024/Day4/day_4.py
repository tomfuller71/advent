# This is a template for an Advent of Code problem solution.
# Replace the part_1 and part_2 functions with your actual logic.


def part_1(data):
    # Implement part 1 logic here
    pass


def part_2(data):
    # Implement part 2 logic here
    pass


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
        default=1,
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
