""" files encoder/decoder """

from os.path import isfile, join
from os import remove, listdir, walk
from sys import argv, exit as sys_exit
from tkinter import filedialog, messagebox, Tk
from cipher import StaticCipher, DynamicCipher


def get_params():
    """ get params """

    is_dir, recursive, remove_after = False, False, False
    if '-d' in argv:
        is_dir = True
    if '-r' in argv:
        recursive = True
    if '--remove-originals' in argv:
        remove_after = True
    return is_dir, recursive, remove_after


def get_filename(filepath, yesno):
    """return filename determining if file was coded or decoded"""

    end = "-coded" if yesno else "-decoded"
    base_path = '/'.join(filepath.split('/')[:len(filepath.split('/'))-1])
    file_name = filepath.split('/')[len(filepath.split('/')) - 1]
    extension = file_name.split(".")[len(file_name.split("."))-1]

    splited = file_name.split('-decoded.'+extension) if yesno \
         else file_name.split('-coded.'+extension)

    if len(splited) > 1:
        output_filename = base_path + '/' + '.'.join(splited[0].split('.'))
    else:
        output_filename = base_path + '/' + \
            '.'.join(splited[0].split('.')[:len(splited[0].split('.'))-1])
    return output_filename + end, extension


def read_and_code(instance, binary, path, extension, keypath):
    """ read binary and call cipher instance code function """

    file_read = binary.read()
    writables_list = instance.code_binary(readed_file=file_read,
                                          extension=extension, key_path=keypath)
    if not writables_list:
        return False
    output_filename = path + '.txt'
    with open(output_filename, 'wb') as out:
        for to_write in writables_list:
            out.write(to_write)
        out.close()
    return True


def read_and_decode(instance, plain, path, keypath):
    """ read binary and call cipher instance decode function """

    try:
        file_read = plain.read()
    except UnicodeDecodeError:
        return False
    decoded_file, decoded_extension = instance\
        .decode_binary(readed_file=file_read, key_path=keypath)
    if not decoded_file or not decoded_extension:
        return False
    output_filename = path + '.' + decoded_extension
    with open(output_filename, 'wb') as out:
        out.write(decoded_file)
        out.close()
    return True


def run_file_dialog(file_types=('All files', '*'), multiple=False, open_dir=False):
    """ create tkinter dialog to select files """

    parent = Tk()  # Create the object
    # Avoid it appearing and then disappearing quickly
    parent.overrideredirect(1)
    parent.withdraw()  # Hide the window as we do not want to see this one

    if open_dir:
        return filedialog.askdirectory(title='Select directory', parent=parent)
    return filedialog \
        .askopenfilenames(title='Select one or more files',
                          filetypes=[file_types], parent=parent) if multiple else \
        filedialog.askopenfilename(title='Select key file',
                                   filetypes=[file_types], parent=parent)


def create_dialog_boxes():
    """ create upload dialog boxes """

    co_decode = messagebox.askyesno(
        None, "Code (YES) or Decode (NO)?", icon='question')
    dyn = messagebox.askyesno(
        None, "Dynamic (YES) or Static (NO)?", icon='question')
    keypath = run_file_dialog(('text files', '.txt'), False)
    return dyn, keypath, co_decode


def process_file(file_names, code, cipher, pathkey, delete):
    """ process files to code or encode """

    for each in file_names:
        if isfile(each):
            filename, ext = get_filename(each, code)
            if code:
                with open(each, 'rb') as file:
                    was_processed = read_and_code(
                        cipher, file, filename, ext, pathkey)
            else:
                with open(each, 'r', encoding='utf8') as file:
                    was_processed = read_and_decode(
                        cipher, file, filename, pathkey)
            if delete and was_processed:
                remove(each)


########  Main  ########
if __name__ == "__main__":

    DIR, RECURSIVE, REMOVE = get_params()

    locate = run_file_dialog(multiple=True) if not DIR \
        else run_file_dialog(file_types=None, multiple=False, open_dir=True)

    if not locate:
        sys_exit()

    DYNAMIC, key_path, YESNO = create_dialog_boxes()

    if not key_path:
        sys_exit()

    cipher_instance = DynamicCipher() if DYNAMIC else StaticCipher(key_path)

    if DIR:
        if RECURSIVE:
            for root, subdirectories, files in walk(locate):
                files = [join(root, file) for file in files]
                process_file(file_names=files, code=YESNO,
                             cipher=cipher_instance, pathkey=key_path, delete=REMOVE)
        else:
            files = listdir(locate)
            files = [join(locate, file) for file in files]
            process_file(file_names=files, code=YESNO,
                         cipher=cipher_instance, pathkey=key_path, delete=REMOVE)
    else:
        process_file(file_names=locate, code=YESNO,
                     cipher=cipher_instance, pathkey=key_path, delete=REMOVE)
