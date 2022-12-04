'''
--- Day 2: Rock Paper Scissors ---
The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?
'''

import sys
from dataclasses import dataclass
from enum import Enum

def score_choice(choice):
    if choice == "X" or choice == "A":
        return 1
    elif choice == "Y" or choice == "B":
        return 2
    elif choice == "Z" or choice == "C":
        return 3
    else:
        raise ValueError(f"Invalid choice: {choice}")

def is_winner(opp_choice, player_choice):
    if player_choice == "X" and opp_choice == "C":
        return True
    elif player_choice == "Y" and opp_choice == "A":
        return True
    elif player_choice == "Z" and opp_choice == "B":
        return True
    else:
        return False

def score_round(opp_choice, player_choice):
    player_choice_score = score_choice(player_choice)
    if player_choice_score == score_choice(opp_choice):
        return 3 + player_choice_score
    elif is_winner(opp_choice, player_choice):
        return 6 + player_choice_score
    else:
        return 0 + player_choice_score


def score_game(rounds):
    total_score = 0
    for opp_choice, player_choice in rounds:
        total_score += score_round(opp_choice, player_choice)
    return total_score


'''
--- Part Two ---
The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
'''

class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @property
    def beaten_by(self):
        if self == Choice.ROCK:
            return Choice.PAPER
        elif self == Choice.PAPER:
            return Choice.SCISSORS
        else:
            return Choice.ROCK
    
    @property
    def beats(self):
        return self.beaten_by.beaten_by
    
    def get_choice(self, choice):
        if choice == "A":
            return Choice.ROCK
        elif choice == "B":
            return Choice.PAPER
        elif choice == "C":
            return Choice.SCISSORS
        else:
            raise ValueError(f"Invalid choice: {choice}")

class Strategy(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


class Round:
    def __init__(self, col1, col2):
        self.opp_choice: Choice = Round.get_choice(col1)
        self.player_strategy: Strategy = Round.get_strategy(col2)

    @property
    def player_choice(self):
        if self.player_strategy == Strategy.LOSE:
            return self.opp_choice.beats
        elif self.player_strategy == Strategy.DRAW:
            return self.opp_choice
        else:
            return self.opp_choice.beaten_by

    def score(self):
        return self.player_choice.value + self.player_strategy.value

    @staticmethod
    def get_choice(choice):
        if choice == "A":
            return Choice.ROCK
        elif choice == "B":
            return Choice.PAPER
        elif choice == "C":
            return Choice.SCISSORS
        else:
            raise ValueError(f"Invalid choice: {choice}")
    
    @staticmethod
    def get_strategy(strategy):
        if strategy == "X":
            return Strategy.LOSE
        elif strategy == "Y":
            return Strategy.DRAW
        elif strategy == "Z":
            return Strategy.WIN
        else:
            raise ValueError(f"Invalid choice: {strategy}")



def main():
    if len(sys.argv) != 2:
        print("Usage: python rps.py <input file>.txt")
        sys.exit(1)

    date_file = sys.argv[1]

    rounds = []
    with open(date_file, mode="r") as data:
        for line in data.readlines():
            text = line.strip()
            if text:
                opp_choice, player_choice = text.split()
                rounds.append((opp_choice, player_choice))

    print(f"Part 1 - Game score: {score_game(rounds)}")
    
    rounds_score = sum(Round(col1, col2).score() for col1, col2 in rounds)
    print(f"Part 2 - Game score: {rounds_score}")



if __name__ == "__main__":
    main()