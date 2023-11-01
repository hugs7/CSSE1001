total_primes = 0

def check_div(i):
    global total_primes
    n = 0
    for j in range(2, i):
        if i % j != 0:
            n = i
            if j == i - 1:
                print(i)
                total_primes += 1
        else:
            n = False
            break
    return n
    

e = int(input("Enter maximum prime: "))

# for 2
print(2)
total_primes += 1

for i in range(2, e + 1):
    numb = check_div(i)
    if numb == False:
        continue

print("total primes: " + str(total_primes))
