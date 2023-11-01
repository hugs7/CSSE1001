
number_of_entries = int(input('Please enter the number of numbers: '))

running_total = 0

for i in range (0, number_of_entries):
    eemp = input("Enter number: ")
    running_total += int(eemp)
    print("Running total: " + str(running_total))

average = running_total // number_of_entries

print("Average: " + str(average))
