# This is a template for an Advent of Code problem solution.
# Replace the part_1 and part_2 functions with your actual logic.


from re import sub


XMAS = ["X", "M", "A", "S"]
LEN_XMAS = 4


def parse_input(data):
    """
    Input is a text  file representing an n * n grid of characters.
    """
    # Example parsing logic, modify as needed
    return [[*word] for word in data.splitlines()]


def check_xmas(grid, i, j, fwd: bool = True):
    """
    Check if the XMAS pattern exists in the grid starting from (i, j) in the specified direction.
    Direction can be 'row', 'col', or 'diag'.
    """
    n = len(grid)
    offset = 0 if fwd else LEN_XMAS - 1
    row = sum(
        int(grid[i][j + k] == XMAS[abs(offset - k)])
        for k in range(LEN_XMAS)
        if j + k < n
    )
    col = sum(
        int(grid[i + k][j] == XMAS[abs(offset - k)])
        for k in range(LEN_XMAS)
        if i + k < n
    )
    diag_down_right = sum(
        int(grid[i + k][j + k] == XMAS[abs(offset - k)])
        for k in range(LEN_XMAS)
        if i + k < n and j + k < n
    )
    diag_down_left = sum(
        int(grid[i + k][j - k] == XMAS[abs(offset - k)])
        for k in range(LEN_XMAS)
        if i + k < n and j - k >= 0
    )
    results = []
    if row == LEN_XMAS:
        results.append("--")
    if col == LEN_XMAS:
        results.append("|")
    if diag_down_right == LEN_XMAS:
        results.append("\\")
    if diag_down_left == LEN_XMAS:
        results.append("/")
    return results


def part_1(data):
    grid = parse_input(data)
    print(
        "Grid parsed successfully. Size:", len(grid), "x", len(grid[0]) if grid else 0
    )
    if not grid or not grid[0]:
        print("Empty grid, returning 0.")
        return 0

    n = len(grid)
    c = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] not in ["X", "S"]:
                continue
            if grid[i][j] == "X":

                found = check_xmas(grid, i, j, fwd=True)
                c += len(found)
                # for direction in found:
                #     print(f"Found XMAS fwd at ({i}, {j}) in {direction} direction")
            elif grid[i][j] == "S":
                found = check_xmas(grid, i, j, fwd=False)
                c += len(found)
                # for direction in found:
                #     print(
                #         f"Found XMAS backwards at ({i}, {j}) in {direction} direction"
                #     )
    return c


DIAGONALS = [
    (-1, -1),  # Top-left
    (-1, 1),  # Top-right
    (1, -1),  # Bottom-left
    (1, 1),  # Bottom-right
]

MATCHES = [
    ["M", "M", "S", "S"],
    ["S", "S", "M", "M"],
    ["S", "M", "S", "M"],
    ["M", "S", "M", "S"],
]


def part_2(data):
    grid = parse_input(data)
    print(
        "Grid parsed successfully. Size:", len(grid), "x", len(grid[0]) if grid else 0
    )
    if not grid or not grid[0]:
        print("Empty grid, returning 0.")
        return 0

    n = len(grid)
    c = 0
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if grid[i][j] != "A":
                continue
            subgrid = [grid[i + i_add][j + j_add] for i_add, j_add in DIAGONALS]
            if subgrid in MATCHES:
                c += 1
                print(f"Found A at ({i}, {j}) with diagonal matching {subgrid}")
    return c


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
