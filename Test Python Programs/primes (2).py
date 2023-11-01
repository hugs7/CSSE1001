upper_limit = int(input("Upper check limit: "))

for i in range(2, upper_limit + 1):
    divisible = False
    for j in range(2, i):
        if i % j == 0:
            divisible = True
            break
    if not divisible:
        print(i)
        
