"""
Sliding Puzzle Game
Assignment 1
Semester 1, 2021
CSSE1001/CSSE7030
"""

import math
from typing import Optional
from a1_support import *


# Replace these <strings> with your name, student number and email address.
__author__ = "Hugo Burton, s4698512"
__email__ = "hugo.burton@uqconnect.edu.au"
__date__ = "10/3/2021"

# Functions


def shuffle_puzzle(solution: str) -> str:
    """
    Shuffle a puzzle solution to produce a solvable sliding puzzle.
    
    Parameters:
        solution (str): a solution to be converted into a shuffled puzzle.
    
    Returns:
        (str): a solvable shuffled game with an empty tile at the
               bottom right corner.
    
    References:
        - https://en.wikipedia.org/wiki/15_puzzle#Solvability
        - https://www.youtube.com/watch?v=YI1WqYKHi78&ab_channel=Numberphile
    
    Note: This function uses the swap_position function that you have to
          implement on your own. Use this function when the swap_position
          function is ready
    """
    shuffled_solution = solution[:-1]
    
    # Do more shuffling for bigger puzzles.
    swaps = len(solution) * 2
    for _ in range(swaps):
        # Pick two indices in the puzzle randomly.
        index1, index2 = random.sample(range(len(shuffled_solution)), k=2)
        shuffled_solution = swap_position(shuffled_solution, index1, index2)
    
    return shuffled_solution + EMPTY

# Write your functions here


def check_win(puzzle: str, solution: str) -> bool:
    """
    Checks for a win
    
    Parameters:
        puzzle (str): current state of the grid
        solution (str): solved grid

    Returns:
        (bool): a win flag. True is user has won; False if game is in progress
    """

    solution_list = list(solution)
    solution_list[-1] = EMPTY               # Makes last character a blank
    solution = "".join(solution_list)
    
    return puzzle == solution               # Return a bool flag


def swap_position(puzzle: str, from_index: int, to_index: int) -> str:
    """
    Swaps position of two characters
    
    Parameters:
        puzzle (str): current state of the grid
        from_index (int): position of character that to_index's character will
                          go to
        to_index (int): position of character that from_index's character will
                        go to
    
    Returns:
        (str): puzzle as string with two characters switched
    """
    
    puzzle_list = list(puzzle)
    
    # Gets characters to be switched
    from_char = puzzle_list[from_index]
    to_char = puzzle_list[to_index]
    
    # Switches characters
    puzzle_list[to_index] = from_char
    puzzle_list[from_index] = to_char
    
    puzzle = "".join(puzzle_list)
    
    return puzzle


def move(puzzle: str, direction: str) -> Optional[str]:
    """
    Moves empty tile in given direction

    Parameters:
        puzzle (str): current state of the grid
        direction (str): user input of which direction to move white space

    Returns:
        Optional (str): puzzle as string updated according to user's input
                        will return 'None' if user enters invalid move
    """
    
    word_len = int(math.sqrt(len(puzzle)))  # Word len -> sqrt string length
    
    white_index = puzzle.index(" ")         # Indexed position of white square

    move_piece = ""                         # Set blank to check for later

    # Determine action from user's move
    if direction == UP:
        if white_index - word_len >= 0:
            move_piece = white_index - word_len
    elif direction == DOWN:
        if white_index + word_len < len(puzzle):
            move_piece = white_index + word_len
    elif direction == LEFT:
        if white_index % word_len != 0:
            move_piece = white_index - 1
    elif direction == RIGHT:
        if white_index % word_len != (word_len - 1):
            move_piece = white_index + 1

    if move_piece != "":
        return swap_position(puzzle, white_index, move_piece)
    else:
        return None


def print_grid(puzzle: str) -> None:
    """
    Prints the puzzle in a friendly format

    Parameters:
        puzzle (str): current state of the grid

    Returns:
        None
    """

    word_len = int(math.sqrt(len(puzzle)))      # Word length -> sqrt of puzzle

    for row in range(word_len):                 # For each row
        print(word_len * (CORNER + HORIZONTAL_WALL * 3) + CORNER)
        for column in range(word_len):          # For each column
            index = row * word_len + column     # Index of cell in grid
            print(VERTICAL_WALL + EMPTY + puzzle[index] + EMPTY, end='')
        print(VERTICAL_WALL)                    # Last character for each row
    print(word_len * (CORNER + HORIZONTAL_WALL * 3) + CORNER)


def main():
    """Entry point to gameplay"""

    valid_inputs = [UP, DOWN, LEFT, RIGHT]

    print(WELCOME_MESSAGE)
    
    playing = True                      # While user hasn't given up

    while playing:
        win = False                     # Win flag
        input_flag = False              # User input flag

        # Difficulty prompt
        while not input_flag:
            word_len = input(BOARD_SIZE_PROMPT)

            try:                        # Attempt to convert to integer
                word_len = int(word_len)
            except ValueError:          # If not integer type, print error
                print(INVALID_MESSAGE)
                continue
        
            if word_len in range(2, 14 + 1):
                input_flag = True

        # Get solution and shuffle
        solution = get_game_solution(WORDS_FILE, word_len)
        puzzle = shuffle_puzzle(solution)
        
        # Main Game Loop
        while not win:                  # While user hasn't solved puzzle
            # Print out grids
            print("Solution:")
            print_grid(solution)        # Solved puzzle
            print("\nCurrent position:")
            print_grid(puzzle)          # Current state of the puzzle
            print("")
            
            # Win check
            win = check_win(puzzle, solution)
            if win:                     # Prompt user for another game
                print(WIN_MESSAGE)
                play_again = input(PLAY_AGAIN_PROMPT).upper()
                if play_again == "Y" or play_again == "":
                    break
                else:
                    print(BYE)
                    return

            # User input for move
            user_input = input(DIRECTION_PROMPT).upper()
            
            if user_input == HELP:          # User requests controls
                print(HELP_MESSAGE)
            elif user_input == GIVE_UP:     # Forfeit; ask user to play again
                print(GIVE_UP_MESSAGE)
                play_again = input(PLAY_AGAIN_PROMPT).upper()
                if play_again == "Y" or "":
                    break
                else:
                    print(BYE)
                    return
            elif user_input == "CHEAT":      # Cheat code
                puzzle = solution[:-1] + EMPTY
                print("You have entered the ultimate cheat code!\n")
            elif user_input in valid_inputs:    # All other inputs
                update = move(puzzle, user_input)
                if update is None:
                    print(INVALID_MOVE_FORMAT.format(user_input))
                else:
                    puzzle = update
            else:
                print(INVALID_MESSAGE)


if __name__ == "__main__":
    main()
