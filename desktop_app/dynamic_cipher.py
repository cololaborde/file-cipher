""" encoder/decoder class """

import base64
import random
import ast
from tqdm import tqdm

class Cipher():
    """ binary encoder/decoder """

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
            mod_dict = ast.literal_eval(mod_read)
            return mod_dict


    def read_key_from_file(self, mod):
        """ return selected random hashmaps to code/decode """
        hash_list = list(mod)
        new_hash = hash_list[random.randint(0, len(hash_list)-1)]
        self.set_current_hash(new_hash)
        to_co_decode_dict = mod[self.get_current_hash()]
        to_code = to_co_decode_dict['base']
        to_decode = to_co_decode_dict['yxpb']
        return to_code, to_decode
        

    def get_key(self, code, script, mod_dict):
        if not code and len(script.split('.')) > 1:
            self.set_current_hash(script.split('.')[1])
        if (code and self.get_current_hash() != '') or (not code):
            base = mod_dict[self.get_current_hash()]['base']
            yxpb = mod_dict[self.get_current_hash()]['yxpb']
        else:
            base, yxpb = self.read_key_from_file(mod_dict)
        return base, yxpb


    def co_decode(self, script, code):
        """ encode or decode file character by character acording to "code" variable value """
        # determining hashmap to use
        mod_dict = self.read_mod()

        base, yxpb = self.get_key(code, script, mod_dict)
        # starting ciph
        content = ""
        pb_title = 'Coding' if code else 'Decoding'
        script = script.split('.')[0]
        for line in tqdm(script, desc=pb_title):
            for character in line:
                try:
                    if code:
                        content = content + base[character]
                    else:
                        content = content + yxpb[character]
                except KeyError:
                    content = content + character
            line = content
        return content


    def code_binary(self, readed_file, extension):
        """ encode binary file getting base64 encoding """
        b64_encode = base64.b64encode(readed_file)
        coded = self.co_decode(b64_encode.decode(), code=True)
        rand_key = self.get_current_hash()
        coded_extension = self.co_decode(extension, code=True)
        self.set_current_hash("")
        return [coded.encode(), ('.' + rand_key).encode(), ('.' + coded_extension).encode()]


    def decode_binary(self, readed_file):
        """ decode binary file reading base64 enconding from txt file """
        decoded = self.co_decode(readed_file, code=False)
        output_extension = readed_file.split(".")[len(readed_file.split("."))-1]
        decoded_output_ext = self.co_decode(output_extension, code=False)
        self.set_current_hash("")
        return base64.b64decode(decoded.encode()), decoded_output_ext
