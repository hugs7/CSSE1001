def square(n):
    """Return the square of n.

    Parameters:
        n (int): Value to square 
    
    Return:
        int: The square of n
    """
    # add your code here
    return n ** 2

number = input('Please enter a number: ')
number = int(number)

number = square(number)

print(number)
