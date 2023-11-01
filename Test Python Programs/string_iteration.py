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
    for i in text2:
        for j in text1:
            #print(i,j)
            if i == j:
                counter += 1
                #print("Counter +1: " + str(counter))
                break
                
    return counter
