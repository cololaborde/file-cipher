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
    to_code = {}
    to_decode = {}

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
                to_code[key] = value
                to_decode[value] = key
                break
        if len(keys) == 0:
            break

    #because the indentation is important to keep in a base64 file
    to_code['']=''
    to_decode['']=''

    return to_code, to_decode

def generate_hash():
    """ create random hash """
    aux_dict = chars.copy()
    passwd = ""
    for _ in range(10):
        passwd = passwd + aux_dict[random.randint(0, (len(aux_dict) - 1))]
    return passwd


dict_of_dicts = {}

for _ in range(100):
    aux = {}
    base, yxpb = create()
    aux['base'] = base
    aux['yxpb'] = yxpb
    dict_of_dicts[generate_hash()] = aux

with open('mod.txt', 'w') as out:
    out.write(str(dict_of_dicts))