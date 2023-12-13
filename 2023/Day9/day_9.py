from aoc_utils import day_parser

def predict_recursive(seq):
    if all(s==0 for s in seq):
        return 0
    diffs = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
    return seq[-1] + predict_recursive(diffs)


def main(data, log=False):
    lines = [list(map(int, line.split())) for line in data.split("\n")]

    # Part 1
    predictions = [predict_recursive(line) for line in lines]
    if log:
        print("Part 1:")
        print(f"\tLines: {lines}")
        print(f"\tPredictions: {predictions}")
    print(f"Part 1: {sum(predictions)}")


    # Part 2
    lines = [list(reversed(line)) for line in lines]
    predictions = [predict_recursive(line) for line in lines]
    if log:
        print("\nPart 2:")
        print(f"\tLines: {lines}")
        print(f"\tPredictions: {predictions}")
    print(f"Part 2: {sum(predictions)}")
    return


if __name__ == "__main__":
    args = day_parser().parse_args()
    with open(args.infile) as f:
        print(f"Using data from {args.infile}.\n")
        data = f.read().strip()
    main(data, log=args.log)