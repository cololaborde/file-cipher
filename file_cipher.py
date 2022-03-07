""" files encoder/decoder """

import tkinter
from tkinter import filedialog, messagebox
from cipher import Cipher

def get_filename(filepath, yesno):
    """return filename determining if file was coded or decoded"""
    ext = "."+filepath.split(".")[len(filepath.split("."))-1]
    end = "-coded" if yesno else "-decoded"
    return filepath.split(".")[0] + end + ext

cipher = Cipher()

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
                cipher.code_binary(readed_file=file_read, level=1, filepath=filename)
        else:
            with open(each, 'r', encoding='utf8') as file:
                file_read = file.read()
                cipher.decode_binary(readed_file=file_read, level=1, filepath=filename)
