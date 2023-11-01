import random

print("Welcome to Alice's addition. Two integers, each between 0 and 9, have been added together. Try to guess their sum.")

rand1, rand2 = random.randint(0, 9), random.randint(0, 9)
sumrand = rand1 + rand2
# print(sumrand)
guesses = 0
flag = False

while flag == False:
    if guesses > 10:
        print("You've had too many unsuccessful guesses.")
        break
    guess = int(input("Enter your sum: "))
    guesses += 1
    if guess == sumrand:
        flag = True
    elif guess < sumrand:
        print("Your guess was too low.")
    elif guess > sumrand:
        print("Your guess was too high.")

if flag == True:
    print("Your guess was correct. The numbers were " + str(rand1) + " and " + str(rand2) + ". And therefore, the sum of the numbers is " + str(sumrand) + ".")
elif flag == False:
    print("The numbers were " + str(rand1) + " and " + str(rand2) + ". And therefore, the sum of the numbers is " + str(sumrand) + ".")
