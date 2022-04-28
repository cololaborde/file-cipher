""" files in a directory encoder/decoder, removing the originals """

import tkinter
from tkinter import filedialog, messagebox
import os
from static_cipher import Cipher as static_cipher
from dynamic_cipher import Cipher as dynamic_cipher


def get_filename(file_path):
    """return filename and extension """
    base_path = '/'.join(file_path.split('/')[:len(file_path.split('/'))-1])
    file_name = file_path.split('/')[len(file_path.split('/')) -1]
    output_filename = base_path + '/' + '.'.join(file_name.split('.')[:len(file_name.split('.'))-1])
    extension = file_name.split(".")[len(file_name.split("."))-1]
    return output_filename, extension


def read_and_code(binary, cipher_instance, file_name, extension):
    """ read binary and call cipher instance code function """
    file_read = binary.read()
    writables_list = cipher_instance.code_binary(readed_file=file_read, extension=extension)
    output_filename = file_name + '.txt'
    with open(output_filename, 'wb') as out:
        for to_write in writables_list:
            out.write(to_write)
        out.close()


def read_and_decode(plain, cipher_instance, file_path):
    """ read binary and call cipher instance decode function """
    file_read = plain.read()
    decoded_file, decoded_extension = cipher_instance.decode_binary(readed_file=file_read)
    output_filename = file_path + '.' + decoded_extension
    with open(output_filename, 'wb') as out:
        out.write(decoded_file)
        out.close()


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
                filepath = os.path.join(root, file)
                filename, ext = get_filename(filepath)
                if YESNO:
                    with open(filepath, 'rb') as file:
                        read_and_code(file, cipher, filename, ext)
                else:
                    with open(filepath, 'r', encoding='utf8') as file:
                        read_and_decode(file, cipher, filename)
                os.remove(filepath)
