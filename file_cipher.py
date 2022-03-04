""" coder and decoder file """

import tkinter
from tkinter import filedialog, messagebox
import base64

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
            line = content
    return content

def code_binary(binary, level, filename):
    """ code binary file getting base64 encoding """
    with open(filename.split('.')[0]+'.txt','wb') as out:
        coded = ""
        while True:
            buf=binary.read()
            if buf:
                b64_encode = base64.b64encode(buf)
                coded = coded + co_decode(b64_encode.decode(), level=level, code=True)
            else:
                out.write(coded.encode())
                out.write(("."+filename.split(".")[len(filename.split("."))-1]).encode())
                out.close()
                break

def decode_binary(each, file_read, level, filename):
    """ decode binary file reading enconding from txt file """
    with open(each, 'r', encoding='utf-8') as file:
        output_extension = file_read.split(".")[1]
        output_filename = filename.split(".")[0] + '.'+output_extension
        with open(output_filename, 'wb') as out:
            decoded = ""
            while True:
                buf=file.read()
                print(buf == file_read)
                if buf:
                    if len(str(buf).split(".")) > 1:
                        buf = str(file_read).split(".", maxsplit=1)[0]
                    decoded = decoded + co_decode(buf, level=level, code=False)
                else:
                    out.write(base64.b64decode(decoded.encode()))
                    out.close()
                    break

def get_filename(each, yesno):
    """return filename determining if file was coded or decoded"""
    ext = "."+each.split(".")[len(each.split("."))-1]
    end = "-coded" if yesno else "-decoded"
    return each.split(".")[0] + end + ext


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
                code_binary(file, level=1, filename=filename)
        else:
            with open(each, 'r', encoding='utf8') as file:
                file_read = file.read()
                decode_binary(each, file_read=file_read, level=1, filename=filename)