'''
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
'''

import sys
from dataclasses import dataclass
import re

@dataclass
class Crate:
    name: str
    starting_stack: int

    def __repr__(self):
        return f'[{self.name}]'

@dataclass
class Move:
    quantity: int
    from_stack: int
    to_stack: int

    def __str__(self):
        return f"move {self.quantity} from {self.from_stack} to {self.to_stack}"

@dataclass
class Stack:
    crates: list[Crate]

    @property
    def top(self):
        return self.crates[-1].name if self.crates else ""

class Stacks:
    def __init__(self, stacks: list[Stack]):
        self.stacks = stacks

    def move(self, move: Move, grouped=False):
        from_stack = self.stacks[move.from_stack - 1]
        to_stack = self.stacks[move.to_stack - 1]
        if grouped:
            to_stack.crates.extend(from_stack.crates[-move.quantity:])
            del from_stack.crates[-move.quantity:]
        else:
            for _ in range(move.quantity):
                to_stack.crates.append(from_stack.crates.pop())

    def __str__(self):
        str_obj = ""
        stack_height = max(len(stack.crates) for stack in self.stacks)
        for i in range(stack_height - 1, -1, -1):
            for stack in self.stacks:
                if i < len(stack.crates):
                    str_obj += f'{stack.crates[i]} '
                else:
                     str_obj += '    '
            str_obj += '\n'
        str_obj += '\n'
        return str_obj

    @property
    def top_row(self):
        return ''.join(stack.top for stack in self.stacks)


def get_crates(stack_lines):
    crates = []
    for line in stack_lines:
        for m in re.finditer(r'\[', line):
            stack_index = m.start() // 4
            stack_name = line[m.start() + 1]
            crates.append(Crate(stack_name, stack_index))
    return crates


def build_stacks(stack_lines, stack_count):
    crates = get_crates(stack_lines)
    stacks = [Stack([]) for _ in range(stack_count)]
    for crate in crates:
        stacks[crate.starting_stack].crates.append(crate)
    
    for stack in stacks:
        stack.crates.reverse()
    
    return Stacks(stacks)


def parse_input(input_file):
    lines = None
    with open(input_file) as f:
        lines = f.readlines()

    stack_count = len(lines[0]) // 4
    stack_lines = list(filter(lambda l: '[' in l, lines))
    move_lines = list(filter(lambda l: 'move' in l, lines))

    return stack_lines, stack_count, move_lines


def parse_moves(move_lines):
    moves = []
    for line in move_lines:
        match = re.search(r'move (\d+) from (\d+) to (\d+)', line)
        if match:
            params = (int(m) for m in match.groups())
            moves.append(Move(*params))
    return moves

'''
--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
'''

def load_ship(stack_lines, stack_count ,move_lines, grouped=False):
    stacks = build_stacks(stack_lines, stack_count)
    moves = parse_moves(move_lines)
    for move in moves:
        stacks.move(move, grouped=grouped)
    return stacks


def main(data_file):
    stack_lines, stack_count, move_lines = parse_input(data_file)
    part1 = load_ship(stack_lines, stack_count, move_lines)
    part2 = load_ship(stack_lines, stack_count, move_lines, grouped=True)
    print(f'Part 1: {part1.top_row}')
    print(f'Part 2: {part2.top_row}')
    


if __name__ == '__main__':
    data_file = "example.txt"
    if len(sys.argv) > 1:
        if sys.argv[1].endswith('.txt'):
            data_file = sys.argv[1]
        else:
            print("Expected .txt file as argument")
            sys.exit(1)
    main(data_file)
