"""
Advent of Code Utility Functions
Common patterns and helper functions for AoC problems.
"""

import argparse
import re
from collections import defaultdict, deque, Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from typing import List, Tuple, Dict, Set, Any, Optional


def day_parser():
    """Standard argument parser for AoC problems."""
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
    return parser


# Common parsing functions
def parse_ints(text: str) -> List[int]:
    """Extract all integers from a string."""
    return [int(x) for x in re.findall(r"-?\d+", text)]


def parse_grid(data: str) -> List[List[str]]:
    """Parse input into a 2D grid."""
    return [list(line) for line in data.strip().split("\n")]


def parse_blocks(data: str) -> List[str]:
    """Split input by blank lines."""
    return data.strip().split("\n\n")


def parse_lines(data: str) -> List[str]:
    """Split input into lines, removing empty lines."""
    return [line for line in data.strip().split("\n") if line]


# Grid utilities
def neighbors_4(row: int, col: int) -> List[Tuple[int, int]]:
    """Get 4-directional neighbors (up, down, left, right)."""
    return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]


def neighbors_8(row: int, col: int) -> List[Tuple[int, int]]:
    """Get 8-directional neighbors (including diagonals)."""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(row + dr, col + dc) for dr, dc in directions]


def in_bounds(row: int, col: int, grid: List[List[Any]]) -> bool:
    """Check if coordinates are within grid bounds."""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def print_grid(grid: List[List[Any]], separator: str = ""):
    """Pretty print a 2D grid."""
    for row in grid:
        print(separator.join(str(cell) for cell in row))


# Direction utilities
DIRECTIONS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "SE": (1, 1),
    "SW": (1, -1),
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def move(pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    """Move from position in given direction."""
    dr, dc = DIRECTIONS[direction]
    return (pos[0] + dr, pos[1] + dc)


def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculate Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Search algorithms
def bfs(start, neighbors_func, goal_func=None):
    """Generic BFS implementation."""
    queue = deque([start])
    visited = {start}
    distances = {start: 0}

    while queue:
        current = queue.popleft()

        if goal_func and goal_func(current):
            return current, distances[current]

        for neighbor in neighbors_func(current):
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return visited, distances


def dfs(start, neighbors_func, goal_func=None, visited=None):
    """Generic DFS implementation."""
    if visited is None:
        visited = set()

    visited.add(start)

    if goal_func and goal_func(start):
        return start

    for neighbor in neighbors_func(start):
        if neighbor not in visited:
            result = dfs(neighbor, neighbors_func, goal_func, visited)
            if result is not None:
                return result

    return None


# Math utilities
def gcd(a: int, b: int) -> int:
    """Greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Least common multiple."""
    return abs(a * b) // gcd(a, b)


def lcm_list(numbers: List[int]) -> int:
    """LCM of a list of numbers."""
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = lcm(result, numbers[i])
    return result


# Common data structures
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# Range utilities
def range_overlap(
    r1: Tuple[int, int], r2: Tuple[int, int]
) -> Optional[Tuple[int, int]]:
    """Find overlap between two ranges (inclusive)."""
    start = max(r1[0], r2[0])
    end = min(r1[1], r2[1])
    return (start, end) if start <= end else None


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Merge overlapping ranges."""
    if not ranges:
        return []

    ranges.sort()
    merged = [ranges[0]]

    for current in ranges[1:]:
        last = merged[-1]
        if current[0] <= last[1] + 1:  # Overlapping or adjacent
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    return merged


# Timing decorator
import time
from functools import wraps


def timer(func):
    """Decorator to time function execution."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


# Debug helpers
def debug_print(*args, enabled=True, **kwargs):
    """Conditional print for debugging."""
    if enabled:
        print(*args, **kwargs)


# Common regex patterns
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
NUMBER_PATTERN = r"-?\d+"
WORD_PATTERN = r"\b[A-Za-z]+\b"
