# This is a template for an Advent of Code problem solution.
# Replace the part_1 and part_2 functions with your actual logic.


"""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def parse_input(data):
    """
    Parse the input data into a suitable format.
    This function should be modified based on the specific problem requirements.
    """
    # Example parsing logic (modify as needed)
    for line in data.splitlines():
        target_str, numbers_str = line.split(":")
        target = int(target_str.strip())
        numbers_list = [
            int(num.strip()) for num in numbers_str.split(" ") if num.strip().isdigit()
        ]
        yield target, numbers_list


def part2_canMakeTarget(target, numbers):
    """
    Original implementation from the user's code.
    """
    if len(numbers) == 0:
        return target == 0
    if len(numbers) == 1:
        return target == numbers[0]
    if len(numbers) == 2:
        a, b = numbers
        return target == a + b or target == a * b or target == int(str(a) + str(b))
    else:
        first, second, *rest = numbers
        multiplied = first * second
        added = first + second
        new_nums_added = [added] + rest
        new_nums_multiplied = [multiplied] + rest
        new_nums_concatenated = [int(str(first) + str(second))] + rest
        if (
            part2_canMakeTarget(target, new_nums_added)
            or part2_canMakeTarget(target, new_nums_multiplied)
            or part2_canMakeTarget(target, new_nums_concatenated)
        ):
            return True
    return False


def canMakeTarget(target, numbers):
    """
    Check if the target can be made from the given numbers using + and * operators.
    Optimized version using forward evaluation with early termination.
    """
    if not numbers:
        return target == 0

    def evaluate(index, current_value):
        # Base case: processed all numbers
        if index == len(numbers):
            return current_value == target

        # Early termination: if current value exceeds target, no point in continuing
        # (since we can only add or multiply positive numbers)
        if current_value > target:
            return False

        next_num = numbers[index]

        # Try addition
        if evaluate(index + 1, current_value + next_num):
            return True

        # Try multiplication
        if evaluate(index + 1, current_value * next_num):
            return True

        return False

    # Start with the first number
    return evaluate(1, numbers[0])


def canMakeTargetIterative(target, numbers):
    """
    Alternative iterative approach using bit manipulation to try all operator combinations.
    More memory efficient for smaller inputs.
    """
    if not numbers:
        return target == 0
    if len(numbers) == 1:
        return target == numbers[0]

    # For n numbers, we need n-1 operators
    num_operators = len(numbers) - 1

    # Try all 2^(n-1) combinations of operators (0 = +, 1 = *)
    for mask in range(1 << num_operators):
        result = numbers[0]

        for i in range(num_operators):
            if mask & (1 << i):  # Bit is 1, use multiplication
                result *= numbers[i + 1]
            else:  # Bit is 0, use addition
                result += numbers[i + 1]

            # Early termination if result exceeds target
            if result > target:
                break

        if result == target:
            return True

    return False


def canMakeTargetMemoized(target, numbers):
    """
    Memoized version using forward evaluation.
    """
    from functools import lru_cache

    if not numbers:
        return target == 0

    nums_tuple = tuple(numbers)

    @lru_cache(maxsize=None)
    def evaluate(index, current_value):
        if index == len(nums_tuple):
            return current_value == target

        if current_value > target:
            return False

        next_num = nums_tuple[index]

        # Try addition
        if evaluate(index + 1, current_value + next_num):
            return True

        # Try multiplication
        if evaluate(index + 1, current_value * next_num):
            return True

        return False

    return evaluate(1, nums_tuple[0])


def part_1(data, log=False, method="backtrack"):
    """
    Solve part 1 with different optimization methods.
    Methods: 'backtrack', 'iterative', 'memoized'
    """
    sum_canMake_target = 0

    # Choose the method
    if method == "iterative":
        solve_func = canMakeTargetIterative
    elif method == "memoized":
        solve_func = canMakeTargetMemoized
    else:
        solve_func = canMakeTarget

    for target, numbers in parse_input(data):
        if log:
            print(f"Checking target {target} with numbers {numbers}")
        if solve_func(target, numbers):
            if log:
                print(f"Target {target} can be made from {numbers}")
            sum_canMake_target += target

    return sum_canMake_target


def benchmark_methods(data):
    """
    Compare performance of different methods.
    """
    import time

    methods = ["backtrack", "iterative", "memoized"]
    results = {}

    for method in methods:
        start_time = time.time()
        result = part_1(data, log=False, method=method)
        end_time = time.time()

        results[method] = {"result": result, "time": end_time - start_time}
        print(f"{method:12}: {result:6} (Time: {end_time - start_time:.4f}s)")

    return results


def part_2(data, log=False):
    sum_canMake_target = 0
    for target, numbers in parse_input(data):
        # if log:
        #     print(f"Checking target {target} with numbers {numbers}")
        if part2_canMakeTarget(target, numbers):
            if log:
                print(f"Target {target} can be made from {numbers}")
            sum_canMake_target += target
        else:
            if log:
                print(f"Target {target} cannot be made from {numbers}")
    if log:
        print(f"Total sum of targets that can be made: {sum_canMake_target}")
    return sum_canMake_target


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
        default=1,
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
