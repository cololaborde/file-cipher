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

## Usage

###### python file_cipher.py

Starts the GUI to select file or files to encrypt or decrypt, you must also indicate whether the encryption mode is static or dynamic and finally a box will open to indicate the previously generated key

###### python file_cipher -d

Starts the GUI to select a directory to encrypt or decrypt the files contained therein, you must also indicate whether the encryption mode is static or dynamic and finally a box will open to indicate the key generated previously

###### python file_cipher -d -r

Same as the previous mode, but it recursively goes through the directories that may exist within the indicated root directory

###### python file_cipher --remove-originals
###### python file_cipher -d --remove-originals
###### python file_cipher -d -r --remove-originals

The --remove-originals parameter indicates that the encrypted files are subsequently removed, leaving only the generated encryption.
