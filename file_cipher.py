""" coder and decoder file """

import tkinter
from tkinter import filedialog, messagebox
import base64
from tqdm import tqdm

base = {'I': 'B', 'E': 'Ñ', 'Q': 'm', '=': 'G', 'j': 'Z', 'V': '5', 't': 'I', '5': 'u', 'f': 'b', ',': 'H', '1': 'o', 'W': 'z', 'p': '9', 'e': 'c', 'O': 'g', '<': 'R', 'Z': '¿', '?': 'w', 'B': 'P', '6': 'U', 'H': 'x', '¡': 'e', '>': 'a', '_': 'M', '7': 'l', 'l': 'd', 'b': 'E', 'D': 'C', '2': 'y', '[': '=', 'a': 'X', 'L': 'ñ', 'g': ';', ':': 'T', 'u': 'A', '¿': 's', 'c': 'W', 'Ñ': 'D', 'z': 'p', ']': 'J', 'N': '8', 'x': 'k', 'r': 'F', 'X': 'h', '!': 'j', 'v': '1', ' ': '?', 'J': 'L', 'm': '6', 'ñ': 'r', 'G': '>', '8': 'i', 's': 'Q', 'w': 'K', 'o': '7', ';': ',', 'k': 'S', 'U': '¡', 'M': ':', 'F': '4', 'K': 'V', 'h': '_', 'S': '/', 'A': 'n', '/': 'f', 'q': '+', 'R': 'N', 'Y': '[', 'y': 'q', '-': ' ', '+': '-', '9': 't', 'i': 'Y', '3': '<', 'd': 'v', '4': '2', 'n': '3', 'T': 'O', 'C': ']', 'P': '!', '': ''}

yxpb = {'B': 'I', 'Ñ': 'E', 'm': 'Q', 'G': '=', 'Z': 'j', '5': 'V', 'I': 't', 'u': '5', 'b': 'f', 'H': ',', 'o': '1', 'z': 'W', '9': 'p', 'c': 'e', 'g': 'O', 'R': '<', '¿': 'Z', 'w': '?', 'P': 'B', 'U': '6', 'x': 'H', 'e': '¡', 'a': '>', 'M': '_', 'l': '7', 'd': 'l', 'E': 'b', 'C': 'D', 'y': '2', '=': '[', 'X': 'a', 'ñ': 'L', ';': 'g', 'T': ':', 'A': 'u', 's': '¿', 'W': 'c', 'D': 'Ñ', 'p': 'z', 'J': ']', '8': 'N', 'k': 'x', 'F': 'r', 'h': 'X', 'j': '!', '1': 'v', '?': ' ', 'L': 'J', '6': 'm', 'r': 'ñ', '>': 'G', 'i': '8', 'Q': 's', 'K': 'w', '7': 'o', ',': ';', 'S': 'k', '¡': 'U', ':': 'M', '4': 'F', 'V': 'K', '_': 'h', '/': 'S', 'n': 'A', 'f': '/', '+': 'q', 'N': 'R', '[': 'Y', 'q': 'y', ' ': '-', '-': '+', 't': '9', 'Y': 'i', '<': '3', 'v': 'd', '2': '4', '3': 'n', 'O': 'T', ']': 'C', '!': 'P', '': ''}


def co_decode(script, level, code):
    """ code or decode file character by character acording to "code" variable value """
    content = ""
    pb_title = 'Coding' if code else 'Decoding'
    for _ in range(int(level)):
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

def code_binary(readed_file, level, filepath):
    """ code binary file getting base64 encoding """
    with open(filepath.split('.')[0] + '.txt','wb') as out:
        b64_encode = base64.b64encode(readed_file)
        coded = co_decode(b64_encode.decode(), level=level, code=True)
        out.write(coded.encode())
        extension = filepath.split(".")[len(filepath.split("."))-1]
        coded_extension = co_decode(extension, level=level, code=True)
        out.write(("."+coded_extension).encode())
        out.close()

def decode_binary(readed_file, level, filepath):
    """ decode binary file reading base64 enconding from txt file """
    output_extension = readed_file.split(".")[1]
    decoded_output_ext = co_decode(output_extension, level=level, code=False)
    output_filename = filepath.split(".")[0] + '.' + decoded_output_ext
    with open(output_filename, 'wb') as out:
        if len(str(readed_file).split(".")) > 1:
            readed_file = str(readed_file).split(".", maxsplit=1)[0]
        decoded = co_decode(readed_file, level=level, code=False)
        out.write(base64.b64decode(decoded.encode()))
        out.close()

def get_filename(filepath, yesno):
    """return filename determining if file was coded or decoded"""
    ext = "."+filepath.split(".")[len(filepath.split("."))-1]
    end = "-coded" if yesno else "-decoded"
    return filepath.split(".")[0] + end + ext


parent = tkinter.Tk() # Create the object
parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
parent.withdraw() # Hide the window as we do not want to see this one

file_types = [('All files', '*')]

# Ask the user to select a one or more file names.
file_names = filedialog.askopenfilenames(title='Select one or more files',
                                        filetypes=file_types, parent=parent)

if len(file_names) > 0:
    YESNO = messagebox.askyesno(None, "Code (YES) or Decode (NO)?", icon ='question')
    for each in file_names:
        filename = get_filename(each, YESNO)
        if YESNO:
            with open(each, 'rb') as file:
                file_read = file.read()
                code_binary(readed_file=file_read, level=1, filepath=filename)
        else:
            with open(each, 'r', encoding='utf8') as file:
                file_read = file.read()
                decode_binary(readed_file=file_read, level=1, filepath=filename)
