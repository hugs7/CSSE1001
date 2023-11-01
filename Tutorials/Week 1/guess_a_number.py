import random

print("Try to guess a number I am thinking of between 1 and 100.")

number = random.randint(1, 100)
# print(number)
flag = False
guesses = 0

while flag == False:
    if guesses > 10:
        print("You've had 10 guesses and still didn't get the number.")
        break
    guess = int(input("Make a guess: "))
    guesses += 1
    if guess == number:
        flag = True
    elif guess < number:
        print("Your guess is too low.")
    elif guess > number:
        print("Your guess is too high.")

if flag == True:
    print("Congratualations, you guessed the number of " + str(number) + ".")
elif flag == False:
    print("The number was " + str(number) + ".")
