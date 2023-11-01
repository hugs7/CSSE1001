running_total = 0
avg = 0
count = 0

while True:
    number = float(input("Enter your number: "))
    if number == "":
        break;
    else:
        running_total += number
        count += 1

avg = running_total / count

print(str(avg))
