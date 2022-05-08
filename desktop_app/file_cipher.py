""" files encoder/decoder """

from tkinter import filedialog, messagebox, Tk
from threading import Thread
from cipher import StaticCipher, DynamicCipher


def get_filename(filepath, yesno):
    """return filename determining if file was coded or decoded"""

    end = "-coded" if yesno else "-decoded"
    base_path = '/'.join(filepath.split('/')[:len(filepath.split('/'))-1])
    file_name = filepath.split('/')[len(filepath.split('/')) - 1]
    output_filename = base_path + '/' + \
        '.'.join(file_name.split('.')[:len(file_name.split('.'))-1])
    extension = file_name.split(".")[len(file_name.split("."))-1]
    return output_filename + end, extension


def read_and_code(cipher_instance, binary, path, extension, keypath):
    """ read binary and call cipher instance code function """

    file_read = binary.read()
    writables_list = cipher_instance.code_binary(readed_file=file_read,
                                                 extension=extension, key_path=keypath)
    output_filename = path + '.txt'
    with open(output_filename, 'wb') as out:
        for to_write in writables_list:
            out.write(to_write)
        out.close()


def read_and_decode(cipher_instance, plain, path, keypath):
    """ read binary and call cipher instance decode function """

    file_read = plain.read()
    decoded_file, decoded_extension = cipher_instance\
        .decode_binary(readed_file=file_read, key_path=keypath)
    output_filename = path + '.' + decoded_extension
    with open(output_filename, 'wb') as out:
        out.write(decoded_file)
        out.close()


def run_file_dialog(file_types, multiple):
    """ create tkinter dialog to select files """

    parent = Tk()  # Create the object
    # Avoid it appearing and then disappearing quickly
    parent.overrideredirect(1)
    parent.withdraw()  # Hide the window as we do not want to see this one

    return filedialog \
        .askopenfilenames(title='Select one or more files',
                          filetypes=file_types, parent=parent) if multiple else \
        filedialog.askopenfilename(title='Select key file',
                                   filetypes=file_types, parent=parent)


def create_upload_boxes():
    """ create upload dialog boxes """

    co_decode = messagebox.askyesno(
        None, "Code (YES) or Decode (NO)?", icon='question')
    dyn = messagebox.askyesno(
        None, "Dynamic (YES) or Static (NO)?", icon='question')
    keypath = run_file_dialog([('text files', '.txt')], False)
    return dyn, keypath, co_decode

########  Main  ########


if __name__ == "__main__":
    file_names = run_file_dialog([('All files', '*')], True)
    if len(file_names) > 0:
        DYNAMIC, key_path, YESNO = create_upload_boxes()
        cipher = DynamicCipher() if DYNAMIC else StaticCipher(key_path)
        for each in file_names:
            filename, ext = get_filename(each, YESNO)
            if YESNO:
                with open(each, 'rb') as file:
                    # temporary fix to threading problem in dynamic mode
                    if len(file_names) > 1 and DYNAMIC:
                        read_and_code(cipher, file, filename, ext, key_path)
                    else:
                        thread = Thread(target=read_and_code, args=(
                            cipher, file, filename, ext, key_path, ))
                        thread.start()
            else:
                with open(each, 'r', encoding='utf8') as file:
                    # temporary fix to threading problem in dynamic mode
                    if len(file_names) > 1 and DYNAMIC:
                        read_and_decode(cipher, file, filename, key_path)
                    else:
                        thread = Thread(target=read_and_decode, args=(
                            cipher, file, filename, key_path, ))
                        thread.start()
