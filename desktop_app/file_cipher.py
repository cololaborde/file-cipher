""" files encoder/decoder """

from tkinter import filedialog, messagebox, Tk
from threading import Thread
from cipher import StaticCipher, DynamicCipher

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
        for to_write in writables_list:
            out.write(to_write)
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

    """ create tkinter dialog to select files """

    parent = Tk() # Create the object
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
        cipher = DynamicCipher() if DYNAMIC else StaticCipher()
        for each in file_names:
            filename, ext = get_filename(each, YESNO)
            if YESNO:
                with open(each, 'rb') as file:
                    #read_and_code(cipher, file, filename, ext)
                    thread = Thread(target = read_and_code, args = (cipher, file, filename, ext, ))
                    thread.start()
            else:
                with open(each, 'r', encoding='utf8') as file:
                    #read_and_decode(cipher, file, filename)
                    thread = Thread(target = read_and_decode, args = (cipher, file, filename, ))
                    thread.start()
