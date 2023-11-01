
number_of_entries = int(input('Please enter the number of numbers: '))

count = 0
total = 0

while count < number_of_entries:
    number = int(input('Please enter your number: '))
    total += number
    print(total)
    count += 1

avg = total // number_of_entries

print(avg)
