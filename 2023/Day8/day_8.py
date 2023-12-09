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


def get_loop_val(nodes, steps, key, log=False):
    stepper = cycle(len(steps))
    i = 0
    node_key = key
    max_iter = len(nodes) * len(steps)
    pos = None
    while i < max_iter:
        if node_key.endswith("Z"):
            if log:
                print(f"{key} loop len: {i}, {pos = }.")
            return i, pos
        pos = next(stepper)
        node_i = steps[pos]
        node_key = nodes[node_key][node_i]
        i += 1


def model_loops(loops, max_iter=1_000_000, log=False):
    did_break = False
    for step in range(max_iter):
        step_vals = []
        for l_len, z_idx in loops:
            step_vals.append(step % l_len == z_idx)
        if all(step_vals):
            print(f"Step {step} {step_vals =}.")
            did_break = True
            break
    print(f"Did break: {did_break}")
    return


def part_2(nodes, steps, log=False):
    """
    Initally tried brute force  - takes way too long ...

    Motivating Idea: The problem has to be solvable - so we know that there exists some "Z" node in the sequence (node, step) starting from each "A" node.

    The problem has n nodes and d steps, so there are a finite number of unique states in the sequence (ln*ld). The number of states is finite, so at some point less < ln*ld steps the sequence must start to repeat itself - i.e. it creates a loop l of length n with a Z in its z_th step.  But there are many type of loop that can be created - e.g. l(3,1), l(5,2), l(6,2) are all loops of length 3, 5, 6 respectively with a Z in the 1st, 2nd, 2nd step respectively.

    l(3,1) : 0,x,2,0,x,2,0,x,2,0,x,2,0,x,2,0,x,2,0,x,2,0,x,2,0,x,2,0,x,2
    l(5,2) : 0,1,x,3,4,0,1,x,3,4,0,1,x,3,4,0,1,x,3,4,0,1,x,3,4,0,1,x,3,4
    l(6,2) : 0,1,x,3,4,5,0,1,x,3,4,5,0,1,x,3,4,5,0,1,x,3,4,5,0,1,x,3,4,5

    It doesn't appear that the "zs" for these particular loops align on any step.  We can test using model_loops() - this shows that these loops do not align on any step < 1_000_000.

    So all A nodes must loop (as states are finite), and all A-nodes must lead to a Z node (as we know the problem is solvable) therefore we know that our loops must align at some point. So what types of loop do align?

    Loops that all have z_nodes at the same step - eg. l(3,1), l(5,1), l(6,1) align at step 1. But this would be a trivial case - but it can't be that simple as brute force didn't find it within way more than ln*ld steps.

    Well if loops that have the same relative position of the z in their loop - eg. l(3,2), l(5,4), l(6,5) - then this looks a lot like a pattern seen in least common multiple (LCM) calculations.

    e.g.
    l(3,2):0,1,Z,0,1,Z,0,1,Z,0,1,Z,0,1,Z,0,1,Z,0,1,Z,0,1,Z,0,1,Z,0,1,Z
    l(5,4):0,1,2,3,4,Z,0,1,2,3,4,Z,0,1,2,3,4,Z,0,1,2,3,4,Z,0,1,2,3,4,Z
    l(6,5):0,1,2,3,4,Z,0,1,2,3,4,Z,0,1,2,3,4,Z,0,1,2,3,4,Z,0,1,2,3,4,Z

    In this special case, solving where the z_nodes align is equivalent to solving the LCM of the loop lengths. This holds true in any case where the relative position of the z_node is the same in each loop - e.g. l(3,1), l(5,3), l(6,4) - as in this case we know that the loops align on the LCM of the loop lengths - but our z is offset from there by in this case 1 step.

    If we can confirm that our data is a special case by confirming that all the loops have a z in the same relative position in the loop. Then we can solve the problem by finding the LCM of the loop lengths and then adding the offset of the z_node from the LCM.

    Technically there was no promise in the problem statement that each loop would have in it only one z_node.  If there were multiple z_nodes in a loop, then we would have look at all the permutations of z_nodes in the loops and find the LCM of each permutation.  But we can confirm that there is only one z_node in each loop by looking at the output of get_loop_val() - which shows that each loop has only one z_node - which simplifies the problem.

    Answer turned out to be 10_668_805_667_831 - no way I was going to brute force that!
    """
    a_nodes = set(filter(lambda x: x[-1] == "A", nodes.keys()))
    sequences = []
    for curr in a_nodes:
        sequences.append(get_loop_val(nodes, steps, curr, log=log))

    assert len(set(s[1] for s in sequences)) == 1, "Not all loops have a z_node in the same relative position in the loop."

    z_steps = [zs[0] for zs in sequences]
    rel_pos = sequences[0][1] + 1 - len(steps)

    if log:
        print(f"Z steps: {z_steps}")

    return math.lcm(*z_steps) + rel_pos


def main(data, log=False):
    step_data, node_data = data.split("\n\n")
    steps = [0 if s == "L" else 1 for s in step_data]

    expr = re.compile(r"\w{3}")
    nodes = {}
    for nd in node_data.split("\n"):
        key, *value = expr.findall(nd)
        nodes[key] = value

    print(f"{len(nodes)} nodes, {len(steps)} steps")

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
