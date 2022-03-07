""" files in a directory encoder/decoder, removing the originals """

import tkinter
from tkinter import filedialog, messagebox
import os
from cipher import Cipher

cipher = Cipher()

parent = tkinter.Tk() # Create the object
parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
parent.withdraw() # Hide the window as we do not want to see this one

# Ask the user to select a one or more file names.
directory = filedialog.askdirectory(title='Select directory', parent=parent)

if os.path.isdir(directory):
    YESNO = messagebox.askyesno(None, "Code (YES) or Decode (NO)?", icon ='question')
    for root, subdirectories, files in os.walk(directory):
        for file in files:
            filename = os.path.join(root, file)
            if YESNO:
                with open(filename, 'rb') as file:
                    file_read = file.read()
                    cipher.code_binary(readed_file=file_read, level=1, filepath=filename)
            else:
                with open(filename, 'r', encoding='utf8') as file:
                    file_read = file.read()
                    cipher.decode_binary(readed_file=file_read, level=1, filepath=filename)
            os.remove(filename)
