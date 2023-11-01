def get_names():
    name = input("Enter name: ")
    
    separate = name.partition(" ")
    
    (first, space, last) = separate

    name = (first, last)
    
    return name
