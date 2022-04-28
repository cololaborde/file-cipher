""" files in a directory encoder/decoder, removing the originals """

import tkinter
from tkinter import filedialog, messagebox
import os
from static_cipher import Cipher as static_cipher
from dynamic_cipher import Cipher as dynamic_cipher


def run_file_dialog():
    """ create tkinter dialog to select directory """
    parent = tkinter.Tk() # Create the object
    parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
    parent.withdraw() # Hide the window as we do not want to see this one

    return filedialog.askdirectory(title='Select directory', parent=parent)


########  Main  ########

if __name__ == "__main__":
    directory = run_file_dialog()
    if os.path.isdir(directory):
        YESNO = messagebox.askyesno(None, "Code (YES) or Decode (NO)?", icon ='question')
        DYNAMIC = messagebox.askyesno(None, "Dynamic (YES) or Static (NO)?", icon ='question')
        cipher = dynamic_cipher() if DYNAMIC else static_cipher()
        for root, subdirectories, files in os.walk(directory):
            for file in files:
                filename = os.path.join(root, file)
                if YESNO:
                    with open(filename, 'rb') as file:
                        file_read = file.read()
                        cipher.code_binary(readed_file=file_read)
                else:
                    with open(filename, 'r', encoding='utf8') as file:
                        file_read = file.read()
                        cipher.decode_binary(readed_file=file_read)
                os.remove(filename)
