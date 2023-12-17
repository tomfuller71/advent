from aoc_utils import day_parser
import numpy as np
from itertools import combinations


def calc_distances(star_pos, expansion_factor, blank_rows, blank_cols):
    star_dist = 0
    expansion_factor -= 1
    for star_pair in combinations(star_pos, 2):
        a, b = star_pair
        a_row, a_col = a
        b_row, b_col = b
        dist = abs(a_row - b_row) + abs(a_col - b_col)
        st_r, en_r = min(a_row, b_row), max(a_row, b_row)
        for i in range(st_r, en_r):
            if i in blank_rows:
                dist += expansion_factor
        st_c, en_c = min(a_col, b_col), max(a_col, b_col)
        for i in range(st_c, en_c):
            if i in blank_cols:
                dist += expansion_factor
    return star_dist


def main(data, log=False):
    data = data.split("\n")
    star_array = np.zeros((len(data), len(data[0])), dtype=int)
    count = 1
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "#":
                star_array[i, j] = count
                count += 1

    blank_rows = []
    for i in range(len(star_array)):
        if np.all(star_array[i] == 0):
            blank_rows.append(i)

    blank_cols = []
    for i in range(len(star_array[0])):
        if np.all(star_array[:, i] == 0):
            blank_cols.append(i)

    star_pos = []
    for i in range(len(star_array)):
        for j in range(len(star_array[0])):
            if star_array[i, j] != 0:
                star_pos.append((i, j))

    # Part 1
    exp_factor = 2
    distance = calc_distances(star_pos, exp_factor, blank_rows, blank_cols)
    print(f"Part 1: {exp_factor=}, {distance=}.")

    # Part 2
    exp_factor = 1_000_000
    distance = calc_distances(star_pos, exp_factor, blank_rows, blank_cols)
    print(f"Part 2: {exp_factor=}, {distance=}.")

    if log:
        print(star_array)
        print(blank_rows)
        print(blank_cols)
        print(star_pos)

    return


if __name__ == "__main__":
    args = day_parser().parse_args()
    with open(args.infile) as f:
        print(f"Using data from {args.infile}.\n")
        data = f.read().strip()
    main(data, log=args.log)
