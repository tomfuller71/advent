from enum import Enum
from math import e
from turtle import st

from matplotlib.widgets import RangeSlider
from regex import F

from aoc_utils import day_parser


class Move(Enum):
    U = (-1, 0)
    D = (1, 0)
    L = (0, -1)
    R = (0, 1)

    def reverse(self):
        if self == Move.U:
            return Move.D
        elif self == Move.D:
            return Move.U
        elif self == Move.L:
            return Move.R
        else:
            return Move.L


CONNECTIONS = {
    ".": tuple(),
    "|": (Move.U, Move.D),
    "-": (Move.L, Move.R),
    "L": (Move.U, Move.R),
    "J": (Move.U, Move.L),
    "7": (Move.D, Move.L),
    "F": (Move.D, Move.R),
    "S": (Move.U, Move.D, Move.L, Move.R),
}

TURNS = ["LJ", "F7"]


class Tile:
    def __init__(self, pos: tuple[int, int], char: str):
        self.pos = pos
        self.connections = CONNECTIONS[char]
        self.char = char
        self.loop = False
        self.inside_row = False
        self.inside_col = False

    @property
    def enclosed(self):
        return self.inside_row and self.inside_col

    @property
    def reverse_connections(self):
        return [c.reverse() for c in self.connections]

    def can_connect(self, other: "Tile"):
        if self.char == ".":
            return False
        if self.char == "S":
            return True
        if any([c in self.connections for c in other.reverse_connections]):
            return True

    def invalidate(self):
        self.connections = []
        self.char = "."

    def __repr__(self):
        return f"Tile({self.pos}, {self.connections}, {self.char}, {self.loop})"


class Maze:
    def __init__(self, data: str):
        self.maze = self.parse_data(data)
        self.start = self.starting_tile()
        self.marked_loop = False
        self.loop_length = self.search_max_distance_from_start()
        self.enclosed = self.count_enclosed()

        rows, cols = len(self.maze) - 2, len(self.maze[0]) - 2
        print(f"Maze size: {rows}x{cols} = {rows * cols}")

    def search_max_distance_from_start(self):
        loop_count = 0
        tile = self.start
        # S guarantees 2 valid connections - can go either way round the loop
        heading = self.valid_connections(tile)[0]
        while True:
            tile.loop = True
            next, heading = self.get_tile_and_heading(tile, heading)
            tile = next
            loop_count += 1
            if next is self.start:
                break
        self.marked_loop = True
        return loop_count // 2

    def char_of_start(self):
        valid = self.valid_connections(self.start)
        valid = (valid[0], valid[1])
        for key, value in CONNECTIONS.items():
            if value == valid:
                return key
        raise ValueError("No valid char found for start.")

    def enclosed_ranges(self, slice: list[Tile], is_row=True):
        passthrough = "-" if is_row else "|"  # char of tiles don't end range
        tiles = [tile for tile in slice if tile.loop]
        if len(tiles) < 2:
            return []
        r_c = 1 if is_row else 0
        passthroughs = "-J7" if is_row else "|JL"
        ranges = []
        i = 0
        while i < len(tiles):
            while i < len(tiles) - 1 and tiles[i + 1].char in passthroughs:
                i += 1
                did_pass = True
            if i >= len(tiles) - 1:
                break

            start = tiles[i].pos[r_c]
            end = tiles[i+1].pos[r_c]
            ranges.append((start, end))
            i += 1
        return ranges

    def count_enclosed(self):
        self.mark_as_enclosed()
        enclosed = 0
        for row in self.maze:
            for tile in row:
                if tile.enclosed:
                    enclosed += 1
        return enclosed

    def mark_as_enclosed(self):

        def within_ranges(ranges, i):
            for start, end in ranges:
                if start <= i < end:
                    return True
            return False
        
        start_char = self.char_of_start()
        self.start.char = start_char

        row_enclosed_ranges = [self.enclosed_ranges(row) for row in self.maze]
        col_enclosed_ranges = [
            self.enclosed_ranges([row[i] for row in self.maze])
            for i in range(len(self.maze[0]))
        ]

        for i, row in enumerate(self.maze):
            for j, tile in enumerate(row):
                if tile.loop:
                    continue
                tile.inside_row = within_ranges(row_enclosed_ranges[i], j)
                tile.inside_col = within_ranges(col_enclosed_ranges[j], i)

        self.start.char = "S"
        return None

    def get_tile_and_heading(self, tile, heading: Move):
        next_t = self.get_tile_in_dir(tile, heading)
        first, second = next_t.connections[0], next_t.connections[1]
        heading = first if first != heading.reverse() else second
        return next_t, heading

    def get_tile(self, pos: tuple[int, int]):
        return self.maze[pos[0]][pos[1]]

    def get_tile_in_dir(self, tile, dir: Move):
        pos = (tile.pos[0] + dir.value[0], tile.pos[1] + dir.value[1])
        return self.get_tile(pos)

    def starting_tile(self):
        for row in self.maze:
            for tile in row:
                if tile.char == "S":
                    return tile
        raise ValueError("No starting tile found.")

    def valid_connections(self, tile: Tile):
        valid = []
        for connection in tile.connections:
            next_tile = self.get_tile_in_dir(tile, connection)
            if connection.reverse() in next_tile.connections:
                valid.append(connection)
        return valid

    def tile_has_valid_connections(self, tile: Tile):
        if tile.char == "." or tile.char == "S":
            return True
        if self.valid_connections(tile):
            return True
        return False

    def print_maze(self, loop_only=False, show_enclosed=False):
        def get_char(tile):
            if show_enclosed and tile.enclosed:
                return "\033[91mE\033[0m"

            if loop_only and not tile.loop:
                return " "
            return tile.char

        rep = "\n".join(
            ["".join([get_char(tile) for tile in row]) for row in self.maze]
        )

        # Replace chars with unicode box-drawing chars
        replacements = [
            (".", " "),
            ("|", "│"),
            ("L", "└"),
            ("J", "┘"),
            ("7", "┐"),
            ("F", "┌"),
            ("S", "\033[91mX\033[0m"),
        ]
        for old, new in replacements:
            rep = rep.replace(old, new)
        print(rep)

    @classmethod
    def parse_data(cls, data):
        maze = []
        rows = data.split("\n")
        pad_row = str("." * len(rows[0]))
        rows = [pad_row] + rows + [pad_row]
        rows = ["." + row + "." for row in rows]

        for i, row in enumerate(rows):
            maze.append([])
            for j, char in enumerate(row):
                maze[i].append(Tile((i, j), char))
        return maze


def main(data, log=False):
    maze = Maze(data)
    print(maze.char_of_start())

    # Part 1
    print(f"Part 1: Max distance from start: {maze.loop_length}")
    if log:
        print("Maze loop:")
        maze.print_maze(loop_only=True, show_enclosed=True)

    # 6870 correct

    # Part 2
    print(f"Part 2: Enclosed tiles: {maze.enclosed}")

    return


if __name__ == "__main__":
    args = day_parser().parse_args()
    with open(args.infile) as f:
        print(f"Using data from {args.infile}.\n")
        data = f.read().strip()
    main(data, log=args.log)
