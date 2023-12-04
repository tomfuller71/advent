"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""
# Part 2
"""
--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""
# insert code below
import re

def adjacent_to_part(matrix, row, col_start, col_stop):
    height = len(matrix) - 1
    width = len(matrix[0])

    adjacent = []
    for i in range(-1, 2, 1):
        slice_row = row + i
        if (slice_row < 0) or (slice_row > height):
            continue
        slice_col_start = max(col_start -1, 0)
        slice_col_end = min(col_stop + 1, width)
        sliced = matrix[slice_row][slice_col_start: slice_col_end]
        adjacent.extend(sliced)
    if any([not (c.isdigit() or c =='.') for c in adjacent]):
        return True
    return False


def find_star_positions(lines):
    star_positions = []
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '*':
                star_positions.append((i, j))
    return star_positions

def match_adj_star(row, num_match, star_pos):
    # if any end idx or start idx is within the box then its a number
    i, j = star_pos
    start, stop = num_match.start(), num_match.end() - 1
    if not (i - 1 <= row <= i + 1):
        return False
    if not ((j - 1 <= start <= j + 1) or (j - 1 <= stop <= j + 1)):
        return False
    print(f"{num_match.group()} {start=} {stop=} is adj star: {star_pos}")
    return True

def get_gear_value(num_matches, star_pos):
    adj_nums = []
    for i, m in num_matches:
        if match_adj_star(i, m, star_pos):
            adj_nums.append(int(m.group()))
    if len(adj_nums) == 2:
        return adj_nums[0] * adj_nums[1]
    return 0

# def adjacent_pos(pos, width, height):
#     adj = []
#     for i in range(-1, 2, 1):
#         if i < 0 or i > height:
#             continue
#         for j in range(-1, 2, 1):
#             if j < 0 or j > width or i == j:
#                 continue
#             adj.append((i, j))
#     return adj

def get_num_matches(lines):
    exp = re.compile(r"(\d+)")
    num_matches = []
    for i, line in enumerate(lines):
        matches = exp.finditer(line)
        num_matches.extend([(i, m) for m in matches])
    print(num_matches)
    return num_matches


def main(data, log=False):
    lines = data.split("\n")
    num_matches = get_num_matches(lines)
        
    print("== Part 1 ==")
    sum_engine_parts = 0
    for i, m in num_matches:
            if adjacent_to_part(lines, i, m.start(), m.end()):
                sum_engine_parts += int(m.group())
    print(sum_engine_parts)

    print("== Part 2 ==")
    sum_gear_values = 0
    positions = find_star_positions(lines)
    for star_pos in positions:
        sum_gear_values += get_gear_value(num_matches, star_pos)
    print(sum_gear_values)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="day_{day}",
        description="Advent of Code challenge.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i", "--infile", type=str, default="input.txt", help="infile to use"
    )
    parser.add_argument(
        "-l", "--log", type=bool, default=False, help="Enable logging"
    )
    
    args = parser.parse_args()
    with open(args.infile) as f:
        print(f"Reading data from {args.infile}")
        data = f.read()

    main(data, log=args.log)
