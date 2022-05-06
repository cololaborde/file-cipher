""" encoder/decoder class """

from ast import literal_eval
from base64 import b64encode, b64decode
from random import randint
from tqdm import tqdm

class Cipher():
    """ binary encoder/decoder """

    base, yxpb = {}, {}

    @classmethod
    def get_base(cls):
        """ get current base dictionary """
        return cls.base

    @classmethod
    def set_base(cls, new_base):
        """ set current base dictionary """
        cls.base = new_base

    @classmethod
    def get_yxpb(cls):
        """ get current yxpb dictionary """
        return cls.yxpb

    @classmethod
    def set_yxpb(cls, new_yxpb):
        """ get current yxpb dictionary """
        cls.yxpb = new_yxpb


    def co_decode(self, script, code):
        """ encode or decode file character by character acording to "code" variable value """
        content = ""
        pb_title = 'Coding' if code else 'Decoding'
        script = script.split('.')[0]
        _b = self.get_base()
        _y = self.get_yxpb()
        for line in tqdm(script, desc=pb_title):
            for character in line:
                try:
                    if code:
                        content = content + _b[character]
                    else:
                        content = content + _y[character]
                except KeyError:
                    content = content + character
            line = content
        return content


class StaticCipher(Cipher):

    """ static coder/decoder """

    def __init__(self):
        """ init method set base and yxpb dicts """
        base = {'I': 'B', 'E': 'Ñ', 'Q': 'm', '=': 'G',
        'j': 'Z', 'V': '5', 't': 'I', '5': 'u', 'f': 'b',
        ',': 'H', '1': 'o', 'W': 'z', 'p': '9', 'e': 'c',
        'O': 'g', '<': 'R', 'Z': '¿', '?': 'w', 'B': 'P',
        '6': 'U', 'H': 'x', '¡': 'e', '>': 'a', '_': 'M',
        '7': 'l', 'l': 'd', 'b': 'E', 'D': 'C', '2': 'y',
        '[': '=', 'a': 'X', 'L': 'ñ', 'g': ';', ':': 'T',
        'u': 'A', '¿': 's', 'c': 'W', 'Ñ': 'D', 'z': 'p',
        ']': 'J', 'N': '8', 'x': 'k', 'r': 'F', 'X': 'h',
        '!': 'j', 'v': '1', ' ': '?', 'J': 'L', 'm': '6',
        'ñ': 'r', 'G': '>', '8': 'i', 's': 'Q', 'w': 'K',
        'o': '7', ';': ',', 'k': 'S', 'U': '¡', 'M': ':',
        'F': '4', 'K': 'V', 'h': '_', 'S': '/', 'A': 'n',
        '/': 'f', 'q': '+', 'R': 'N', 'Y': '[', 'y': 'q',
        '-': ' ', '+': '-', '9': 't', 'i': 'Y', '3': '<',
        'd': 'v', '4': '2', 'n': '3', 'T': 'O', 'C': ']',
        'P': '!', '': ''}
        yxpb = {'B': 'I', 'Ñ': 'E', 'm': 'Q', 'G': '=',
        'Z': 'j', '5': 'V', 'I': 't', 'u': '5', 'b': 'f',
        'H': ',', 'o': '1', 'z': 'W', '9': 'p', 'c': 'e',
        'g': 'O', 'R': '<', '¿': 'Z', 'w': '?', 'P': 'B',
        'U': '6', 'x': 'H', 'e': '¡', 'a': '>', 'M': '_',
        'l': '7', 'd': 'l', 'E': 'b', 'C': 'D', 'y': '2',
        '=': '[', 'X': 'a', 'ñ': 'L', ';': 'g', 'T': ':',
        'A': 'u', 's': '¿', 'W': 'c', 'D': 'Ñ', 'p': 'z',
        'J': ']', '8': 'N', 'k': 'x', 'F': 'r', 'h': 'X',
        'j': '!', '1': 'v', '?': ' ', 'L': 'J', '6': 'm',
        'r': 'ñ', '>': 'G', 'i': '8', 'Q': 's', 'K': 'w',
        '7': 'o', ',': ';', 'S': 'k', '¡': 'U', ':': 'M',
        '4': 'F', 'V': 'K', '_': 'h', '/': 'S', 'n': 'A',
        'f': '/', '+': 'q', 'N': 'R', '[': 'Y', 'q': 'y',
        ' ': '-', '-': '+', 't': '9', 'Y': 'i', '<': '3',
        'v': 'd', '2': '4', '3': 'n', 'O': 'T', ']': 'C',
        '!': 'P', '': ''}
        self.set_base(base)
        self.set_yxpb(yxpb)


    def code_binary(self, readed_file, extension):
        """ encode binary file getting base64 encoding """
        b64_encode = b64encode(readed_file)
        coded = self.co_decode(b64_encode.decode(), code=True)
        coded_extension = self.co_decode(extension, code=True)
        return [coded.encode(), ("."+coded_extension).encode()]


    def decode_binary(self, readed_file):
        """ decode binary file reading base64 enconding from txt file """
        decoded = self.co_decode(readed_file, code=False)
        output_extension = readed_file.split(".")[len(readed_file.split('.'))-1]
        decoded_output_ext = self.co_decode(output_extension, code=False)
        return b64decode(decoded.encode()), decoded_output_ext



class DynamicCipher(Cipher):
    """ dynamic coder/decoder """

    current_hash = ""

    @classmethod
    def get_current_hash(cls):
        """ get current hash """
        return cls.current_hash


    @classmethod
    def set_current_hash(cls, new_hash):
        """ set current hash """
        cls.current_hash = new_hash

    @staticmethod
    def read_mod():
        """ return readed and converted to hashmap mod file """
        with open('mod.txt', 'r', encoding='utf-8') as mod:
            mod_read = mod.read()
            mod_dict = literal_eval(mod_read)
            return mod_dict


    def read_key_from_file(self, mod):
        """ return selected random hashmaps to code/decode """
        hash_list = list(mod)
        new_hash = hash_list[randint(0, len(hash_list)-1)]
        self.set_current_hash(new_hash)
        to_co_decode_dict = mod[self.get_current_hash()]
        to_code = to_co_decode_dict['base']
        to_decode = to_co_decode_dict['yxpb']
        return to_code, to_decode


    def get_key(self, code, script):
        """ determine and return the key used to decode and what will used to code """
        mod_dict = self.read_mod()
        if not code and len(script.split('.')) > 1:
            self.set_current_hash(script.split('.')[1])
        if (code and self.get_current_hash() != '') or (not code):
            base = mod_dict[self.get_current_hash()]['base']
            yxpb = mod_dict[self.get_current_hash()]['yxpb']
        else:
            base, yxpb = self.read_key_from_file(mod_dict)
        return base, yxpb


    def code_binary(self, readed_file, extension):
        """ encode binary file getting base64 encoding """
        b64_encode = b64encode(readed_file)
        base, yxpb = self.get_key(True, b64_encode.decode())
        self.set_base(base)
        self.set_yxpb(yxpb)
        coded = self.co_decode(b64_encode.decode(), code=True)
        rand_key = self.get_current_hash()
        coded_extension = self.co_decode(extension, code=True)
        self.set_current_hash("")
        return [coded.encode(), ('.' + rand_key).encode(), ('.' + coded_extension).encode()]


    def decode_binary(self, readed_file):
        """ decode binary file reading base64 enconding from txt file """
        base, yxpb = self.get_key(False, readed_file)
        self.set_base(base)
        self.set_yxpb(yxpb)
        decoded = self.co_decode(readed_file, code=False)
        output_extension = readed_file.split(".")[len(readed_file.split("."))-1]
        decoded_output_ext = self.co_decode(output_extension, code=False)
        self.set_current_hash("")
        return b64decode(decoded.encode()), decoded_output_ext
