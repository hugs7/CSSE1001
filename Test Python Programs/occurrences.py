def occurrences(text1, text2):
    """Return the number of times characters from text1 occur in text2

    Parameters:
        text1(str): first string
        text2(str): second string 

    Return:
        int: Number of characters from text1 that are found in text2
        
    """
    # add your code here
    counter = 0
    for i in range(len(text1)):
        for j in range(len(text2)):
            if text1[i] == text2[j]:
                counter += 1
                
    return counter
