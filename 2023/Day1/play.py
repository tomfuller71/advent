import re

NUM = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
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

with open("input.txt") as f:
    data = f.read()

lines = data.split("\n")[:-1]
exp = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")
sum = 0
for line in lines:
    matches = exp.findall(line)
    if matches:
        sum += 10 * NUM[matches[0]] + NUM[matches[-1]]

print(sum)
