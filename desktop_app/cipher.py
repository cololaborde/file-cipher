""" encoder/decoder class """

from abc import abstractmethod
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

    @staticmethod
    def read_mod(keypath):
        """ return readed and converted to hashmap mod file """
        with open(keypath, 'r', encoding='utf-8') as mod:
            mod_read = mod.read()
            mod_dict = literal_eval(mod_read)
            return mod_dict

    @abstractmethod
    def code_binary(self, readed_file, extension, key_path):
        """ code binary """

    @abstractmethod
    def decode_binary(self, readed_file, key_path):
        """ decode binary """

    def co_decode(self, script, code):
        """ encode or decode file character by character acording to "code" variable value """
        content = ""
        pb_title = 'Coding' if code else 'Decoding'
        script = script.split('.')[0]
        _b = self.get_base()
        _y = self.get_yxpb()
        if not _b or not _y:
            return None
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

    def __init__(self, keypath):
        """ init method set base and yxpb dicts """
        base, yxpb = self.get_key(keypath)
        self.set_base(base)
        self.set_yxpb(yxpb)

    def get_key(self, keypath):
        """ return mod to use """
        mod_dict = self.read_mod(keypath)
        try:
            return mod_dict['base'], mod_dict['yxpb']
        except KeyError:
            print('incorrect key file')
            return None, None

    def code_binary(self, readed_file, extension, key_path):
        """ encode binary file getting base64 encoding """
        b64_encode = b64encode(readed_file)
        coded = self.co_decode(b64_encode.decode(), code=True)
        coded_extension = self.co_decode(extension, code=True)
        if not coded or not coded_extension:
            return []
        return [coded.encode(), ("."+coded_extension).encode()]

    def decode_binary(self, readed_file, key_path):
        """ decode binary file reading base64 enconding from txt file """
        decoded = self.co_decode(readed_file, code=False)
        output_extension = readed_file.split(
            ".")[len(readed_file.split('.'))-1]
        decoded_output_ext = self.co_decode(output_extension, code=False)
        if not decoded or not decoded_output_ext:
            return None, None
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

    def read_key_from_file(self, mod):
        """ return selected random hashmaps to code/decode """
        hash_list = list(mod)
        new_hash = hash_list[randint(0, len(hash_list)-1)]
        self.set_current_hash(new_hash)
        try:
            to_co_decode_dict = mod[self.get_current_hash()]
            to_code = to_co_decode_dict['base']
            to_decode = to_co_decode_dict['yxpb']
        except KeyError:
            print('incorrect key file')
            return None, None
        return to_code, to_decode

    def get_key(self, code, script, keypath):
        """ determine and return the key used to decode and what will used to code """
        mod_dict = self.read_mod(keypath)
        if not code and len(script.split('.')) > 1:
            self.set_current_hash(script.split('.')[1])
        if (code and self.get_current_hash() != '') or (not code):
            try:
                base = mod_dict[self.get_current_hash()]['base']
                yxpb = mod_dict[self.get_current_hash()]['yxpb']
            except KeyError:
                print('incorrect key file')
                return None, None
        else:
            base, yxpb = self.read_key_from_file(mod_dict)
        return base, yxpb

    def code_binary(self, readed_file, extension, key_path):
        """ encode binary file getting base64 encoding """
        b64_encode = b64encode(readed_file)
        base, yxpb = self.get_key(True, b64_encode.decode(), key_path)
        if not base or not yxpb:
            return []
        self.set_base(base)
        self.set_yxpb(yxpb)
        coded = self.co_decode(b64_encode.decode(), code=True)
        rand_key = self.get_current_hash()
        coded_extension = self.co_decode(extension, code=True)
        self.set_current_hash("")
        return [coded.encode(), ('.' + rand_key).encode(), ('.' + coded_extension).encode()]

    def decode_binary(self, readed_file, key_path):
        """ decode binary file reading base64 enconding from txt file """
        base, yxpb = self.get_key(False, readed_file, key_path)
        if not base or not yxpb:
            return None, None
        self.set_base(base)
        self.set_yxpb(yxpb)
        decoded = self.co_decode(readed_file, code=False)
        output_extension = readed_file.split(
            ".")[len(readed_file.split("."))-1]
        decoded_output_ext = self.co_decode(output_extension, code=False)
        if not decoded or not decoded_output_ext:
            return None, None
        self.set_current_hash("")
        return b64decode(decoded.encode()), decoded_output_ext
