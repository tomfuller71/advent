"""
--- Day 8: Resonant Collinearity ---
"""

from aoc_utils import *
from itertools import combinations


def get_antennas(grid):
    """Extract antenna positions from the grid."""
    antennas = defaultdict(list)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != ".":
                point = Point(x, y)
                if cell not in antennas:
                    antennas[cell] = [point]
                else:
                    antennas[cell].append(point)
    return antennas


@timer
def part_1(data, log=False):
    """Solve part 1 of the problem."""
    grid = parse_grid(data)

    if log:
        debug_print(f"Parsed data: {grid[:5]}...")  # Show first 5 items

    # TODO: Implement part 1 logic here

    antennas = get_antennas(grid)
    if log:
        debug_print(f"Antenna positions: {antennas}")
    antinodes = set()
    for antenna, points in antennas.items():
        combos = combinations(points, 2)
        if log:
            # Print each antenna and its positions
            points_str = ", ".join(f"({p.x}, {p.y})" for p in points)
            debug_print(f"Antenna {antenna} at positions: {points_str}")
        for a, b in combos:
            # Calculate the slope and intercept for each pair
            diff = b - a
            nodes = [a - diff, b + diff]
            if log:
                debug_print(
                    f"Processing antenna {antenna} with points {a} and {b}, diff: {diff}, nodes: {nodes}"
                )
            for node in nodes:
                if node.inBounds(grid):
                    antinodes.add(node)
                    if log:
                        debug_print(
                            f"Adding antinode at {node} for antenna {antenna} with points {a} and {b}"
                        )
    if log:
        debug_print(f"Antinodes found: {antinodes}")

    return len(antinodes)


@timer
def part_2(data, log=False):
    """Solve part 2 of the problem."""
    grid = parse_grid(data)

    if log:
        debug_print(f"Parsed data: {grid[:5]}...")  # Show first 5 items

    # TODO: Implement part 1 logic here

    antennas = get_antennas(grid)
    if log:
        debug_print(f"Antenna positions: {antennas}")
    antinodes = set()
    for antenna, points in antennas.items():
        combos = combinations(points, 2)
        if log:
            # Print each antenna and its positions
            points_str = ", ".join(f"({p.x}, {p.y})" for p in points)
            debug_print(f"Antenna {antenna} at positions: {points_str}")
        for a, b in combos:
            # Calculate the slope and intercept for each pair
            diff = b - a
            antinodes.add(a)
            antinodes.add(b)
            a_back = a - diff
            b_forward = b + diff
            while a_back.inBounds(grid):
                antinodes.add(a_back)
                a_back -= diff
            while b_forward.inBounds(grid):
                antinodes.add(b_forward)
                b_forward += diff
    if log:
        debug_print(f"Antinodes found: {antinodes}")

    return len(antinodes)


if __name__ == "__main__":
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
