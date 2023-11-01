def get_digits(str1):
    global str2
    str2 = ""
    for i in str1:
        if i.isdigit():
            str2 += i
    return str2
