'''
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?
'''
import sys
import numpy as np

    
class Board:
    def __init__(self, data):
        self.squares = np.array(Board.from_data(data))
        self.marked = np.zeros(self.squares.shape)
    
    def mark(self, value):
        rows, cols = np.where(self.squares == value)
        for row, col in zip(rows, cols):
            self.marked[row, col] = 1
    
    def is_winner(self):
        mean_rows = np.mean(self.marked, axis=1)
        mean_cols = np.mean(self.marked, axis=0)
        return 1 in mean_rows or 1 in mean_cols
    
    def score(self, value):
        rows, cols = np.where(self.marked == 0)
        return np.sum(self.squares[rows, cols]) * value
    
    @classmethod
    def from_data(cls, data: str) -> list[list[int]]:
        return [
                [int(value) for value in row.split()]
                for row in data.splitlines()
               ]


def part1(calls, boards):
    for call in calls:
        for index, board in enumerate(boards):
            board.mark(call)
            if board.is_winner():
                return index + 1, board.score(call)
    return 0, 0


'''
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
'''

def part2(calls, boards):
    winning_indices = []
    winning_scores = []
    for call in calls:
        for index, board in enumerate(boards):
            if index in winning_indices:
                continue
            board.mark(call)
            if board.is_winner():
                winning_indices.append(index)
                winning_scores.append(board.score(call))
    return winning_indices[-1] + 1, winning_scores[-1]


def main(board_data, call_data):
    calls = [int(value) for value in call_data.split(',')]
    
    boards = [Board(board) for board in board_data]
    winner, score = part1(calls, boards)
    print(f'Part 1: Winner: {winner}, Score: {score}')

    boards = [Board(board) for board in board_data]
    winner, score = part2(calls, boards)
    print(f'Part 2: Last winner: {winner}, Score: {score}')


if __name__ == '__main__':
    datafile = 'example.txt'
    if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
        datafile = sys.argv[1]

    with open(datafile) as f:
        data = f.read().split('\n\n')
        main(data[1:], data[0])
