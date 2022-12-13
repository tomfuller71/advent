# This is a template for a boilerplate file for a new day of Advent of Code

# Part 1
'''

'''
# insert part 1 code here





# Part 2
'''

'''
# insert part 2 code here


def main(data):
    # Part 1

    # Part 2

    pass


if __name__ == '__main__':
    TESTING = True
    data_file = 'input.txt'
    if TESTING:
        data_file = 'example.txt'

    with open(data_file) as f:
        data = f.read()

    main(data)