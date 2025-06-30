#!/usr/bin/env python3
"""
Benchmark different implementations of the Day 7 solution.
"""

import time
from day_7 import (
    parse_input,
    canMakeTarget,
    canMakeTargetIterative,
    canMakeTargetMemoized,
)


def original_canMakeTarget(target, numbers):
    """
    Original implementation from the user's code.
    """
    if len(numbers) == 0:
        return target == 0
    if len(numbers) == 1:
        return target == numbers[0]
    if len(numbers) == 2:
        a, b = numbers
        return target == a + b or target == a * b
    else:
        first, second, *rest = numbers
        multiplied = first * second
        added = first + second
        new_nums_added = [added] + rest
        new_nums_multiplied = [multiplied] + rest
        if original_canMakeTarget(target, new_nums_added) or original_canMakeTarget(
            target, new_nums_multiplied
        ):
            return True
    return False


def solve_with_method(data, method_func):
    """Solve using a specific method function."""
    total = 0
    for target, numbers in parse_input(data):
        if method_func(target, numbers):
            total += target
    return total


def benchmark_methods(data, runs=5):
    """
    Compare performance of different methods.
    """
    methods = {
        "Original": original_canMakeTarget,
        "Optimized": canMakeTarget,
        "Iterative": canMakeTargetIterative,
        "Memoized": canMakeTargetMemoized,
    }

    print("Performance Comparison:")
    print("=" * 50)

    for name, method_func in methods.items():
        times = []
        result = None

        for _ in range(runs):
            start_time = time.perf_counter()
            result = solve_with_method(data, method_func)
            end_time = time.perf_counter()
            times.append(end_time - start_time)

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(
            f"{name:12}: {result:6} | Avg: {avg_time:.6f}s | Min: {min_time:.6f}s | Max: {max_time:.6f}s"
        )


if __name__ == "__main__":
    # Test with example data
    with open("example.txt") as f:
        example_data = f.read().strip()

    print("Benchmarking with example data:")
    benchmark_methods(example_data)

    print("\n" + "=" * 50)

    # Test with actual input if available
    try:
        with open("input.txt") as f:
            input_data = f.read().strip()
        print("Benchmarking with actual input data:")
        benchmark_methods(input_data, runs=3)  # Fewer runs for larger input
    except FileNotFoundError:
        print("input.txt not found, skipping full input benchmark")
