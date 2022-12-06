'''
--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)
'''

import sys
from collections import Counter
from dataclasses import dataclass

def get_digit_lists(lines: list[str]) -> list[str]:
    digit_length = len(lines[0])
    digit_lists = [''] * digit_length
    for line in lines:
        for i, c in enumerate(line):
            digit_lists[i] += c
    return digit_lists

def get_counters(digit_lists: list[str]) -> list[Counter]:
    return [Counter(digit_list) for digit_list in digit_lists]

def get_gamma_and_epsilon(counters: list[Counter]) -> tuple[str, str]:
    gamma, epsilon = '', ''
    for counter in counters:
        most_common, least_common = counter.most_common(2)
        gamma += most_common[0] # index 0 is the key, index 1 is the count
        epsilon += least_common[0]
    return gamma, epsilon


def rates_product(gamma: str, epsilon: str) -> int:
    return int(gamma, 2) * int(epsilon, 2)

def part1(lines: list[str]):
    digit_lists = get_digit_lists(lines)
    counters = get_counters(digit_lists)
    gamma, epsilon = get_gamma_and_epsilon(counters)
    print("Part 1:")
    print(f'\tGamma: {gamma} ({int(gamma, 2)})')
    print(f'\tEpsilon: {epsilon} ({int(epsilon, 2)})')
    print(f'\tPower consumption: {rates_product(gamma, epsilon)}\n')

'''
--- Part Two ---
Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating by the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report - finding them is the tricky part. Both values are located using a similar process that involves filtering out values until only one remains. Before searching for either rating value, start with the full list of binary numbers from your diagnostic report and consider just the first bit of those numbers. Then:

Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers which do not match the bit criteria.
If you only have one number left, stop; this is the rating value for which you are searching.
Otherwise, repeat the process, considering the next bit to the right.
The bit criteria depends on which type of rating value you want to find:

To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.
For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.
Then, to determine the CO2 scrubber rating value from the same example above:

Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2 numbers with a 1 in the second position: 01111 and 01010.
In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010.
As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.
Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.

Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in decimal, not binary.)
'''
@dataclass
class BitPosition:
    most_common: str
    least_common: str
    equal: bool
    
    def __str__(self):
        return f'Most Common: {self.most_common}, Least Common: {self.least_common}, Equal: {self.equal}'


def get_bit_position(lines: list[str], position: int) -> BitPosition:
    digits = ''.join(line[position] for line in lines)
    most_common, least_common = Counter(digits).most_common(2)
    equal = most_common[1] == least_common[1]
    return BitPosition(most_common[0], least_common[0], equal)


def filter_lines(lines: list[str], key: str) -> list[str]:
    return list(filter(lambda line: line[:len(key)] == key, lines))


def get_rating(lines, if_equal_select='1'):
    rating = ''
    while len(lines) > 1:
        bit_position = get_bit_position(lines, len(rating))
        if bit_position.equal:
            rating += if_equal_select
        elif if_equal_select == '1':
            rating += bit_position.most_common
        else:
            rating += bit_position.least_common
        lines = filter_lines(lines, rating)
    return int(lines[0], 2)


def part2(lines: list[str]):
    o2_rating = get_rating(lines, '1')
    co2_rating = get_rating(lines, '0')
    print("Part 2:")
    print(f'\tOxygen Generator Rating: {o2_rating}')
    print(f'\tCO2 Scrubber Rating: {co2_rating}')
    print(f'\tLife Support Rating: {o2_rating * co2_rating}')

def main(datafile: str):
    with open(datafile) as f:
        lines = [line.strip() for line in f.readlines()]
    part1(lines)
    part2(lines)

if __name__ == '__main__':
    datafile = 'example.txt'
    if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
        datafile = sys.argv[1]
    main(datafile)