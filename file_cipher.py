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

def co_decode_binary(binary, code, filename):
    """ code or decode binary file getting base64 encoding """
    with open(filename,'wb') as f2:
       while True:
            buf=binary.read(1024)
            if buf:
                b64_encode = base64.b64encode(buf)
                coded = co_decode(b64_encode.decode(), level=1, code=code)
                decoded = co_decode(coded, level=1, code=False)
                print(len(str(coded.encode())))
                print(len(coded.encode()))
                print(len(str(coded.encode())) == len(coded.encode()))
                if len(coded.encode())%4 != 0:
                    new_coded = fix_characters_number(coded)
                    print(coded.encode())
                    print(new_coded)
                    f2.write(base64.b64decode(new_coded))
                else:
                    f2.write(base64.b64decode(coded.encode()))
            else:
                f2.close()
                break

def fix_characters_number(coded):
    
    def remove_extras(new_coded):
        return new_coded[2:len(new_coded)][:-1]

    founded = False
    new_coded = coded
    while not founded:
        for _ in range(3):
            new_coded = str(new_coded.encode())[:-1] + "='"
            if len(new_coded) %4 == 0:
                founded = True
                return new_coded
        new_coded = coded
        for i in range(3):
            new_coded = str(new_coded.encode())[:-(i+2)] + "'"
            if len(new_coded) %4 == 0:
                founded = True
                return new_coded
    return new_coded

def get_filename(each, yesno):
    ext = "."+each.split(".")[len(each.split("."))-1]
    END = "-coded" if yesno else "-decoded"
    return each.split(".")[0] + END + ext

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
        with open(each, 'rb') as file:
            
            filename = get_filename(each, yesno)
            if is_binary(file.read(1024)):
                file.close()
                with open(each, 'rb') as file:
                    binary = True
                    result = co_decode_binary(file, code=yesno, filename=filename)
            else:
                binary = False
                with open(each, 'r', encoding='utf8') as file:
                    result = co_decode(file, level=1, code=yesno) 

        if not binary:
            with open(filename, 'w', encoding='utf8') as file_encoded:
                file_encoded.write(result)
                file_encoded.close()