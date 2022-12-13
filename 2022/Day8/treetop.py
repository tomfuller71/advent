'''
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
 [1 1 1 1 1]
 [1 1 1 0 1]
 [1 1 0 1 1]
 [1 0 1 0 1]
 [1 1 1 1 1]
Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
'''

import sys
import numpy as np
from numpy.typing import NDArray as Array
from enum import Enum

class LineType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


def parse_data(data: str) ->Array:
    return np.array([list(x) for x in data.splitlines()]).astype(int)


def get_sight_line(trees: Array, index, line_type: LineType):
    if line_type == LineType.VERTICAL:
        return trees[:, index]
    else:
        return trees[index, :]

def mark_visible_trees(line: Array) -> Array:
    visible = np.zeros_like(line)
    for i, tree in enumerate(line):
        if i == 0 or i == len(line) - 1:
            visible[i] = 1
        elif np.all(line[i+1:] < tree) or np.all(line[:i] < tree):
            visible[i] = 1
    return visible


def visible_trees(trees: Array) -> int:
    rows, cols = trees.shape
    visible = np.zeros_like(trees)
    for i in range(rows):
        row = get_sight_line(trees, i, LineType.HORIZONTAL)
        marked = mark_visible_trees(row)
        visible[i, :] += marked
    for i in range(cols):
        col = get_sight_line(trees, i, LineType.VERTICAL)
        marked = mark_visible_trees(col)
        visible[:, i] += marked
    visible = np.where(visible > 0, 1, 0)
    print(visible)
    return np.sum(visible)



'''
--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390
Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390
Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
'''

def distance(line: Array, height) -> int:
    distance = 0
    for tree in line:
        distance += 1
        if tree >= height:
            break
    return distance


def scenic_score(trees: Array, row, col) -> int:
    value = trees[row, col]
    up = distance(trees[: row, col][::-1], value)
    left = distance(trees[row, :col][::-1], value)
    down = distance(trees[row+1:, col], value)
    right = distance(trees[row, col+1:], value)
    # print(f'({row}, {col}): {value=} {up=} {left=} {down=} {right=}')
    return up * down * left * right

def best_scenic_score(trees: Array) -> tuple[int, Array]:
    rows, cols = trees.shape
    scores = np.zeros_like(trees)
    for i in range(rows):
        for j in range(cols):
            scores[i, j] = scenic_score(trees, i, j)
    best_scenic_score = np.max(scores)
    best_score_index = np.where(scores == best_scenic_score)
    return best_scenic_score, best_score_index


def main(data):
    #Part 1 - should return 21
    trees = parse_data(data)
    print(f'Part 1: {visible_trees(trees)}') 

    # Part 2 - should return 8
    best_score, best_score_index = best_scenic_score(trees)
    indices = list(zip(*best_score_index))
    print(f'Part 2: {best_score} at {indices}')
    


if __name__ == '__main__':
    TESTING = False
    data_file = 'input.txt'
    if TESTING:
        data_file = 'example.txt'

    with open(data_file) as f:
        data = f.read()

    main(data)