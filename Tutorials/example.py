"""
Calculator program
Example assignment
Semester 1, 2021
CSSE1001
"""

__author__ = "Hugo Burton, s4698512"
__email__ = "hugo.burton@uqconnect.edu.au"
__date__ = "3/3/2021"

def add(x: int, y: int) -> int:
    """
    Adds two numbers together

    Parameters:
        x (int): first number to be added
        y (int): second number to be added

    Returns:
        (int): sum of x and y
    
    """
    summation = x + y

    return summation

def multiply(x: int, y: int) -> int:
    """
    Multiplies two numbers together

    Parameters:
        x (int): first number to be multiplied
        y (int): second number to be multiplied

    Returns:
        (int): product of x and y
    
    """
    product = x * y

    return product

def main() -> None:
    """Main excecution of code in this program."""
    while True:
        flag = False
        while flag == False:
            QUESTION = "What would you like to do?: "
            user_input = input(QUESTION).upper()
            if user_input == "ADD" or user_input == "MULTIPLY" or user_input == "Q":
                flag = True

        if user_input == "ADD":
            action = "added"
        elif user_input == "MULTIPLY":
            action = "multiply"
        elif user_input == "Q":
            answer = input("Are you sure you want to quit? (y/n): ")
            if answer == "y" or answer == "Y":
                return
            else:
                continue

                
        flag = False
        while flag == False:
            x = input("Please type in the first number to be " + action + ": ")
            
            try:
                x = int(x)
                flag = True
            except:
                print("That is not a valid input. Please try again")
                continue

        flag = False
        while flag == False:
            y = input("Please type in the second number to be " + action + ": ")
            
            try:
                y = int(y)
                flag = True
            except:
                print("That is not a valid input. Please try again")
                continue
        
        if user_input == "ADD":
            answer = add(x, y)
            print("The sum of the numbers is " + str(answer) + ".")
        elif user_input == "MULTIPLY":
            answer = multiply(x, y)
            print("The product of the numbers is " + str(answer) + ".")

if __name__ == "__main__":
    main()
