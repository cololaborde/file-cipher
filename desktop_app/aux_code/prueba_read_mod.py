import ast
import random

def get_base_yxpb(mod):
    hash_list = [key for key in mod]
    to_co_decode_hash = hash_list[random.randint(0, len(hash_list)-1)]
    to_co_decode_dict = mod[to_co_decode_hash]
    to_code = to_co_decode_dict['base']
    to_decode = to_co_decode_dict['yxpb']
    return to_code, to_decode


with open('mod.txt', 'r') as mod:
    mod_read = mod.read()
    mod_dict = ast.literal_eval(mod_read)
    print(mod_dict['QHSD!RhJh='])