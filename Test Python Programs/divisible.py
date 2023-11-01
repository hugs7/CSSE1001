def div_3_5(start, end):
    counter = start
    count = 0
    while counter < end:
        if counter % 3 == 0:
            count += 1
            # print (str(counter) + " divisible by 3")
        elif counter % 5 == 0:
            count += 1
            # print (str(counter) + " divisible by 5")
        counter += 1
    return count

s = float(input("Input starting number: "))
e = float(input("Input ending number: "))

c = div_3_5(s, e)

print(c)
