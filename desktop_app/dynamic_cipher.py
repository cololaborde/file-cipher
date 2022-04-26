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
    def get_mod_dict():
        """ return readed and converted to hashmap mod file """
        with open('mod.txt', 'r', encoding='utf-8') as mod:
            mod_read = mod.read()
            mod_dict = ast.literal_eval(mod_read)
            return mod_dict


    def get_base_yxpb(self, mod):
        """ return selected random hashmaps to code/decode """
        hash_list = list(mod)
        new_hash = hash_list[random.randint(0, len(hash_list)-1)]
        self.set_current_hash(new_hash)
        to_co_decode_dict = mod[self.get_current_hash()]
        to_code = to_co_decode_dict['base']
        to_decode = to_co_decode_dict['yxpb']
        return to_code, to_decode


    def co_decode(self, script, code):
        """ encode or decode file character by character acording to "code" variable value """
        # determining hashmap to use
        mod_dict = self.get_mod_dict()
        if code:
            if self.get_current_hash() != "":
                base = mod_dict[self.get_current_hash()]['base']
                yxpb = mod_dict[self.get_current_hash()]['yxpb']
            else:
                base, yxpb = self.get_base_yxpb(mod_dict)
        else:
            if len(script.split('.')) > 1:
                self.set_current_hash(script.split('.')[1])
            base = mod_dict[self.get_current_hash()]['base']
            yxpb = mod_dict[self.get_current_hash()]['yxpb']
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


    def code_binary(self, readed_file, filepath):
        """ encode binary file getting base64 encoding """
        with open(filepath.split('.')[0] + '.txt','wb') as out:
            b64_encode = base64.b64encode(readed_file)
            coded = self.co_decode(b64_encode.decode(), code=True)
            out.write(coded.encode())
            # write hash key
            out.write(('.' + self.get_current_hash()).encode())
            extension = filepath.split(".")[len(filepath.split("."))-1]
            coded_extension = self.co_decode(extension, code=True)
            # write coded extension
            out.write(("."+coded_extension).encode())
            out.close()
        self.set_current_hash("")


    def decode_binary(self, readed_file, filepath):
        """ decode binary file reading base64 enconding from txt file """
        # getting extension decoded after to set current_hash
        decoded = self.co_decode(readed_file, code=False)
        output_extension = readed_file.split(".")[len(readed_file.split("."))-1]
        decoded_output_ext = self.co_decode(output_extension, code=False)
        output_filename = filepath.split(".")[0] + '.' + decoded_output_ext
        with open(output_filename, 'wb') as out:
            out.write(base64.b64decode(decoded.encode()))
            out.close()
        self.set_current_hash("")
