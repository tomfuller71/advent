"""
Day X: [Problem Title]

[Brief description of the problem]
"""

from aoc_utils import *


def parse_input(data):
    """Parse the input data into a useful format."""
    lines = parse_lines(data)
    # TODO: Implement parsing logic
    return lines


@timer
def part_1(data, log=False):
    """Solve part 1 of the problem."""
    parsed_data = parse_input(data)

    if log:
        debug_print(f"Parsed data: {parsed_data[:5]}...")  # Show first 5 items

    # TODO: Implement part 1 logic here
    result = None

    return result


@timer
def part_2(data, log=False):
    """Solve part 2 of the problem."""
    parsed_data = parse_input(data)

    if log:
        debug_print(f"Parsed data: {parsed_data[:5]}...")  # Show first 5 items

    # TODO: Implement part 2 logic here
    result = None

    return result


if __name__ == "__main__":
    import argparse
    import os
    from pathlib import Path

    # Use os to change directory to ensure we are in /Users/tomfuller/advent/{year}/Day{day}
    current_path = Path(__file__).resolve().parent
    os.chdir(current_path)

    # Use the enhanced argument parser from aoc_utils
    args = day_parser().parse_args()

    # Determine input file
    if args.example:
        inFile = "example.txt"
    else:
        inFile = "input.txt"

    log = args.log
    part = args.part

    # Check if the input file exists
    if not os.path.exists(inFile):
        raise FileNotFoundError(
            f"Input file '{inFile}' does not exist in {current_path}."
        )

    # Read the input data
    with open(inFile) as f:
        data = f.read().strip()
        if log:
            print(f"Using {inFile} data (length: {len(data)} chars)...\n")

    # Run the specified part
    if log:
        print(f"Running Part {part} with logging enabled\n")

    if part == 1:
        result = part_1(data, log=log)
    elif part == 2:
        result = part_2(data, log=log)
    else:
        raise ValueError("Invalid part specified. Use 1 or 2.")

    if result is not None:
        print(f"\nResult for Part {part}: {result}")
    else:
        print(f"Part {part} returned None - implementation may be incomplete.")
