#!/usr/bin/env python3
"""
Solution runner for Advent of Code problems.
Provides easy testing and execution of solutions.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path


def find_solution_file(day_dir):
    """Find the main solution file in a day directory."""
    day_path = Path(day_dir)

    # Look for common patterns
    patterns = [
        f"day_{day_path.name.lower().replace('day', '')}.py",
        f"day{day_path.name.lower().replace('day', '')}.py",
        "solution.py",
        "main.py",
    ]

    for pattern in patterns:
        candidate = day_path / pattern
        if candidate.exists():
            return candidate

    # If no pattern matches, look for any .py file that's not aoc_utils.py
    py_files = [f for f in day_path.glob("*.py") if f.name != "aoc_utils.py"]
    if len(py_files) == 1:
        return py_files[0]
    elif len(py_files) > 1:
        print(f"Multiple Python files found in {day_dir}:")
        for i, f in enumerate(py_files):
            print(f"  {i+1}. {f.name}")
        choice = input("Which file to run? (number): ")
        try:
            return py_files[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice")
            return None

    return None


def run_solution(solution_file, part=None, example=False, log=False):
    """Run a solution file with the given parameters."""
    cmd = ["python3", str(solution_file)]

    if part:
        cmd.extend(["-p", str(part)])
    if example:
        cmd.append("-e")
    if log:
        cmd.append("-l")

    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, cwd=solution_file.parent, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running solution: {e}")
        return False


def test_solution(day_dir):
    """Test a solution against both example and actual input."""
    solution_file = find_solution_file(day_dir)
    if not solution_file:
        print(f"No solution file found in {day_dir}")
        return False

    print(f"Testing solution: {solution_file}")

    # Test Part 1 with example
    print("\n=== Part 1 (Example) ===")
    success = run_solution(solution_file, part=1, example=True, log=True)

    if success:
        print("\n=== Part 1 (Actual) ===")
        run_solution(solution_file, part=1, example=False)

        print("\n=== Part 2 (Example) ===")
        success = run_solution(solution_file, part=2, example=True, log=True)

        if success:
            print("\n=== Part 2 (Actual) ===")
            run_solution(solution_file, part=2, example=False)


def benchmark_solution(day_dir, runs=5):
    """Benchmark a solution by running it multiple times."""
    solution_file = find_solution_file(day_dir)
    if not solution_file:
        print(f"No solution file found in {day_dir}")
        return

    import time

    for part in [1, 2]:
        times = []
        print(f"\nBenchmarking Part {part} ({runs} runs)...")

        for i in range(runs):
            start = time.time()
            cmd = ["python3", str(solution_file), "-p", str(part)]
            subprocess.run(cmd, cwd=solution_file.parent, capture_output=True)
            end = time.time()
            times.append(end - start)
            print(f"  Run {i+1}: {times[-1]:.4f}s")

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"  Average: {avg_time:.4f}s")
        print(f"  Min: {min_time:.4f}s")
        print(f"  Max: {max_time:.4f}s")


def main():
    parser = argparse.ArgumentParser(
        description="Run and test Advent of Code solutions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("day", nargs="?", type=int, help="Day number to run")
    parser.add_argument(
        "-y", "--year", type=int, help="Year (default: current directory year)"
    )
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], help="Part to run")
    parser.add_argument(
        "-e", "--example", action="store_true", help="Use example input"
    )
    parser.add_argument("-l", "--log", action="store_true", help="Enable logging")
    parser.add_argument(
        "-t", "--test", action="store_true", help="Test solution with both inputs"
    )
    parser.add_argument(
        "-b", "--benchmark", action="store_true", help="Benchmark solution"
    )
    parser.add_argument("--list", action="store_true", help="List available days")

    args = parser.parse_args()

    # Determine year and day directory
    if args.year:
        year_dir = Path(f"{args.year}")
    else:
        # Try to determine year from current directory
        cwd = Path.cwd()
        if cwd.name.isdigit():
            year_dir = cwd
        elif cwd.parent.name.isdigit():
            year_dir = cwd.parent
        else:
            print(
                "Could not determine year. Please specify with -y or run from a year directory."
            )
            return 1

    if not year_dir.exists():
        print(f"Year directory {year_dir} does not exist")
        return 1

    # List available days
    if args.list:
        day_dirs = sorted(
            [d for d in year_dir.iterdir() if d.is_dir() and d.name.startswith("Day")]
        )
        print(f"Available days in {year_dir}:")
        for day_dir in day_dirs:
            solution_file = find_solution_file(day_dir)
            status = "✅" if solution_file else "❌"
            print(f"  {status} {day_dir.name}")
        return 0

    if not args.day:
        print("Please specify a day number or use --list to see available days")
        return 1

    day_dir = year_dir / f"Day{args.day}"
    if not day_dir.exists():
        print(f"Day directory {day_dir} does not exist")
        return 1

    # Run the appropriate action
    if args.benchmark:
        benchmark_solution(day_dir)
    elif args.test:
        test_solution(day_dir)
    else:
        solution_file = find_solution_file(day_dir)
        if solution_file:
            run_solution(solution_file, args.part, args.example, args.log)
        else:
            print(f"No solution file found in {day_dir}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
