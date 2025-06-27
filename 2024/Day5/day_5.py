# This is a template for an Advent of Code problem solution.
# Replace the part_1 and part_2 functions with your actual logic.


def parse_input(data):
    ordered, updates = data.split("\n\n")
    ordered = {
        (int(x), int(y)) for line in ordered.splitlines() for x, y in [line.split("|")]
    }
    updates = [[int(n) for n in line.split(",")] for line in updates.splitlines()]
    return ordered, updates


def get_rules(orders: set[tuple[int, int]], update: list[int]):
    def filter_orders(order):
        x, y = order
        return x in update and y in update

    return [*filter(filter_orders, orders)]


def check_rules(orders: set[tuple[int, int]], update: list[int]):
    rules = get_rules(orders, update)
    for x, y in rules:
        order_position = update.index(x)
        update_position = update.index(y)
        if order_position > update_position:
            return False
    return True


def correct_update(orders: set[tuple[int, int]], update: list[int]) -> list[int]:
    rules = get_rules(orders, update)
    less_thans = {}
    for x, y in rules:
        if y not in less_thans:
            less_thans[y] = [x]
        else:
            less_thans[y].append(x)
    first = (set(update) - set(less_thans.keys())).pop()
    corrected_update = [
        first,
        *[
            entry[0]
            for entry in sorted(less_thans.items(), key=lambda item: len(item[1]))
        ],
    ]
    return corrected_update


def part_1(data):
    orders, updates = parse_input(data)
    sum_midddle_values = 0
    for update in updates:
        if check_rules(orders, update):
            middle_digit = update[len(update) // 2]
            sum_midddle_values += middle_digit
    return sum_midddle_values


def part_2(data):
    orders, updates = parse_input(data)
    sum_midddle_values = 0
    for update in updates:
        corrected_update = correct_update(orders, update)
        if any(x != y for x, y in zip(corrected_update, update)):
            print("Update corrected:", corrected_update)
            sum_midddle_values += corrected_update[len(corrected_update) // 2]

    return sum_midddle_values


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
        print("Data length:", len(data), "\n")
    if args.part == 1:
        result = part_1(data)
    elif args.part == 2:
        result = part_2(data)
    else:
        raise ValueError("Invalid part specified. Use 1 or 2.")
    if result is not None:
        print(f"Result for part {part}:\n {result}")
