from aoc_utils import day_parser

def predict_recursive(seq):
    if all(s==0 for s in seq):
        return 0
    diffs = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
    return predict_recursive(diffs)


def main(data, log=False):
    lines = [map(int, line.split()) for line in data.split("\n")]
    # Part 1
    print(f"Part 1: {sum(predict(line) for line in lines)}")


    # Part 2


    return


if __name__ == "__main__":
    args = day_parser().parse_args()
    with open(args.infile) as f:
        print(f"Using data from {args.infile}.\n")
        data = f.read().strip()
    main(data, log=args.log)
    main(data, log=args.log)