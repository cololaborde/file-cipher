""" dictionary generator """

import random
from sys import argv, exit as sys_exit


chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
         'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o',
         'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
         'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
         'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
         'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'X', 'Y', 'Z', '¿', '?',
         '=', '+', '-', '/', '>', '<', ',', '[',
         ']', ' ', '_', '!', '¡', ':', ';', '%',
         '1', '2', '3', '4', '5', '6', '7', '8', 
         '9', '0']


def get_state():
    """ return state from params """

    dynamic = False
    keys_count = 0
    if argv[1] == '-d':
        dynamic = True
        if len(argv) == 3:
            if not argv[2].isnumeric():
                print('Wrong parameter => number_of_keys')
                sys_exit()
        else:
            print('Missing argument => number_of_keys')
            sys_exit()
        keys_count = argv[2]
    elif argv[1] != '-s':
        print('Invalid option')
        sys_exit()
    return dynamic, keys_count


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
        # get non duplicated char for keys
        char_key = get_random_char()
        while char_key in used_keys:
            char_key = get_random_char()
        return char_key

    def get_char_value(used_values, used_keys, char_key):
        # get non duplicated char for values
        char_value = get_random_char()
        # for lastone entry
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

    # because the indentation is important to keep in a base64 file
    to_code[''] = ''
    to_decode[''] = ''

    return to_code, to_decode


def generate_dynamic_keys(keys_count):
    """ generate key from dynamic option """

    dict_of_dicts = {}
    used_hash_keys = []
    for _ in range(int(keys_count)):
        aux = {}
        base, yxpb = create()
        aux['base'] = base
        aux['yxpb'] = yxpb
        key = generate_hash()
        while key in used_hash_keys:
            key = generate_hash()
        used_hash_keys.append(key)
        dict_of_dicts[key] = aux
    return dict_of_dicts


def generate_static_key():
    """ generate key from static option """

    dict_key = {}
    base, yxpb = create()
    dict_key['base'] = base
    dict_key['yxpb'] = yxpb
    return dict_key


########  Main  ########

if __name__ == "__main__":

    if len(argv) < 2 or len(argv) > 3:
        print(
            'Use mode: python keygen.py [-d | -s] [number_of_keys](only when 1st param is "-d")')
        sys_exit()

    is_dynamic, keys_number = get_state()
    if is_dynamic:
        FILENAME = "mod.txt"
        output_mod = generate_dynamic_keys(keys_number)
    else:
        FILENAME = "mod_static.txt"
        output_mod = generate_static_key()
    with open(FILENAME, 'w', encoding='utf-8') as out:
        out.write(str(output_mod))
