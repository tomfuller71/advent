# This is a template for a boilerplate file for a new day of Advent of Code

# Part 1
'''
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

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

'''
# insert code below
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
    def coords(self):
        return (self.row, self.col)
    
    @property
    def is_start(self):
        return self.height == 0
    
    @property
    def is_end(self):
        return self.height == 27

    def __repr__(self) -> str:
        if self.is_start:
            return "S"
        elif self.is_end:
            return "E"
        else:
            return str(self.height)
    
    def __eq__(self, other: 'Position') -> bool:
        return self.row == other.row and self.col == other.col

class Direction(Enum):
    D = (1, 0)
    R = (0, 1)
    U = (-1, 0)
    L = (0,-1)
    
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
    def reverse(self):
        if self == Direction.D:
            return Direction.U
        elif self == Direction.U:
            return Direction.D
        elif self == Direction.L:
            return Direction.R
        else:
            return Direction.L
    
    def __repr__(self):
        return self.symbol


MapPoint = tuple[Direction, Position]

class HillMap:
    def __init__(self, data):
        self.positions, self.start, self.end = HillMap.parse_data(data)
        self.rows, self.cols = self.positions.shape
        self.size = self.positions.size
    
    def get_position(self, pos: Position, direction: Direction) -> Optional[Position]:
        row, col = pos.coords
        row_mvt, col_mvt = direction.value
        new_row, new_col = row + row_mvt, col + col_mvt
        if (0 <= new_col <= self.cols-1  and 0 <= new_row <= self.rows-1):
            return self.positions[new_row, new_col]
        else:
            return None

    def move_options(self, pos: Optional[Position], excluded: Optional[Direction]) -> list[MapPoint]:
        options = []
        if not pos: return options

        for direction in Direction:
            if direction is excluded: continue
            new_pos = self.get_position(pos, direction)
            if not new_pos: continue
            if 0 <= abs(new_pos.height - pos.height) <= 1:
                options.append((direction, new_pos))
        return options


    @classmethod
    def parse_data(cls, data) -> tuple[Array, Position, Position]:
        map = []
        start = Position(0,0,0)
        end = Position(0,0,0)
        for row, line in enumerate(data.strip().splitlines()):
            row_positions = []
            for col, letter in enumerate(line):
                position = Position(row, col, 0)
                if letter == "S":
                    start = position
                elif letter == "E":
                    position.height = 27
                    end = position
                else:
                    position.height = ord(letter) - 96
                row_positions.append(position)
            map.append(row_positions)
        return np.array(map), start, end
    
    def __repr__(self):
        return f'{self.positions}'

@dataclass
class Step:
    position: Position
    direction: Direction
    previous: Optional['Step'] = None

class Path:
    shape = (0,0)

    def __init__(self, step: Optional[Step] = None) -> None:
        self.current_step = step
        self.distance = 0 

    @property
    def isEmpty(self) -> bool:
        return self.current_step is None
    
    def add_step(self, direction, position) -> int:
        self.distance += 1
        next_step = Step(position, direction)
        if self.isEmpty:
            self.current_step = next_step
        else:
            next_step.previous = self.current_step
            self.current_step = next_step
        return self.distance

    def get_distance_to_pos(self, position: Position) -> Optional[int]:
        step = self.current_step
        distance = 0 
        while step:
            if step.position == position:
                return distance
            step = step.previous
            distance += 1
        return None

    
    # def is_better(self, position: Position, distance) -> bool:
    #     step = self.current_step
    #     while step:
    #         if step.position == position and step.distance <= distance:
    #             return True
    #         step = step.previous
    #     return False

    def __repr__(self):
        path_map = np.empty(Path.shape, dtype=str)
        path_map.fill(".")
        step = self.current_step
        while step:
            row, col = step.position.coords
            path_map[row, col] = step.direction.symbol
            step = step.previous
        return f'{path_map}'


class Solver:
    def __init__(self, map: HillMap) -> None:
        self.map = map
        self.distances: Array = np.zeros((map.rows, map.cols))
        self.distances.fill(map.size)
        self.open_paths: list[Path] = []
        self.completed_paths: list[Path] = []
        moves = self.map.move_options(map.start, excluded=None)
        for direction, position in moves:
            path = Path()
            path.add_step(direction, position)
            self.open_paths.append(path)
        
    def shortest_distance_to(self, pos: Position):
        return self.distances[pos.row, pos.col]

    def make_move(self, path: Path, move):
        


    def solve(self):
        while self.open_paths:
            selected = self.open_paths.pop()
            if not selected.current_step: continue
            curr_pos = selected.current_step.position
            exclude_dir = selected.current_step.direction.reverse
            distance = selected.distance + 1

            # Get possible moves
            moves = self.map.move_options(curr_pos, excluded=exclude_dir)
            # if dead end continue
            if not moves: continue
            
            end_found = False
            good_moves = []
            for new_dir, new_pos in moves:
                shortest = self.shortest_distance_to(pos)
             # check if a move at end if so append path to completed and break
                if new_pos is self.map.end:
                    _ = selected.add_step(new_dir, new_pos)
                    self.completed_paths.append(selected)
                    end_found = True
                    break
                else:
                    # check if shorter path to pos already exists


            if end_found : continue



            # if only one good good move then add that as next step to current path and continue
            # if more than one move pop the first and add that as next step to current then create new path based on the current path and ad those to the open_paths






            
                




class Route:
    def __init__(self, starting: Position, positions: Optional[list[Position]]=None, directions: Optional[list[Direction]] = None):
        self.current_position = starting
        self.positions = positions if positions else []
        self.directions = directions if directions else []
    
    @property
    def length(self) -> int:
        return len(self.positions)

    def visited(self, position):
        return position in self.positions

    def new_from(self, direction, position) -> 'Route':
        return Route(
            starting=position,
            positions=self.positions.copy() + [self.current_position],
            directions=self.directions.copy() + [direction]
            )

    def map_route_path(self, shape: tuple[int, int]) -> str:
        path_map = np.empty(shape, dtype=str)
        path_map.fill(".")
        for position, direction in zip(self.positions, self.directions):
            path_map[position.row, position.col] = direction.symbol
        return f'{path_map}'


class MapSolver:
    def __init__(self, height_map: HillMap) -> None:
        self.map = height_map
        self.completed_routes: list[Route] = []
        self.open_routes: list[Route] = []
        self.open_routes.append(Route(self.map.start))
    
    def get_new_routes_from(self, route: Route):
        options = self.map.explore_map_from(route.current_position)
        return [route.new_from(*option) for option in options]
    
    def solve(self):
        while self.open_routes:
            current_route = self.open_routes.pop()
            new_routes = self.get_new_routes_from(current_route)
            if not new_routes:
                print(f'Position {current_route.current_position.coords} is a dead end.')
            for route in new_routes:
                if route.current_position is self.map.end:
                    self.completed_routes.append(route)
                else:
                    self.open_routes.append(route)
        self.print_best_route()

    
    def print_best_route(self):
        route_lengths = [route.length for route in self.completed_routes]
        shortest = min(route_lengths)
        shortest_route_index = route_lengths.index(shortest)
        best_route = self.completed_routes[shortest_route_index]
        print(f'Shortest path to end is {shortest} steps.')
        print(best_route.map_route_path(self.map.positions.shape))


def main(data, logging):
    print('== Part 1 ==')
    map = HillMap(data)
    print(map)
    solver = MapSolver(map)
    solver.solve()

    print('== Part 2 ==')



if __name__ == '__main__':
    example = "Sabqponm\nabcryxxl\naccszExk\nacctuvwj\nabdefghi\n"
    TESTING = True
    # data_file = 'input.txt'
    # if TESTING:
    #     data_file = 'example.txt'

    # with open(data_file) as f:
    #     data = f.read()

    main(example, TESTING)