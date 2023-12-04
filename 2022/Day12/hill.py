# Part 1
'''
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z. [*** E HAS SAME VALUE AS Z - NOT HIGHER THAN Z ***]

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.) [*** E.G. YOU CAN GO DOWNWARDS FROM SAY C to A BUT CAN ONLY CLIMB UP BY ONE ***]

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
'''
# Part 2
'''
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?
'''




import numpy as np
from numpy.typing import NDArray as Array
from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Position:
    row: int
    col: int
    height: int

    @property
    def coords(self) -> tuple[int, int]:
        return (self.row, self.col)

    def __repr__(self) -> str:
        return str(self.height)

    def __eq__(self, __o: 'Position') -> bool:
        return self.row == __o.row and self.col == __o.col


class Direction(Enum):
    D = (1, 0)
    R = (0, 1)
    U = (-1, 0)
    L = (0, -1)

    @property
    def symbol(self):
        if self == Direction.D:
            return 'v'
        elif self == Direction.U:
            return '^'
        elif self == Direction.L:
            return '<'
        else:
            return '>'
    @property
    def reverse(self) -> 'Direction':
        if self == Direction.D:
            return Direction.U
        elif self == Direction.U:
            return Direction.D
        elif self == Direction.L:
            return Direction.R
        else:
            return Direction.L

    def __repr__(self) -> str:
        return self.symbol


Move = tuple[Direction, Position]
Path = list[Move]


class HillMap:
    def __init__(self, data):
        self.positions, self.start, self.end, self.lowest = HillMap.parse(data)
        self.rows, self.cols = self.positions.shape
        self.size = self.positions.size

    def get_position(self, pos: Position, direction: Direction) -> Optional[Position]:
        row, col = pos.coords
        row_mvt, col_mvt = direction.value
        new_row, new_col = row + row_mvt, col + col_mvt
        if (0 <= new_col <= self.cols-1 and 0 <= new_row <= self.rows-1):
            return self.positions[new_row, new_col]
        else:
            return None

    def get_moves(self, pos: Optional[Position], reverse) -> list[Move]:
        options: list[Move] = []
        if not pos:
            return options
        for direction in Direction:
            new_pos = self.get_position(pos, direction)
            if not reverse and new_pos and new_pos.height - pos.height <= 1:
                options.append((direction, new_pos))
            elif reverse and new_pos and pos.height - new_pos.height <= 1:
                options.append((direction, new_pos))
        return options

    @classmethod
    def parse(cls, data) -> tuple[Array, Position, Position, list[Position]]:
        map = []
        lowest_positions = []
        start, end = Position(0, 0, 0), Position(0, 0, 0)
        for row, line in enumerate(data.strip().splitlines()):
            row_positions = []
            for col, letter in enumerate(line):
                position = Position(row, col, 0)
                if letter == "S":
                    position.height = 1
                    start = position
                elif letter == "E":
                    position.height = 26
                    end = position
                else:
                    position.height = ord(letter) - 96

                if letter == 'S' or letter == 'a':
                    lowest_positions.append(position)
                row_positions.append(position)

            map.append(row_positions)
        return np.array(map), start, end, lowest_positions

    def get_map_array(self):
        map = self.positions.copy().astype(str)
        map[self.start.row, self.start.col] = 'S'
        map[self.end.row, self.end.col] = 'E'
        return map

    def __repr__(self) -> str:
        return f'{self.get_map_array()}'

def reverse_path(path: Path) -> Path:
    return [(move[0].reverse, move[1]) for move in reversed(path)]

def solve_map(map: HillMap, reverse=False):
    distances: Array = np.zeros((map.rows, map.cols))
    distances.fill(map.size)
    open_paths: list[Path] = [[move] for move in map.get_moves(map.end if reverse else map.start, reverse)]
    shortest_path: Path = []
    shortest_path_length = map.size
    endpoints: list[Position] = map.lowest if reverse else [map.end]

    while open_paths:
        current_path = open_paths.pop()
        new_distance = len(current_path) + 1
        moves = map.get_moves(current_path[-1][1], reverse)
        end_found = False
        good_moves = []
        for new_dir, new_pos in moves:
            # Stop if end found
            if new_pos in endpoints:
                if shortest_path_length > new_distance:
                    shortest_path = current_path
                    shortest_path_length = new_distance
                end_found = True
                break
            else:
                # Not good move if can get to same pos in less steps
                shortest = distances[new_pos.row, new_pos.col]
                if new_distance < shortest:
                    distances[new_pos.row, new_pos.col] = new_distance
                    good_moves.append((new_dir, new_pos))

        if not end_found:
            open_paths.extend(current_path + [move] for move in good_moves)
        
    if reverse:
        shortest_path = reverse_path(shortest_path)

    return shortest_path_length, shortest_path

# Not required to solve but replicates example solution
def get_map_path(map: HillMap, path: Path):
    path_map = np.empty_like(map.positions)
    path_map.fill(".")
    path_map[map.end.row, map.end.col] = 'E'

    for direction, position in path:
        path_map[position.row, position.col] = direction.symbol

    path_str = ""
    for i in range(map.rows):
        path_str += "".join(path_map[i]) + "\n"

    return path_str


def main(data, logging):
    map = HillMap(data)

    print('== Part 1 ==')
    steps, path = solve_map(map, reverse=False)
    path_str = get_map_path(map, path)
    print(f'The best path is {steps} steps.')
    with open("part1_solution.txt", "w") as file:
        file.write(path_str)

    print('== Part 2 ==')
    steps, path = solve_map(map, reverse=True)
    path_str = get_map_path(map, path)
    print(f'The best path is {steps} steps.')
    with open("part2_solution.txt", "w") as file:
        file.write(path_str)


if __name__ == '__main__':
    TESTING = False
    data_file = 'input.txt'
    if TESTING:
        data_file = 'example.txt'

    with open(data_file) as f:
        data = f.read()

    main(data, TESTING)

