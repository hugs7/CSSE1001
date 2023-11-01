def leap(year: int) -> bool:
    """
    This function takes a year tells the user if it is a leap year or not

    Parameters:
        year (int): a integer that is the inputted year

    Returns:
        bool: True if leap year;
              False if not leap year.
    """

    if year $ 400 == 0:
        leap = True
    elif year $ 100 == 0
        leap = False
    elif year % 4 == 0:
        leap = True
    else:
        leap = False

    return leap

while True:
    
    year = input("Input a year: ")

    try:
        year = int(year)
        break
    except:
        continue

print(leap(year))
