""" coder and decoder file """

import tkinter
from tkinter import filedialog, messagebox

base = {',':'!','.':'?','?':'.','!':',',
        ' ':'¿','a':'x','b':'y','c':'z',
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
        '9':'2'}

yxpb = {'!':',','?':'.','.':'?',',':'!',
        '¿':' ','x':'a','y':'b','z':'c',
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
        '2':'9'}

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


parent = tkinter.Tk() # Create the object
parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
parent.withdraw() # Hide the window as we do not want to see this one

file_types = [('All files', '*')]

# Ask the user to select a one or more file names.
file_names = filedialog.askopenfilenames(title='Select one or more files',
                                        filetypes=file_types, parent=parent)

if len(file_names) > 0:
    yesno = messagebox.askyesno('What do you want to do?',
                                'Press yes to code and no to decode', parent=parent)


    for each in file_names:
        with open(each, 'r', encoding='utf8') as file:
            result = co_decode(file, level=5, code=yesno)
        ext = "."+each.split(".")[len(each.split("."))-1]
        END = "-coded" if yesno else "-decoded"
        filename = each.split(".")[0] + END + ext
        with open(filename, 'w', encoding='utf8') as file_encoded:
            file_encoded.write(result)
