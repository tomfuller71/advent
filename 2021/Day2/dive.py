'''
--- Day 2: Dive! ---
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

forward X increases the horizontal position by X units.
down X increases the depth by X units.
up X decreases the depth by X units.
Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2
Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

forward 5 adds 5 to your horizontal position, a total of 5.
down 5 adds 5 to your depth, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13.
up 3 decreases your depth by 3, resulting in a value of 2.
down 8 adds 8 to your depth, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15.
After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
'''
import sys
from enum import Enum
from dataclasses import dataclass

class Direction(Enum):
    FORWARD = (1, 0)
    DOWN = (0, 1)
    UP = (0, -1)


class Move:
    def __init__(self, direction: Direction, distance: int):
        self.forward_change = direction.value[0] * distance
        self.aim_change = direction.value[1] * distance


class Submarine:
    def __init__(self, forward=0, depth=0):
        self.forward = forward
        self.depth = depth

    def move(self, move: Move):
        self.forward += move.forward_change
        self.depth += move.aim_change
    
    def moves(self, moves):
        for move in moves:
            self.move(move)

    def __str__(self):
        return f'Product of forward {self.forward}, depth {self.depth} = {self.forward * self.depth}'

def get_moves(datafile):
    with open(datafile) as f:
        return [Move(Direction[direction.upper()], int(distance)) for direction, distance in (line.split() for line in f)]

'''
--- Part Two ---
Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:

down X increases your aim by X units.
up X decreases your aim by X units.
forward X does two things:
It increases your horizontal position by X units.
It increases your depth by your aim multiplied by X.
Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
down 5 adds 5 to your aim, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
up 3 decreases your aim by 3, resulting in a value of 2.
down 8 adds 8 to your aim, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.
After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
'''

class AimedSubmarine(Submarine):
    def __init__(self, forward=0, depth=0, aim=0):
        super().__init__(forward, depth)
        self.aim = aim

    def move(self, move: Move):
        self.forward += move.forward_change
        self.aim += move.aim_change
        self.depth += move.forward_change * self.aim


def main(datafile):
    moves = get_moves(datafile)
    submarine1 = Submarine()
    submarine1.moves(moves)
    submarine2 = AimedSubmarine()
    submarine2.moves(moves)
    print(f'Part 1: {submarine1}')
    print(f'Part 2: {submarine2}')


if __name__ == '__main__':
    datafile = 'example.txt'
    if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
        datafile = sys.argv[1]
    main(datafile)