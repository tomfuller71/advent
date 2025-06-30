# This is a template for an Advent of Code problem solution.
# Replace the part_1 and part_2 functions with your actual logic.

from termcolor import colored
from collections import OrderedDict


def parse_input(data) -> tuple[list[list[str]], int, int, tuple[int, int]]:
    map = [[c for c in line] for line in data.splitlines()]
    r = len(map)
    c = len(map[0]) if r > 0 else 0
    cursor_idx = data.replace("\n", "").index(
        "^"
    )  # Strip newline character from the data
    pos: tuple[int, int] = divmod(cursor_idx, c)
    return map, r, c, pos


DIRECTIONS = [
    (-1, 0),  # Up
    (0, 1),  # Right
    (1, 0),  # Down
    (0, -1),  # Left
]

MOVE = tuple[tuple[int, int], int]  # (position, move direction index)

MOVES_STR = ["↑", "→", "↓", "←"]


def check_loop(
    start: MOVE,
    matrix: list[list[str]],
) -> bool:
    r = len(matrix)
    c = len(matrix[0]) if r > 0 else 0
    pos, move_idx = start
    x, y = pos
    matrix[x][y] = "#"
    did_loop = False
    new_searched = set()
    while 0 <= x < r and 0 <= y < c:
        if matrix[x][y] == "#":
            x -= DIRECTIONS[move_idx][0]
            y -= DIRECTIONS[move_idx][1]
            move_idx = (move_idx + 1) % 4
        else:
            move = ((x, y), move_idx)
            if move in new_searched:
                did_loop = True
                break

            new_searched.add(move)
            x += DIRECTIONS[move_idx][0]
            y += DIRECTIONS[move_idx][1]

    matrix[pos[0]][pos[1]] = "."
    return did_loop


def get_route(start: tuple[int, int], matrix: list[list[str]], r: int, c: int):
    route = OrderedDict()  # Use OrderedDict to maintain insertion order
    x, y = start
    move_idx = 0
    while 0 <= x < r and 0 <= y < c:
        if matrix[x][y] == "#":
            x -= DIRECTIONS[move_idx][0]
            y -= DIRECTIONS[move_idx][1]
            move_idx = (move_idx + 1) % 4
        else:
            if not ((x, y)) in route:
                route[(x, y)] = move_idx
            matrix[x][y] = MOVES_STR[move_idx]
        x += DIRECTIONS[move_idx][0]
        y += DIRECTIONS[move_idx][1]
    return route


def print_map(
    matrix: list[list[str]], moves: list[MOVE], new_obstacles: set[tuple[int, int]]
):
    r = len(matrix)
    c = len(matrix[0]) if r > 0 else 0
    start = moves[0][0]
    end = moves[-1][0]
    matrix[start[0]][start[1]] = colored("S", "green")  # Start
    matrix[end[0]][end[1]] = colored("E", "red")  # End

    for pos, move_dir in moves:
        x, y = pos
        matrix[x][y] = MOVES_STR[move_dir]

    for x, y in new_obstacles:
        matrix[x][y] = colored("O", "blue")

    if c < 10:
        print(" ", " ".join([str(i) for i in range(c)]))
    for i, line in enumerate(matrix):
        if i < 10:
            print(f"{i}   " + " ".join(line))
        elif i < 100:
            print(f"{i}  " + " ".join(line))
        else:
            print(f"{i} " + " ".join(line))


def part_1(data, log=False):
    matrix, r, c, start = parse_input(data)
    route = get_route(start, matrix, r, c)
    print(f"Part 1: {len(route)}")


def part_2(data, log=False):
    matrix, r, c, start = parse_input(data)
    route = get_route(start, matrix, r, c)

    new_obstacles = set()
    moves = [*route.items()]

    for (x, y), move_idx in moves[1:]:
        loops = check_loop(((x, y), move_idx), matrix)
        if loops:
            new_obstacles.add((x, y))

    print(f"Part 1: {len(moves)}")
    print(f"Part 2: {len(new_obstacles)}")
    if log:
        print_map(matrix, moves, new_obstacles)


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
        default=False,
    )
    parser.add_argument(
        "-e",
        "--example",
        action="store_true",
        help="Use example input file (default: %(default)s)",
        default=False,
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
    inFile = "input.txt" if not args.example else "example.txt"
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
        result = part_1(data, log=log)
    elif args.part == 2:
        result = part_2(data, log=log)
    else:
        raise ValueError("Invalid part specified. Use 1 or 2.")
    if result is not None:
        print(f"Result for part {part}:\n {result}")
