#!/usr/bin/env python3
"""
Advent of Code Performance Analysis
Track and compare solution performance across days and years.
"""
import json
import os
import subprocess
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class PerformanceTracker:
    def __init__(self, data_file="performance.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """Load existing performance data."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {}

    def save_data(self):
        """Save performance data to file."""
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def record_performance(self, year, day, part, runtime, result=None):
        """Record a performance measurement."""
        key = f"{year}-{day}"
        if key not in self.data:
            self.data[key] = {}

        if f"part_{part}" not in self.data[key]:
            self.data[key][f"part_{part}"] = []

        entry = {
            "timestamp": datetime.now().isoformat(),
            "runtime": runtime,
            "result": result,
        }

        self.data[key][f"part_{part}"].append(entry)
        self.save_data()

    def get_best_times(self, year=None):
        """Get best times for each problem."""
        results = {}
        for key, day_data in self.data.items():
            year_day, day_num = key.split("-")
            if year and int(year_day) != year:
                continue

            results[key] = {}
            for part, measurements in day_data.items():
                if measurements:
                    best_time = min(m["runtime"] for m in measurements)
                    results[key][part] = best_time

        return results

    def print_summary(self, year=None):
        """Print a summary of performance data."""
        best_times = self.get_best_times(year)

        print(f"Performance Summary{' for ' + str(year) if year else ''}")
        print("=" * 50)

        total_time = 0
        problem_count = 0

        for key in sorted(best_times.keys()):
            year_day, day_num = key.split("-")
            print(f"\nDay {day_num} ({year_day}):")

            day_total = 0
            for part in ["part_1", "part_2"]:
                if part in best_times[key]:
                    runtime = best_times[key][part]
                    day_total += runtime
                    print(f"  {part}: {runtime:.4f}s")
                    problem_count += 1

            if day_total > 0:
                total_time += day_total
                print(f"  Total: {day_total:.4f}s")

        if problem_count > 0:
            print(f"\nOverall Statistics:")
            print(f"  Total problems solved: {problem_count}")
            print(f"  Total runtime: {total_time:.4f}s")
            print(f"  Average per problem: {total_time/problem_count:.4f}s")


def benchmark_solution(solution_file, runs=3):
    """Benchmark a solution file."""
    if not solution_file.exists():
        return None

    results = {}

    for part in [1, 2]:
        times = []
        result = None

        for _ in range(runs):
            cmd = ["python3", str(solution_file), "-p", str(part)]
            start_time = time.time()

            try:
                process = subprocess.run(
                    cmd,
                    cwd=solution_file.parent,
                    capture_output=True,
                    text=True,
                    timeout=30,  # 30 second timeout
                )
                end_time = time.time()

                if process.returncode == 0:
                    times.append(end_time - start_time)
                    # Extract result from output
                    output_lines = process.stdout.strip().split("\n")
                    for line in output_lines:
                        if line.startswith("Result for Part"):
                            result = line.split(": ", 1)[1] if ": " in line else None
                            break
                else:
                    print(f"Error in part {part}: {process.stderr}")

            except subprocess.TimeoutExpired:
                print(f"Part {part} timed out (>30s)")
                break
            except Exception as e:
                print(f"Error running part {part}: {e}")
                break

        if times:
            results[f"part_{part}"] = {
                "best_time": min(times),
                "avg_time": sum(times) / len(times),
                "result": result,
            }

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Advent of Code Performance Analysis")
    parser.add_argument("-y", "--year", type=int, help="Year to analyze")
    parser.add_argument("-d", "--day", type=int, help="Day to benchmark")
    parser.add_argument(
        "--benchmark-all", action="store_true", help="Benchmark all solutions"
    )
    parser.add_argument(
        "--summary", action="store_true", help="Show performance summary"
    )
    parser.add_argument(
        "--runs", type=int, default=3, help="Number of runs for benchmarking"
    )

    args = parser.parse_args()

    tracker = PerformanceTracker()

    if args.summary:
        tracker.print_summary(args.year)
        return

    if args.benchmark_all:
        # Find all solution files
        base_dir = Path(".")
        year_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.isdigit()]

        if args.year:
            year_dirs = [d for d in year_dirs if int(d.name) == args.year]

        for year_dir in sorted(year_dirs):
            year = int(year_dir.name)
            print(f"\nBenchmarking {year}...")

            day_dirs = sorted(
                [
                    d
                    for d in year_dir.iterdir()
                    if d.is_dir() and d.name.startswith("Day")
                ]
            )

            for day_dir in day_dirs:
                day_num = int(day_dir.name.replace("Day", ""))

                # Find solution file
                solution_files = [
                    f for f in day_dir.glob("*.py") if f.name != "aoc_utils.py"
                ]
                if not solution_files:
                    continue

                solution_file = solution_files[0]  # Take the first one
                print(f"  Day {day_num}: ", end="", flush=True)

                results = benchmark_solution(solution_file, args.runs)
                if results:
                    for part_key, part_data in results.items():
                        part_num = int(part_key.split("_")[1])
                        tracker.record_performance(
                            year,
                            day_num,
                            part_num,
                            part_data["best_time"],
                            part_data["result"],
                        )

                    part1_time = results.get("part_1", {}).get("best_time", 0)
                    part2_time = results.get("part_2", {}).get("best_time", 0)
                    total_time = part1_time + part2_time
                    print(f"{total_time:.4f}s")
                else:
                    print("Failed")

    elif args.day:
        # Benchmark specific day
        year = args.year or datetime.now().year
        day_dir = Path(f"{year}/Day{args.day}")

        if not day_dir.exists():
            print(f"Day directory {day_dir} does not exist")
            return 1

        solution_files = [f for f in day_dir.glob("*.py") if f.name != "aoc_utils.py"]
        if not solution_files:
            print(f"No solution file found in {day_dir}")
            return 1

        solution_file = solution_files[0]
        print(f"Benchmarking {solution_file}...")

        results = benchmark_solution(solution_file, args.runs)
        if results:
            for part_key, part_data in results.items():
                part_num = int(part_key.split("_")[1])
                print(
                    f"Part {part_num}: {part_data['best_time']:.4f}s (avg: {part_data['avg_time']:.4f}s)"
                )
                if part_data["result"]:
                    print(f"  Result: {part_data['result']}")

                tracker.record_performance(
                    year,
                    args.day,
                    part_num,
                    part_data["best_time"],
                    part_data["result"],
                )
    else:
        tracker.print_summary(args.year)


if __name__ == "__main__":
    main()
