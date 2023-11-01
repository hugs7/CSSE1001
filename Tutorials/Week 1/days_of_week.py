import datetime
from datetime import date

day_names = {"No Zero Week Day", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}

day_of_month = int(input("Please input the day of the month: "))
month = int(input("Please input the month as a number (1 - 12)"))
year = int(input("Please input the year"))

day_of_week = date(year, month, day_of_month).isoweekday()

print(day_names[day_of_week])
# day = day_names[day_of_week]
# print(da
