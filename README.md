<h1 align="center">
  file-cipher
</h1>
<br/>
<h3 align="center">
  Python file cipher implementation
</h3>

## Description

The program performs a binary read of each set file to convert it to base64 format. Once the encoding is obtained, each character is consistently replaced based on a previously generated "key". The key can be obtained from [keygen.py](desktop_app/utils/keygen.py). The result is dumped into a copy of the original file, indicating the applied operation in the name.

<br/>

## Use modes

### - Static

   Using the static key (mod_static.txt) if 2 files are encoded, both will be encode with the same key.

### - Dynamic

  Dynamic mode chooses randomly 1 among N keys from dynamic key (mod_dyn.txt) for each uploaded file.

<br/>

## Usage - [file_cipher.py](desktop_app/file_cipher.py)


### File(s)

  One or more files must be selected to be encoded or decoded, also indicating the encryption mode and finally the previously generated key must be selected.

```bash
#python3
python file_cipher.py
```


### Directory

  One directory must be selected to encode or decode the files in it, also indicating the encryption mode and finally the previously generated key must be selected.

```bash
#python3
python file_cipher -d
```


### Directory recursively

  Same as previous mode, but it recursively goes through the directories inside.

```bash
#python3
python file_cipher -d -r
```


### Keep only generated encode

  The --remove-originals parameter indicates that encoded files are subsequently removed, leaving only the generated encode.

```bash
#python3
python file_cipher --remove-originals
python file_cipher -d --remove-originals
python file_cipher -d -r --remove-originals
```

<br/>

## Usage - [keygen.py](desktop_app/utils/keygen.py)

   A key can be generated to encode statically and dynamically.

### Static key: 
```bash
#python3
python keygen.py -s  # →  mod_static.txt
```

### Dynamic key: 
```bash
#python3
python keygen.py -d N  # →  mod_dyn.txt
```
being N the number of keys to create.
