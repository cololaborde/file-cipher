""" coder and decoder file """

import tkinter
from tkinter import filedialog, messagebox
import base64
import re

base = {'+':'<','/':'/',',':'!','.':'?',
        ' ':' ','a':'x','b':'y','c':'z',
        'd':'a','e':'b','f':'c','g':'d',
        'h':'e','i':'f','j':'g','k':'h',
        'l':'i','m':'j','n':'k','ñ':'l',
        'o':'m','p':'n','q':'ñ','r':'o',
        's':'p','t':'q','u':'r','v':'s',
        'w':'t','x':'u','y':'v','z':'w',
        'A':'X','B':'Y','C':'Z','D':'A',
        'E':'B','F':'C','G':'D','H':'E',
        'I':'F','J':'G','K':'H','L':'I',
        'M':'J','N':'K','Ñ':'L','O':'M',
        'P':'N','Q':'Ñ','R':'O','S':'P',
        'T':'Q','U':'R','V':'S','W':'T',
        'X':'U','Y':'V','Z':'W','0':'3',
        '1':'4','2':'5','3':'6','4':'7',
        '5':'8','6':'9','7':'0','8':'1',
        '9':'2','?':'.','!':',','':'','=':'='}

yxpb = {'<':'+','/':'/','!':',','?':'.',
        ' ':' ','x':'a','y':'b','z':'c',
        'a':'d','b':'e','c':'f','d':'g',
        'e':'h','f':'i','g':'j','h':'k',
        'i':'l','j':'m','k':'n','l':'ñ',
        'm':'o','n':'p','ñ':'q','o':'r',
        'p':'s','q':'t','r':'u','s':'v',
        't':'w','u':'x','v':'y','w':'z',
        'X':'A','Y':'B','Z':'C','A':'D',
        'B':'E','C':'F','D':'G','E':'H',
        'F':'I','G':'J','H':'K','I':'L',
        'J':'M','K':'N','L':'Ñ','M':'O',
        'N':'P','Ñ':'Q','O':'R','P':'S',
        'Q':'T','R':'U','S':'V','T':'W',
        'U':'X','V':'Y','W':'Z','3':'0',
        '4':'1','5':'2','6':'3','7':'4',
        '8':'5','9':'6','0':'7','1':'8',
        '2':'9','.':'?',',':'!','':'','=':'='}

def co_decode(script, level, code):
    """ code or decode file character by character acording to "code" variable value """
    content = ""
    for _ in range(int(level)):
        for line in script:
            for character in line:
                try:
                    if code:
                        content = content + base[character]
                    else:
                        content = content + yxpb[character]
                except KeyError:
                    content = content + character
                    print(character)
            line = content
    return content

def code_binary(binary, code, filename):
    """ code or decode binary file getting base64 encoding """
    with open(filename.split('.')[0]+'.txt','wb') as f2:
       coded = ""
       while True:
            buf=binary.read()
            if buf:
                b64_encode = base64.b64encode(buf)
                coded = coded + co_decode(b64_encode.decode(), level=1, code=code)
                decoded = co_decode(coded, level=1, code=False)
            else:
                f2.write(coded.encode())
                f2.write(("."+filename.split(".")[len(filename.split("."))-1]).encode())
                f2.close()
                break

def decode_binary(each, file_read, level, code, filename):
    with open(each, 'r') as file:
        output_extension = file_read.split(".")[1]
        output_filename = filename.split(".")[0] + '.'+output_extension
        with open(output_filename, 'wb') as out:
            decoded = ""
            while True:
                 buf=file.read()
                 if buf:
                    if len(str(buf).split(".")) > 1:
                        buf = str(buf).split(".")[0]
                    decoded = decoded + co_decode(buf, level=1, code=False)
                 else:
                    out.write(base64.b64decode(decoded.encode()))
                    out.close()
                    break

def get_filename(each, yesno):
    ext = "."+each.split(".")[len(each.split("."))-1]
    END = "-coded" if yesno else "-decoded"
    return each.split(".")[0] + END + ext

def write_not_binary(filename, result):
    with open(filename, 'w', encoding='utf8') as file_encoded:
        file_encoded.write(result)
        file_encoded.close()

parent = tkinter.Tk() # Create the object
parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
parent.withdraw() # Hide the window as we do not want to see this one

file_types = [('All files', '*')]

# Ask the user to select a one or more file names.
file_names = filedialog.askopenfilenames(title='Select one or more files',
                                        filetypes=file_types, parent=parent)

textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary = lambda bytes: bool(bytes.translate(None, textchars))

if len(file_names) > 0:
    yesno = messagebox.askyesno('What do you want to do?',
                                'Press YES to CODE and NO to DECODE', parent=parent)
    binary = False    
    for each in file_names:
        filename = get_filename(each, yesno)
        if yesno:
            with open(each, 'rb') as file:
                if is_binary(file.read(1024)):
                    file.close()
                    with open(each, 'rb') as file:
                        binary = True
                        result = code_binary(file, code=True, filename=filename)
                else:
                    binary = False
                    with open(each, 'r', encoding='utf8') as file:
                        result = co_decode(file, level=1, code=True) 
            if not binary:
                write_not_binary(filename, result)
        else:
            with open(each, 'r', encoding='utf8') as file:
                file_read = file.read()
                if len(str(file_read).split('.')) == 0:
                    result = co_decode(file, level=1, code=False)
                    write_not_binary(filename, result)
                else:
                    decode_binary(each, file_read=file_read, level=1, code=False, filename=filename)