"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

NUM_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

WORD_PARTS = set()
for word in NUM_WORDS.keys():
    word_frag = ""
    for c in word:
        word_frag += c
        WORD_PARTS.add(word_frag)

def scanline(line: str, reverse=False):
    numbers = []
    for i in range(len(line)):
        if line[i].isdigit():
            numbers.append(int(line[i]))
            continue

        part = ""
        for c in line[i:]:
            if (part + c) not in WORD_PARTS:
                break
            part += c

        if value := NUM_WORDS.get(part, 0):
            numbers.append(value)
    
    if numbers:
        return 10 * numbers[0] + numbers[-1]
    return 0
    

def main(data):
    lines = data.split("\n")
    if not lines[-1]:
        print("dropping last value")
        lines.pop()
    


    numbers = [scanline(l) for l in lines]
    print(f"Total Part 2: {sum(numbers)}")


if __name__ == "__main__":
    TESTING = False
    data_file = "input.txt"
    if TESTING:
        data_file = "example.txt"

    with open(data_file) as f:
        data = f.read()

    main(data)

# Correct 54019

# Wrong answers
#  54121 to high
#  54119
