"""
--- Day 5: If You Give A Seed A Fertilizer ---
== Part 1 ==
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4


The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?


== Part 2 ==

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?

"""
import sys
import re
from dataclasses import dataclass
from collections import deque
import timeit

@dataclass
class Range:
    dest_start: int
    source_start: int
    length: int

    def __post_init__(self):
        self.offset = self.dest_start - self.source_start

    @property
    def dest_end(self):
        return self.dest_start + self.length

    @property
    def source_end(self):
        return self.source_start + self.length

    def translate(self, value):
        if value not in self:
            return None
        return value + self.offset

    def __repr__(self):
        return f"Range({self.dest_start}, {self.source_start}, {self.length})"

    def __contains__(self, value):
        return self.source_start <= value < self.source_start + self.length


@dataclass
class MapPair:
    source: str
    destination: str
    ranges: list[Range]

    def __post_init__(self):
        self.ranges = list(sorted(self.ranges, key=lambda r: r.source_start))
        range_st_ends = [(r.source_start, r.source_end, r.offset) for r in self.ranges]
        contiguous_ranges = [range_st_ends[0]]
        current_end = range_st_ends[0][1]
        for r in range_st_ends[1:]:
            if r[0] != current_end:
                contiguous_ranges.append((current_end, r[1] - 1, 0))
            contiguous_ranges.append(r)
            current_end = r[1]
        self.joined =  contiguous_ranges


    def get_destination_value(self, value):
        for r in self.ranges:
            if value in r:
                return r.dest_start + (value - r.source_start)
        return value

    def get_dest_ranges(self, start, end):
        sub_ranges = []
        ranges = self.joined
        if ranges[0][0] > start:
            ranges = [(start, ranges[0][0], 0)] + ranges
        for r_st, r_end, offset in ranges:
            if r_st > end or r_end < start:
                continue
            if r_st >= start and r_end <= end:
                sub_ranges.append((r_st + offset, r_end + offset))
            else:
                max_start = max(r_st, start)
                min_end = min(r_end, end)
                sub_ranges.append((max_start + offset, min_end + offset))
        if not sub_ranges:
            sub_ranges.append((start, end))
        return sub_ranges


class Map:
    def __init__(self, map_data):
        self.maps = []
        for data in map_data:
            source = data[0]
            destination = data[1]
            range_values = [int(n) for n in data[2].split()]
            ranges = [range_values[i : i + 3] for i in range(0, len(range_values), 3)]
            ranges = [Range(*r) for r in ranges]
            self.maps.append(MapPair(source, destination, ranges))

    def map_value(self, item):
        if log:
            print(f"Mapping seed value {item}.")
        for map in self.maps:
            item = map.get_destination_value(item)
            if log:
                print(f" - Mapped to {item} by {map.source} -> {map.destination}")
        return item

    def get_dest_ranges(self, start, end, log=False):
        if log:
            print(f"Seed range: ({start}, {end}):")

        dest_ranges = [(start, end)]
        for map in self.maps:
            if log:
                print(f" - Map: {map.source} -> {map.destination}")
            found_ranges = []
            for found_range in dest_ranges:
                new_ranges = map.get_dest_ranges(*found_range)
                if log:
                    print(f"- {found_range} -> {new_ranges}")
                found_ranges.extend(new_ranges)
            dest_ranges = found_ranges

        return dest_ranges

    def minimum_range_start(self, start, length, log=False):
        dest_ranges = self.get_dest_ranges(start, length, log=log)
        if not dest_ranges:
            return None

        min_val = min(dest_ranges, key=lambda r: r[0])[0]

        if log:
            print(f"Dest ranges: {dest_ranges}")
        return min_val

    def __repr__(self):
        return f"Map({self.maps})"

    def __contains__(self, key):
        return key in self.maps


def main(data, log=False):
    # Parse data
    seed_exp = re.compile(r"seeds: ((\d+ )+\d+)")
    map_exp = re.compile(r"(\w+)-to-(\w+) map:\n((\d+ \d+ \d+\n)+)")
    seed_data = seed_exp.match(data)
    map_data = map_exp.findall(data)

    if not seed_data or not map_data:
        print("Failed to parse data.")
        sys.exit()

    seed_data = seed_data.group(1).split()
    seeds = [int(n) for n in seed_data]

    map = Map(map_data)

    # Part 1
    print("== Part 1 ==")
    locations = [map.map_value(s) for s in seeds]
    if log:
        print(f"Locations: {locations}")
    closest_location = min(locations)
    print(f"Closest location: {closest_location}")

    # Part 2
    print("== Part 2 ==")
    # Set up timer
    start = timeit.default_timer()
    seed_range_starts = [int(n) for n in seed_data[::2]]
    seed_range_lengths = [int(n) for n in seed_data[1::2]]
    range_pairs = [(s, s + l) for s, l in zip(seed_range_starts, seed_range_lengths)]

    # Get the minimum location for each range
    range_mins = [
        map.minimum_range_start(start, length, log=log)
        for start, length in range_pairs
    ]
    if log:
        print(f"Range mins: {range_mins}")

    # Filter out None values
    range_mins = [m for m in range_mins if m is not None]

    # Get the minimum of the minimums
    closest_location = min(range_mins)
    print(f"Closest location: {closest_location}")
    print(f"Time: {timeit.default_timer() - start}")


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
