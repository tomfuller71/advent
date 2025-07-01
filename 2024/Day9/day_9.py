"""
Day X: [Problem Title]

[Brief description of the problem]
"""

import dis
from hmac import new
from importlib.metadata import files
from math import e
from operator import le
from tabnanny import check
from aoc_utils import *


def parse_input(data):
    """Parse the input data into a useful format."""
    # TODO: Implement parsing logic
    return [int(c) for c in data.strip()]


@timer
def part_1(data, log=False):
    """Solve part 1 of the problem."""

    disk_map = parse_input(data)
    disc = []
    id = 0
    compress_size = 0
    free_space = 0

    for i, val in enumerate(disk_map):
        if i % 2 == 0:
            disc.extend([id] * val)
            id += 1
            compress_size += val
        else:
            disc.extend([None] * val)
            free_space += val
    i = 0
    j = len(disc) - 1
    while i < compress_size:
        val = disc[i]
        if val is None:
            while disc[j] is None:
                j -= 1
            disc[i] = disc[j]
            disc[j] = None
            j -= 1
        i += 1

    checksum = 0
    for i in range(len(disc)):
        if disc[i] is not None:
            checksum += (i) * disc[i]

    if log:
        print(f"Disk map: {disk_map}")
        print(f"Disk structure: {disc}")
        print(f"Compressed size: {compress_size}")
        print(f"Free space: {free_space}")

    return checksum


@timer
def part_2(data, log=False):
    """Solve part 2 of the problem"""

    disk_map = parse_input(data)
    files = []
    spaces = []
    id_count = 0
    disc_i = 0

    for i, val in enumerate(disk_map):
        if i % 2 == 0:
            files.append((disc_i, id_count, val))
            id_count += 1
        elif val > 0:
            spaces.append([disc_i, val])
        disc_i += val

    file_positions = {}

    for file_i in range(len(files) - 1, -1, -1):
        disc_i, id, size = files[file_i]

        best_space_idx = None
        for space_idx, (sp_pos, sp_size) in enumerate(spaces):
            if sp_pos >= disc_i:
                break
            if sp_size >= size:
                best_space_idx = space_idx
                break

        if best_space_idx is None:
            file_positions[id] = disc_i
            debug_print(
                f"File {id} stays in original position at {disc_i}", enabled=log
            )
            continue

        sp_pos, sp_size = spaces[best_space_idx]
        file_positions[id] = sp_pos
        debug_print(f"File {id} placed at {sp_pos}", enabled=log)
        if sp_size == size:
            spaces.pop(best_space_idx)
        else:
            spaces[best_space_idx][0] = sp_pos + size
            spaces[best_space_idx][1] = sp_size - size

    checksum = 0
    for id, pos in file_positions.items():
        file_size = files[id][2]
        for i in range(file_size):
            checksum += (pos + i) * id

    if log:
        debug_print(f"Disk map: {disk_map}")
        debug_print(f"File positions: {file_positions}")
        debug_print(f"Final checksum: {checksum}")

    return checksum


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
