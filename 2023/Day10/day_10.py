from calendar import c
from enum import Enum


from aoc_utils import day_parser


class Move(Enum):
    U = (-1, 0)
    D = (1, 0)
    L = (0, -1)
    R = (0, 1)

    def __repr__(self):
        return self.name

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

TURNS = {
    ".": 0,
    "|": 0,
    "-": 0,
    "L": 1,
    "J": -1,
    "7": -1,
    "F": 1,
    "S": 0,
}


class Tile:
    def __init__(self, pos: tuple[int, int], char: str):
        self.pos = pos
        self.connections = CONNECTIONS[char]
        self.char = char
        self.loop = False
        self.down_face_inside = False
        self.enclosed = False

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
        self.start_char = self.char_of_start()
        self.marked_loop = False
        self.loop_length = self.search_max_distance_from_start()
        self.enclosed = self.count_enclosed()

        rows, cols = len(self.maze) - 2, len(self.maze[0]) - 2
        print(f"Maze size: {rows}x{cols} = {rows * cols}")

    def search_max_distance_from_start(self):
        loop_count = 0
        tile = self.start
        tile.char = self.start_char
        tile.connections = CONNECTIONS[self.start_char]
        # S guarantees 2 valid connections - can go either way round the loop
        dirs = self.valid_connections(tile)
        heading = None
        if dirs[0] in [Move.L, Move.R]:
            heading = dirs[0]
        elif dirs[1] in [Move.L, Move.R]:
            heading = dirs[1]
        else:
            heading = dirs[0]

        handedness_LR = heading if heading in [Move.L, Move.R] else Move.R
        current_LR = handedness_LR
        print(f'Starting at {self.start.pos} with {self.start_char}, {heading=} {handedness_LR=}')
        while True:
            tile.loop = True
            LR_heading = heading if heading in [Move.L, Move.R] else current_LR
            tile.down_face_inside = LR_heading != handedness_LR
            print(f'For tile: {tile.char}, {heading=}, LR={LR_heading}, inside={tile.down_face_inside}')
            
            next, next_heading = self.get_tile_and_heading(tile, heading)
            loop_count += 1
            if next is self.start:
                break
            tile = next
            heading = next_heading
            current_LR = LR_heading
        self.marked_loop = True
        tile.char = "S"
        return loop_count // 2

    def char_of_start(self):
        valid = self.valid_connections(self.start)
        valid = (valid[0], valid[1])
        for key, value in CONNECTIONS.items():
            if value == valid:
                return key
        raise ValueError("No valid char found for start.")

    
    def count_enclosed(self):
        self.mark_as_enclosed()
        enclosed = 0
        for row in self.maze:
            for tile in row:
                if tile.enclosed:
                    enclosed += 1
        return enclosed

    def mark_as_enclosed(self):
        candidates = []
        for row in self.maze[1: -1]:
            first, last  = None, None
            for i in range(1, len(row)):
                if row[i].loop:
                    first = i
                    break

            for i in range(len(row) - 1, 0, -1):
                if row[i].loop:
                    last = i
                    break

            if not first or not last:
                continue

            for i in range(first, last):
                if not row[i].loop:
                    candidates.append(row[i])

        for tile in candidates:
            up_tile = self.get_tile_in_dir(tile, Move.U)
            while not up_tile.loop and up_tile.pos[0] > 1:
                up_tile = self.get_tile_in_dir(up_tile, Move.U)
            if up_tile.loop and up_tile.down_face_inside:
                tile.enclosed = True
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
