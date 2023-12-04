# This is a template for a boilerplate file for a new day of Advent of Code

"""
--- Day 4: Scratchcards ---

The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, all with their opaque covering already scratched off. Picking one up, it looks like each card has two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have. You organize the information into a table (your puzzle input).

== Part 1 ==

As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the list of winning numbers. The first match makes the card worth one point and each match after the first doubles the point value of that card.

For example:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86) are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three times for each of the three matches after the first).

Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
Card 4 has one winning number (84), so it is worth 1 point.
Card 5 has no winning numbers, so it is worth no points.
Card 6 has no winning numbers, so it is worth no points.
So, in this example, the Elf's pile of scratchcards is worth 13 points.

Take a seat in the large pile of colorful cards. How many points are they worth in total?



== Part 2 ==

"""
import sys
import re
import math
from collections import deque

p1_example_answer = [8, 2, 2, 1, 0, 0]


def main(data, log=True):
    exp = re.compile(r"(\d+)")
    lines = data.strip().replace(":", "|").split("\n")

    # Part 1
    line_card_sets = []
    for line in lines:
        line_sets = []
        for line_part in line.split("|")[1:]:
            line_sets.append(set(exp.findall(line_part)))
            if log: print(line_part)
        line_card_sets.append(line_sets)

    count_same_nums = [len((c[0] & c[1])) for c in line_card_sets]
    points = [math.pow(2, e - 1) if e else 0 for e in count_same_nums]
    sum_points = sum(points)

    # Part 2
    n_lines = len(lines)
    unscratched = deque([i for i in range(n_lines)])
    scratched = 0

    while (unscratched):
        card_i = unscratched.popleft()
        scratched += 1
        cards_won = count_same_nums[card_i]
        for i in range(cards_won):
            next_card_count_i = (card_i + i + 1) % n_lines
            unscratched.append(next_card_count_i)

            if log:
                print(f"Card {card_i + 1} won card {next_card_count_i + 1}")


    # Logging
    if log:
        print("== Parsing ==")
        print(lines)
        print("== Parsing ==")
        print(line_card_sets)
        print(f"Count same nums: {count_same_nums}")
        print(f"Scores: {points}")


    print("== Part 1 ==")
    print(int(sum_points))
    print("== Part 2 ==")
    print(scratched)


if __name__ == "__main__":
    log = False
    if len(sys.argv) < 2:
        print("Useage: python <pyfile> <infile> [-l|--log]")
        sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] in ["-l", "--log"]:
            log = True
    with open(sys.argv[1]) as f:
        print(f"Using data from {sys.argv[1]}.\n")
        data = f.read()
    main(data, log=log)
