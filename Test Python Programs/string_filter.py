def filter_string_2(str1, str2):
    for i in str1:
        if i in str2:
            str1 = str1.replace(i,"")
    return str1
