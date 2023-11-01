"""A program to calculate tax payable

More information about the program
"""

__author__ = "Hugo Burton"

TAX_FREE_THRESHOLD = int(18200)
tax_rate = float(input("Enter your tax rate: (%)"))
income = float(input("Enter your gross income: $"))

car_cost = float(input("Enter your car usage cost: $"))
prof_dev_cost = float(input("Enter your professional development cost: $"))

if(income >= TAX_FREE_THRESHOLD):
    income = income - TAX_FREE_THRESHOLD
    deductions = tax_rate * (car_cost + prof_dev_cost)
    print("Deducted cost: " + str(deductions))
    tax_payable = tax_rate * (income - deductions)
    print ("Your tax owning amount is $" + str(tax_payable))
