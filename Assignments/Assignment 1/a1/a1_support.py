"""
Support code for the Sliding Puzzle Game
Assignment 1
Semester 1, 2021
CSSE1001/CSSE7030
"""

import random
from typing import List

# Grid display elements
HORIZONTAL_WALL = "-"
VERTICAL_WALL = "|"
CORNER = "+"
EMPTY = " "

# Actions
HELP = "H"
GIVE_UP = "GU"
# Directions
UP = "U"
DOWN = "D"
LEFT = "L"
RIGHT = "R"

# Prompts
BOARD_SIZE_PROMPT = """
Choose your difficulty. The larger the puzzle, the harder it is to solve.
How big do you want the puzzle to be? """
DIRECTION_PROMPT = 'Please input a direction (enter "H" for instructions): '
PLAY_AGAIN_PROMPT = "Do you want to play again? [Y/n] "

# Messages
WELCOME_MESSAGE = """
Welcome to the big brain sliding puzzle game.
This game is based on the real life sliding puzzle: \
https://en.wikipedia.org/wiki/Sliding_puzzle
Try the game online here: \
https://www.helpfulgames.com/subjects/brain-training/sliding-puzzle.html
"""

INVALID_MESSAGE = "That's not a valid input, try again.\n"
# Use this constant with the str.format method.
# https://docs.python.org/3.9/library/string.html#format-examples
INVALID_MOVE_FORMAT = "'{}' is not a possible move here. Please try again.\n"

HELP_MESSAGE = """
Options:
    H:          Display this help message
    GU:         Stop the current game
    [U|D|L|R]:  Move the empty cell in the up/down/left/right direction, 
                respectively.

"""
WIN_MESSAGE = r"""Congratulations, you've won the game. Here's your candy:
              ___      .-""-.      ___
              \  "-.  /      \  .-"  /
               > -=.\/        \/.=- <
               > -='\        /\'=- <
              /__.-'  \      /  '-.__\
                       '-..-'
    
    """
GIVE_UP_MESSAGE = "Aww, too bad. Better luck next time.\n"
BYE = "Bye.\n"

WORDS_FILE = "words.txt"


def load_words(file_name: str, word_length: int) -> List[str]:
    """
    Loads all words of specified length from a word file.

    Parameters:
        file_name (str): Name of file to load words from
        word_length (int): Length of words to be loaded

    Returns:
        (List[str]): List of word_length sized words from file
    """
    words = []
    with open(file_name) as word_file:
        for line in word_file.readlines():
            word = line.strip()
            if len(word) == word_length:
                words.append(word)

    return words


def get_random_words(words: List[str], amount: int) -> List[str]:
    """
    Returns a list of certain amount of words randomly selected from the
    given words list.

    Parameters:
        words (List[str]): A list a words
        amount (int): The amount of randomly selected words to return

    Returns:
        (List[str]): A list of randomly selected words
    """
    return random.choices(words, k=amount)


def get_game_solution(file_name: str, grid_size: int) -> str:
    """
    Returns the game solution as a single string.

    The game solution is the combination of a series of words randomly
    selected from the given words file.
    The amount of words the solution is composed of is equal to grid_size.
    Each word is the length of grid_size.

    e.g. If grid_size is 3, a possible returned solution is catdogpig which is
    a combination of 3 words of length 3.

    Parameters:
        file_name (str): Name of file from which words are loaded.
        grid_size (int): Size of the puzzle's grid, this determines the size of
                         words used in the puzzle.

    Returns:
        (str): The solution to the puzzle as a string.
    """
    words = load_words(file_name, grid_size)
    return "".join(get_random_words(words, grid_size))


if __name__ == "__main__":
    print("This file is not intended to be run on its own. Run a1.py instead.")
