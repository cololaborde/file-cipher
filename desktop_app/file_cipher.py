""" files encoder/decoder """

import tkinter
from tkinter import filedialog, messagebox
from threading import Thread
from dynamic_cipher import Cipher as dynamic_cipher
from static_cipher import Cipher as static_cipher

def get_filename(filepath, yesno):
    """return filename determining if file was coded or decoded"""
    end = "-coded" if yesno else "-decoded"
    base_path = '/'.join(filepath.split('/')[:len(filepath.split('/'))-1])
    file_name = filepath.split('/')[len(filepath.split('/')) -1]
    output_filename = base_path + '/' + '.'.join(file_name.split('.')[:len(file_name.split('.'))-1])
    extension = file_name.split(".")[len(file_name.split("."))-1]
    return output_filename + end, extension


def read_and_code(cipher_instance, binary, path, extension):
    """ read binary and call cipher instance code function """
    file_read = binary.read()
    writables_list = cipher_instance.code_binary(readed_file=file_read, extension=extension)
    output_filename = path + '.txt'
    with open(output_filename, 'wb') as out:
        for w in writables_list:
            out.write(w)
        #out.write(coded_file.encode())
        #out.write(("."+coded_extension).encode())
        out.close()


def read_and_decode(cipher_instance, plain, path):
    """ read binary and call cipher instance decode function """
    file_read = plain.read()
    decoded_file, decoded_extension = cipher_instance.decode_binary(readed_file=file_read)
    output_filename = path + '.' + decoded_extension
    with open(output_filename, 'wb') as out:
        out.write(decoded_file)
        out.close()


def run_file_dialog():
    parent = tkinter.Tk() # Create the object
    parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
    parent.withdraw() # Hide the window as we do not want to see this one

    file_types = [('All files', '*')]

    # Ask the user to select a one or more file names.
    return filedialog.askopenfilenames(title='Select one or more files',
                                        filetypes=file_types, parent=parent)


########  Main  ########

if __name__ == "__main__":
    file_names = run_file_dialog()
    if len(file_names) > 0:
        YESNO = messagebox.askyesno(None, "Code (YES) or Decode (NO)?", icon ='question')
        DYNAMIC = messagebox.askyesno(None, "Dynamic (YES) or Static (NO)?", icon ='question')
        cipher = dynamic_cipher() if DYNAMIC else static_cipher()
        for each in file_names:
            filename, ext = get_filename(each, YESNO)
            if YESNO:
                with open(each, 'rb') as file:
                    thread = Thread(target = read_and_code, args = (cipher, file, filename, ext, ))
                    thread.start()
            else:
                with open(each, 'r', encoding='utf8') as file:
                    thread = Thread(target = read_and_decode, args = (cipher, file, filename, ))
                    thread.start()
