""" files encoder/decoder """

import tkinter
from tkinter import filedialog, messagebox
from threading import Thread
from dynamic_cipher import Cipher as dynamic_cipher
from static_cipher import Cipher as static_cipher

def get_filename(filepath, yesno):
    """return filename determining if file was coded or decoded"""
    ext = "."+filepath.split(".")[len(filepath.split("."))-1]
    end = "-coded" if yesno else "-decoded"
    return filepath.split(".")[0] + end + ext

def read_and_code(cipher_instance, binary, path):
    """ read binary and call cipher instance code function """
    file_read = binary.read()
    cipher_instance.code_binary(readed_file=file_read, level=1, filepath=path)

def read_and_decode(cipher_instance, plain, path):
    """ read binary and call cipher instance decode function """
    file_read = plain.read()
    cipher_instance.decode_binary(readed_file=file_read, level=1, filepath=path)


parent = tkinter.Tk() # Create the object
parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
parent.withdraw() # Hide the window as we do not want to see this one

file_types = [('All files', '*')]

# Ask the user to select a one or more file names.
file_names = filedialog.askopenfilenames(title='Select one or more files',
                                        filetypes=file_types, parent=parent)


########  Main  ########

if __name__ == "__main__":
    if len(file_names) > 0:
        YESNO = messagebox.askyesno(None, "Code (YES) or Decode (NO)?", icon ='question')
        DYNAMIC = messagebox.askyesno(None, "Dynamic (YES) or Static (NO)?", icon ='question')
        cipher = dynamic_cipher() if DYNAMIC else static_cipher()
        for each in file_names:
            filename = get_filename(each, YESNO)
            if YESNO:
                with open(each, 'rb') as file:
                    thread = Thread(target = read_and_code, args = (cipher, file, filename, ))
                    thread.start()
            else:
                with open(each, 'r', encoding='utf8') as file:
                    thread = Thread(target = read_and_decode, args = (cipher, file, filename, ))
                    thread.start()
