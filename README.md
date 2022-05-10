<h1 align="center">
  file-cipher
</h1>
<br/>
<h3 align="center">
  Python file cipher implementation
</h3>

## Description

The program performs a binary read of each set file to convert it to base64 format. Once the encoding is obtained, each character is consistently replaced based on a previously generated "key". The key can be obtained from /utils/keygen.py. The result is dumped into a copy of the original file, indicating the applied operation in the name.

<br/>

## Use modes
The program has two modes of use, one static, that is, using the "static encryption key" (mod_static.txt) if 2 files are encrypted, both will be encrypted with the same key.
Dynamic mode chooses randomly 1 among N keys from "dynamic encryption key"(mod_dyn.txt) file  for each file

<br/>

## Usage - file_cipher.py

#### python file_cipher.py

Starts the GUI to select file(s) to encrypt or decrypt, you must also indicate whether the encryption mode is static or dynamic and finally a box will open to indicate the previously generated key

#### python file_cipher -d

Starts the GUI to select a directory to encrypt or decrypt the files contained therein, you must also indicate whether the encryption mode is static or dynamic and finally a box will open to indicate the key generated previously

##### python file_cipher -d -r

Same as the previous mode, but it recursively goes through the directories that may exist within the indicated root directory

#### python file_cipher --remove-originals
#### python file_cipher -d --remove-originals
#### python file_cipher -d -r --remove-originals

The --remove-originals parameter indicates that the encrypted files are subsequently removed, leaving only the generated encryption.

<br/>

## Usage - keygen.py

There are two possible keys to generate. One to use in static mode and one to use in dynamic mode.

To indicate it to generate a static use key, just run:
#### python keygen.py -s   -->  mod_static.txt

and to generate a dynamic use key: 
#### python keygen.py -d N   -->  mod_dyn.txt
being N the number of keys to generate
