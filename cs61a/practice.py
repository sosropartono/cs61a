def cascade(number):
    if number < 10:
        return number
    else:
        print(number)
        return cascade(number//10)
        print(number)
        