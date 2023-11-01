def sum_range(start, end):
    cum = 0
    for i in range(start, end):
        cum += i
        
    return cum

def sum_evens(start, end):
    cum = 0
    for i in range(start, end):
        if i % 2 == 0:
            print(i)
            cum += i
            print(str(cum) + "\n\n")
    return cum
