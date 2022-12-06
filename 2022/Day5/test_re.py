import re
from dataclasses import dataclass

@dataclass
class Move:
    quantity: int
    from_stack: int
    to_stack: int

move = "move 1 from 2 to 1"


def parse_moves(move_lines):
    moves = []
    for line in move_lines:
        quantity, from_stack, to_stack = re.search(r'move (\d+) from (\d+) to (\d+)', line).groups() # type: ignore
        moves.append(Move(int(quantity), int(from_stack), int(to_stack)))
    return moves

print(parse_moves([move]))
