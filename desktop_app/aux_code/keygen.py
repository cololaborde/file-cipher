""" dictionary generator """

import random
import sys
from sys import argv


chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
     'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o',
     'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
     'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
     'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
     'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T',
     'U', 'V', 'W', 'X', 'Y', 'Z', '¿', '?',
     '=', '+', '-', '/', '>', '<', ',','[',
     ']', ' ', '_', '!', '¡', ':', ';', '%',
     '1', '2', '3', '4', '5', '6', '7', '8', '9']


def generate_hash():
    """ create random hash """
    aux_dict = chars.copy()
    passwd = ""
    for _ in range(10):
        passwd = passwd + aux_dict[random.randint(0, len(aux_dict) - 1)]
    return passwd


def create():
    """ generate and return codification/decodification dictionary """

    def get_random_char():
        return chars[random.randint(0, len(chars)-1)]

    def get_char_key(used_keys):
        #get non duplicated char for keys
        char_key = get_random_char()
        while char_key in used_keys:
            char_key = get_random_char()
        return char_key

    def get_char_value(used_values, used_keys, char_key):
        #get non duplicated char for values
        char_value = get_random_char()
        #for lastone entry
        if len(used_keys) == len(chars):
            while char_value in used_values:
                char_value = chars[random.randint(0, len(chars)-1)]
        else:
            while char_key == char_value or char_value in used_values:
                char_value = chars[random.randint(0, len(chars)-1)]
        return char_value

    to_code = {}
    to_decode = {}
    used_keys = []
    used_values = []

    for _ in range(len(chars)):
        char_key = get_char_key(used_keys)
        used_keys.append(char_key)

        char_value = get_char_value(used_values, used_keys, char_key)
        used_values.append(char_value)

        to_code[char_key] = char_value
        to_decode[char_value] = char_key

    #because the indentation is important to keep in a base64 file
    to_code['']=''
    to_decode['']=''

    return to_code, to_decode


########  Main  ########

if __name__ == "__main__":

    dict_of_dicts = {}
    used_hash_keys = []

    if len(argv) < 2 or not argv[1].isnumeric():
        print('Missing arguments: keys quantity')
        sys.exit()
    for i in range(int(argv[1])):
        aux = {}
        base, yxpb = create()
        aux['base'] = base
        aux['yxpb'] = yxpb
        key = generate_hash()
        while key in used_hash_keys:
            key = generate_hash()
        used_hash_keys.append(key)
        dict_of_dicts[key] = aux
    with open('mod.txt', 'w', encoding='utf-8') as out:
        out.write(str(dict_of_dicts))
