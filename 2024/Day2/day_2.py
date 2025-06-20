# This is a template for an Advent of Code problem solution.
# Replace the part_1 and part_2 functions with your actual logic.


from calendar import c


def parse_input(data):
    lines = []
    for line in data.splitlines():
        nums = [int(num) for num in line.split()]
        lines.append(nums)
    return lines


def part_1(data):
    # Implement part 1 logic here
    lines = parse_input(data)
    margin = 3
    count_unsafe = 0
    for line in lines:
        is_asc = False
        is_dec = False
        for i in range(1, len(line)):
            prior = line[i - 1]
            current = line[i]
            if prior == current:
                count_unsafe += 1
                print(
                    f"Line: {line} Prior: {prior}, Current: {current} - Unsafe - values are equal"
                )
                break
            elif current > prior:
                is_asc = True
                if is_dec:
                    count_unsafe += 1
                    print(
                        f"Line: {line} Prior: {prior}, Current: {current} - Unsafe - ascending after descending"
                    )
                    break
                elif (current - prior) > margin:
                    count_unsafe += 1
                    print(
                        f"Line: {line} Prior: {prior}, Current: {current} - Unsafe - difference of {current - prior}"
                    )
                    break
            else:
                is_dec = True
                if is_asc:
                    count_unsafe += 1
                    print(
                        f"Line: {line} Prior: {prior}, Current: {current} - Unsafe - descending after ascending"
                    )
                    break
                elif (prior - current) > margin:
                    count_unsafe += 1
                    print(
                        f"Line: {line} Prior: {prior}, Current: {current} - Unsafe - difference of {prior - current}"
                    )
                    break
    print(f"Count of unsafe lines: {count_unsafe}")
    print(f"Count of safe lines: {len(lines) - count_unsafe}")
    return len(lines) - count_unsafe


def faulty_line_index(line: list[int]) -> int | None:
    asc = False
    desc = False
    for i in range(1, len(line)):
        prior = line[i - 1]
        current = line[i]
        if current > prior:
            asc = True
        elif current < prior:
            desc = True
        if prior == current or abs(current - prior) > 3 or asc and desc:
            return i
    return None


def part_2(data):
    # Implement part 1 logic here
    lines = parse_input(data)
    safe_count = 0

    for line in lines:
        fault_at = faulty_line_index(line)
        if fault_at is None:
            safe_count += 1
        else:
            alt_lines = [
                [*line[:fault_at], *line[fault_at + 1 :]],  # Remove fault
                [*line[: fault_at - 1], *line[fault_at:]],  # Remove prior
                [*line[: fault_at - 2], *line[fault_at - 1 :]],  # Remove prior prior
            ]
            print(f"Alternative lines: {alt_lines}")
            safe = False
            for alt_line in alt_lines:
                if faulty_line_index(alt_line) is None:
                    safe = True
                    print(f"Line: {line} - Safe after dampening with {alt_line}")
                    break
            if safe:
                # Dampening the line by removing the fault or prior values
                safe_count += 1
            else:
                print(f"Line: {line} - Unsafe after dampening")

    print(f"Count of safe lines: {safe_count}")
    return safe_count


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
        default="example.txt",
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

"""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
