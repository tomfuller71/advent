'''

'''

import sys




def main(data):
    pass


if __name__ == '__main__':
    TESTING = True
    data_file = 'input.txt'
    if TESTING:
        data_file = 'example.txt'

    with open(data_file) as f:
        data = f.read()

    main(data)