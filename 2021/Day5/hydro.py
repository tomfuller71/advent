'''
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
'''
import sys
import re
import numpy as np
from dataclasses import dataclass


@dataclass
class Point:
    col: int
    row: int

    def __repr__(self):
        return f'Point(col:{self.col}, row:{self.row})'


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def get_diag_cells(self):
        cols = self.get_range(self.p1.col, self.p2.col)
        rows = self.get_range(self.p1.row, self.p2.row)
        return zip(cols, rows)

    def get_min_max(self):
        rows, cols = (self.p1.row, self.p2.row), (self.p1.col, self.p2.col)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        return min_row, max_row, min_col, max_col

    def __repr__(self):
        return f'Line({self.p1}, {self.p2}, {self.is_diagonal})'

    @property
    def is_diagonal(self):
        return not (self.p1.col == self.p2.col or self.p1.row == self.p2.row)

    @staticmethod
    def get_range(val1, val2):
        step = 1 if val1 < val2 else -1
        return range(val1, val2 + step, step)


class Map:
    def __init__(self, lines: list[Line], allow_diag=False):
        self.allow_diag = allow_diag
        col_vals = []
        row_vals = []
        for line in lines:
            col_vals.extend([line.p1.col, line.p2.col])
            row_vals.extend([line.p1.row, line.p2.row])
        self.map = np.zeros((max(row_vals) + 1, max(col_vals) + 1), dtype=int)
        self.add_lines_to_map(lines)

    def add_lines_to_map(self, lines: list[Line]):
        for line in lines:
            if line.is_diagonal:
                if not self.allow_diag: continue
                for col, row in line.get_diag_cells():
                    self.map[row, col] += 1
            else:
                min_row, max_row, min_col, max_col = line.get_min_max()
                self.map[min_row: max_row + 1, min_col: max_col + 1] += 1

    def number_line_intersects(self):
        return np.sum(np.where(self.map > 1, 1, 0))


def parse_data(data: str):
    line_data = data.splitlines()
    lines = []
    for line in line_data:
        matches = re.findall(r'(\d+)', line)
        numbers = [int(num) for num in matches]
        if numbers:
            p1 = Point(*numbers[:2])
            p2 = Point(*numbers[2:])
            lines.append(Line(p1, p2))
    return lines

'''
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
'''

def main(data: str):
    lines = parse_data(data)
    map = Map(lines)
    print(f'Part 1: Number of intersects: {map.number_line_intersects()}')
    map = Map(lines, allow_diag=True)
    print(f'Part 2: Number of intersects: {map.number_line_intersects()}')


if __name__ == "__main__":
    datafile = 'example.txt'
    if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
        datafile = sys.argv[1]
    with open(datafile) as f:
        data = f.read()
        main(data)
