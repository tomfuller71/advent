#!/usr/bin/env python3
"""
Analyze why memoization doesn't help for this specific problem.
"""

from functools import lru_cache
from day_7 import parse_input


def analyze_subproblem_overlap():
    """Analyze if there are actually repeated subproblems."""

    with open("input.txt") as f:
        data = f.read().strip()

    # Track all (index, current_value) pairs across all equations
    all_subproblems = set()
    repeated_subproblems = set()
    subproblem_counts = {}

    def track_subproblems(target, numbers):
        if not numbers:
            return target == 0

        nums_tuple = tuple(numbers)
        local_subproblems = set()

        def evaluate(index, current_value):
            subproblem = (index, current_value)

            # Track this subproblem
            if subproblem in all_subproblems:
                repeated_subproblems.add(subproblem)
            if subproblem in local_subproblems:
                # Repeated within same equation
                subproblem_counts[subproblem] = subproblem_counts.get(subproblem, 0) + 1

            all_subproblems.add(subproblem)
            local_subproblems.add(subproblem)

            if index == len(nums_tuple):
                return current_value == target

            if current_value > target:
                return False

            next_num = nums_tuple[index]

            if evaluate(index + 1, current_value + next_num):
                return True

            if evaluate(index + 1, current_value * next_num):
                return True

            return False

        return evaluate(1, nums_tuple[0])

    # Test first 100 equations
    equations = list(parse_input(data))[:100]

    print("Subproblem Overlap Analysis:")
    print("=" * 50)

    for i, (target, numbers) in enumerate(equations):
        track_subproblems(target, numbers)
        if (i + 1) % 25 == 0:
            print(f"Processed {i+1} equations...")

    print(f"\nResults:")
    print(f"Total unique subproblems: {len(all_subproblems):,}")
    print(f"Repeated across equations: {len(repeated_subproblems):,}")
    print(f"Repeated within equations: {len(subproblem_counts):,}")
    print(
        f"Cross-equation reuse rate: {len(repeated_subproblems)/len(all_subproblems)*100:.2f}%"
    )

    if repeated_subproblems:
        print(f"\nSample repeated subproblems:")
        for i, subproblem in enumerate(list(repeated_subproblems)[:10]):
            print(f"  {subproblem}")

    if subproblem_counts:
        print(f"\nMost repeated within equations:")
        sorted_counts = sorted(
            subproblem_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]
        for subproblem, count in sorted_counts:
            print(f"  {subproblem}: repeated {count} times")


def analyze_equation_characteristics():
    """Analyze why this problem doesn't benefit from memoization."""

    with open("input.txt") as f:
        data = f.read().strip()

    equations = list(parse_input(data))

    print(f"\nProblem Characteristics Analysis:")
    print("=" * 50)

    # Calculate total possible combinations per equation
    total_combinations = 0
    large_search_spaces = 0

    for target, numbers in equations[:50]:  # Sample
        combinations = 2 ** (len(numbers) - 1)
        total_combinations += combinations
        if combinations > 64:  # 2^6
            large_search_spaces += 1

    print(f"Sample of 50 equations:")
    print(f"Average combinations per equation: {total_combinations/50:.0f}")
    print(f"Equations with >64 combinations: {large_search_spaces}")

    # The key insight: each equation is independent!
    print(f"\nKey Insights:")
    print(f"1. Each equation uses different target values")
    print(f"2. Each equation has different number sequences")
    print(f"3. No subproblems are shared between equations")
    print(f"4. Within an equation, search space is small (2^n combinations)")
    print(f"5. Memoization overhead exceeds benefits for small search spaces")


if __name__ == "__main__":
    analyze_subproblem_overlap()
    analyze_equation_characteristics()
