#!/usr/bin/env python3
"""
Analyze the characteristics of Day 7 input to understand memoization potential.
"""

import time
from collections import Counter
from day_7 import parse_input, canMakeTarget, canMakeTargetMemoized


def analyze_input_characteristics(data):
    """Analyze the input to understand memoization potential."""
    print("Input Analysis:")
    print("=" * 50)

    targets = []
    number_counts = []
    all_numbers = []

    for target, numbers in parse_input(data):
        targets.append(target)
        number_counts.append(len(numbers))
        all_numbers.extend(numbers)

    print(f"Total equations: {len(targets)}")
    print(f"Target range: {min(targets):,} to {max(targets):,}")
    print(
        f"Numbers per equation: {min(number_counts)} to {max(number_counts)} (avg: {sum(number_counts)/len(number_counts):.1f})"
    )
    print(f"Total numbers used: {len(all_numbers)}")
    print(f"Unique numbers: {len(set(all_numbers))}")
    print(f"Number range: {min(all_numbers)} to {max(all_numbers):,}")

    # Count frequency of number list lengths
    length_counts = Counter(number_counts)
    print(f"\nEquation lengths distribution:")
    for length in sorted(length_counts.keys()):
        print(f"  {length} numbers: {length_counts[length]} equations")

    # Count most common numbers
    number_freq = Counter(all_numbers)
    print(f"\nMost common numbers:")
    for num, count in number_freq.most_common(10):
        print(f"  {num}: appears {count} times")


def detailed_memoization_test(data, max_equations=None):
    """Test memoization with simpler analysis."""
    print(f"\nDetailed Memoization Analysis:")
    print("=" * 50)

    equations = list(parse_input(data))
    if max_equations:
        equations = equations[:max_equations]

    # Run both methods and compare
    methods = {"Optimized": canMakeTarget, "Memoized": canMakeTargetMemoized}

    results = {}

    for name, method_func in methods.items():
        start_time = time.perf_counter()
        correct_count = 0
        total_sum = 0

        for i, (target, numbers) in enumerate(equations):
            if method_func(target, numbers):
                correct_count += 1
                total_sum += target

            if (i + 1) % 100 == 0 and len(equations) > 100:
                print(f"{name}: Processed {i+1}/{len(equations)} equations...")

        end_time = time.perf_counter()

        results[name] = {
            "time": end_time - start_time,
            "correct_count": correct_count,
            "total_sum": total_sum,
        }

    print(f"\nResults for {len(equations)} equations:")
    for name, result in results.items():
        print(
            f"{name:12}: {result['total_sum']:,} in {result['time']:.4f}s ({result['correct_count']} solvable)"
        )

    if len(results) == 2:
        optimized_time = results["Optimized"]["time"]
        memoized_time = results["Memoized"]["time"]
        if memoized_time < optimized_time:
            improvement = (optimized_time - memoized_time) / optimized_time * 100
            print(f"Memoization is {improvement:.1f}% faster!")
        else:
            slowdown = (memoized_time - optimized_time) / optimized_time * 100
            print(f"Memoization is {slowdown:.1f}% slower")


def compare_scaling(data):
    """Compare how methods scale with different input sizes."""
    print(f"\nScaling Analysis:")
    print("=" * 50)

    equations = list(parse_input(data))
    test_sizes = [50, 100, 200, 400, len(equations)]

    methods = {"Optimized": canMakeTarget, "Memoized": canMakeTargetMemoized}

    for size in test_sizes:
        if size > len(equations):
            continue

        print(f"\nTesting with {size} equations:")
        test_equations = equations[:size]

        for name, method_func in methods.items():
            times = []

            # Run 3 times for average
            for _ in range(3):
                start_time = time.perf_counter()
                total = 0
                for target, numbers in test_equations:
                    if method_func(target, numbers):
                        total += target
                end_time = time.perf_counter()
                times.append(end_time - start_time)

            avg_time = sum(times) / len(times)
            print(f"  {name:12}: {avg_time:.4f}s")


if __name__ == "__main__":
    # Analyze example data
    with open("example.txt") as f:
        example_data = f.read().strip()

    print("EXAMPLE DATA:")
    analyze_input_characteristics(example_data)
    detailed_memoization_test(example_data)

    print("\n" + "=" * 70 + "\n")

    # Analyze full input data
    with open("input.txt") as f:
        input_data = f.read().strip()

    print("FULL INPUT DATA:")
    analyze_input_characteristics(input_data)
    detailed_memoization_test(input_data, max_equations=200)  # Test subset first
    compare_scaling(input_data)
