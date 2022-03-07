""" dictionary generator """

import random

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
     'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o',
     'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
     'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
     'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
     'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T',
     'U', 'V', 'W', 'X', 'Y', 'Z', '¿', '?',
     '=', '+', '-', '/', '>', '<', ',','[',
     ']', ' ', '_', '!', '¡', ':', ';', '1',
     '2', '3', '4', '5', '6', '7', '8', '9']

def create():
    """ generate and return codification/decodification dictionary """
    b = {}
    y = {}

    keys = chars.copy()
    values = chars.copy()

    while True:
        index = random.randint(0, len(keys)-1)
        key = keys[index]
        while True:
            index_value = random.randint(0, len(values)-1)
            value = values[index_value]
            if value != key:
                keys.pop(index)
                values.pop(index_value)
                b[key] = value
                y[value] = key
                break
        if len(keys) == 0:
            break

    #because the indentation is important to keep in a base64 file
    b['']=''
    y['']=''

    return b, y

base, yxpb = create()

print('base = '+str(base))
print('yxpb = '+str(yxpb))
