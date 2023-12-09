import re
import math
from timeit import default_timer as timer

from aoc_utils import day_parser


def cycle(n):
    i = 0
    while True:
        yield i
        i = (i + 1) % n


def part_1(nodes, steps):
    seen = set()
    stepper = cycle(len(steps))
    curr, dest, count = "AAA", "ZZZ", 0
    while curr != dest:
        pos = next(stepper)
        node_i = steps[pos]

        # Check for loop
        if curr in seen:
            print("Loop detected")
            break
        else:
            seen.add((curr, pos))

        curr = nodes[curr][node_i]
        count += 1
    return count


def get_loop_val(nodes, steps, key, max_iter=100_000, log=False):
    seen = set()
    stepper = cycle(len(steps))
    zs = []
    i = 0
    node_key = key
    while i < max_iter:
        pos = next(stepper)
        node_i = steps[pos]
        if (node_key, pos) in seen:
            break

        seen.add((node_key, pos))

        if node_key.endswith("Z"):
            zs.append(i)

        node_key = nodes[node_key][node_i]
        i += 1

    if log:
        print(f"{key} loops at {node_key} after {i} moves, {zs = }.")

    return zs


def part_2(nodes, steps, max_iter=100_000, log=False):
    # Initally tried brute force  - takes way too long ... 

    # Idea: if we can confirm that our data is a special case where for each node that starts with a "A" the subsequent sequence of nodes visited does at some point loop (rather than contains an infinite sequence), and that each of these loop contains at least one z_node, then we can calculate the LCM of each permutations of picking one z_node steps index from each node loop - which will be the first time that permution of z_nodes align. The min of these LCMs will be the answer.

    # Answer turned out to be 10_668_805_667_831 - no way I was going to brute force that!

    a_nodes = set(filter(lambda x: x[-1] == "A", nodes.keys()))
    sequences = {}
    for curr in a_nodes:
        sequences[curr] = get_loop_val(
            nodes, steps, curr, max_iter=max_iter, log=log
        )

    assert all(sequences.values()), f"Some A-nodes didn't loop within {max_iter} iters. Cannot proceed."

    # Note: output confirms that our input is indeed a special case where all "A" nodes sequences loop - also from review of the output I know that each A-node loop contains only one Z-node - so there is only one permutation of Z-nodes to consider.
    z_steps = [zs[0] for zs in sequences.values()]

    if log:
        print(f"Z steps: {z_steps}")

    return math.lcm(*z_steps)


def main(data, log=False):
    step_data, node_data = data.split("\n\n")
    steps = [0 if s == "L" else 1 for s in step_data]

    expr = re.compile(r"\w{3}")
    nodes = {}
    for nd in node_data.split("\n"):
        key, *value = expr.findall(nd)
        nodes[key] = value

    print(f"Part 1: {part_1(nodes, steps)}")

    start = timer()
    print(f"Part 2: {part_2(nodes, steps, log=log)}")
    end = timer()
    print(f"Part 2 Time: {end - start}")
    return


if __name__ == "__main__":
    args = day_parser().parse_args()
    with open(args.infile) as f:
        print(f"Using data from {args.infile}.\n")
        data = f.read().strip()
    main(data, log=args.log)
