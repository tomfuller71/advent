from collections import Counter
from enum import Enum
from functools import total_ordering


@total_ordering
class HandType(Enum):
    """An enum for the type of hand."""

    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self) -> str:
        return self.name


def score_face(card, joker=False):
    """Returns a score for the first card in a hand. J as Joker is optional."""
    if card == "A":
        return 14
    if card == "K":
        return 13
    if card == "Q":
        return 12
    if card == "J":
        return 11 if not joker else 1
    if card == "T":
        return 10
    return int(card)


def get_label(hand, joker=False):
    """Returns the label of a hand, with optional J as a joker."""
    counter = Counter(hand)
    jokers = counter["J"]
    if joker:
        counter["J"] = 0
    counts = counter.most_common()
    first = counts[0][1]
    second = counts[1][1] if len(counts) > 1 else 0
    label = 0
    if first > 3:
        label = first + 2
    elif first == 3 and second == 2:
        label = first + second
    elif first == 3:
        label = first + 1
    elif first == 2 and second == 2:
        label = first + 1
    else:
        label = first

    if joker:
        for _ in range(jokers):
            if label in range(2, 5):
                label += 2
            else:
                label += 1
    return HandType(label)


def main(data, log=False):
    # Parse the data
    hand_bid_pairs = [line.split() for line in data.strip().split("\n")]

    # Two case for jokers
    for joker in [False, True]:
        print(f"Using jokers: {joker}")

        # Map the hands to their labels and scores - this enables direct sorting
        mapped_pairs = []
        for hand, bid in hand_bid_pairs:
            label = get_label(hand, joker=joker)
            scores = [score_face(card, joker=joker) for card in hand]
            mapped_pairs.append(((label, *scores), int(bid)))

        sorted_pairs = sorted(mapped_pairs)

        if log:
            print(f"Found {len(mapped_pairs)} hands.")
            for hand, bid in mapped_pairs:
                label, *vals = hand
                print(f"\tlabel: {label.name}, vals: {vals}, bid: {bid}")

            print(f"Sorted hands:")
            for hand, bid in sorted_pairs:
                print(f"\t({hand}, {bid})")

        # Calculate the total winnings
        total_winnings = 0
        for i, (hand, bid) in enumerate(sorted_pairs):
            total_winnings += bid * (i + 1)
        print(f"The total winnings are {total_winnings}.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Run Advent of Code problem.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--infile", action="store",
        help="Input file name (default: %(default)s)",
        default="example.txt",
    )
    parser.add_argument("-l", "--log", action="store_true",
        help="Enable log (default: %(default)s)",
        default=False,
    )

    args = parser.parse_args()
    with open(args.infile) as f:
        print(f"Using data from {args.infile}.\n")
        data = f.read()
    main(data, log=args.log)
