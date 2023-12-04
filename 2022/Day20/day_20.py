# This is a template for a boilerplate file for a new day of Advent of Code

"""
== Part 1 ==


== Part 2 ==

"""
import sys


def main(data, log=False):
    print("== Part 1 ==")

    print("== Part 2 ==")


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