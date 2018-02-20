import random as rd

def check_letter(x):
    # TODO DOC
    return x == 'f' or x == 'e' or x == 'd'


def RGBA_arg():
    #  Define RGBA color
    # TODO DOC
    hex_str = hex(int(rd.random()*16777215))[2:]
    hex_str = 'ffefdf'
    n = len(hex_str)
    while n < 6:
        hex_str = '0'+hex_str
        n = len(hex_str)
    if check_letter(hex_str[0]) and check_letter(hex_str[2]) and check_letter(hex_str[4]):
        index = 2*rd.randint(0,2)
        res_str = ''
        for i in range(len(hex_str)):
            if i == index:
                char = str(rd.randint(0,9))
            else:
                char = hex_str[i]
            res_str += char
        hex_str = res_str
    return '#'+hex_str