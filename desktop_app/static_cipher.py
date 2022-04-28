""" encoder/decoder class """

import base64
from tqdm import tqdm

class Cipher():
    """ binary encoder/decoder """

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

    def co_decode(self, script, code):
        """ encode or decode file character by character acording to "code" variable value """
        content = ""
        pb_title = 'Coding' if code else 'Decoding'
        script = script.split('.')[0]
        for line in tqdm(script, desc=pb_title):
            for character in line:
                try:
                    if code:
                        content = content + self.base[character]
                    else:
                        content = content + self.yxpb[character]
                except KeyError:
                    content = content + character
            line = content
        return content


    def code_binary(self, readed_file, extension):
        """ encode binary file getting base64 encoding """
        b64_encode = base64.b64encode(readed_file)
        coded = self.co_decode(b64_encode.decode(), code=True)
        coded_extension = self.co_decode(extension, code=True)
        return [coded.encode(), ("."+coded_extension).encode()]


    def decode_binary(self, readed_file):
        """ decode binary file reading base64 enconding from txt file """
        decoded = self.co_decode(readed_file, code=False)
        output_extension = readed_file.split(".")[len(readed_file.split('.'))-1]
        decoded_output_ext = self.co_decode(output_extension, code=False)
        return base64.b64decode(decoded.encode()), decoded_output_ext
