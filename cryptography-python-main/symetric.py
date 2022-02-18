from assymmetric import readChunks
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import sys

def encrypt(path,cipher,outE):
    
    encryptor = cipher.encryptor()
    f=open(path+'.txt')
    for chunks in readChunks(f,1000000000): # ~1gb max
        ct = encryptor.update(chunks.encode())
        with open (outE+'.txt','wb+') as ff:
            ff.write(ct)
    encryptor.finalize()

def decrypt(path,cipher,outD):
    decryptor = cipher.decryptor()
    f=open(path+'.txt','rb')
    for chunks in readChunks(f,1000000000): # ~1gb max 
        ct = decryptor.update(chunks)
        with open (outD+'.txt','wb+') as ff:
            ff.write(ct)   
    decryptor.finalize()

def init_sym(path='DEFAULT',size=32):
    nonce = os.urandom(16)
    if path == 'DEFAULT': ## we generating key not reading it from a file
        key = os.urandom(size)
        print('DEFAULT')
    else:       ##we reading from file 
        print('NOT DEFAULT')
        key=''
        with open(path+'.txt', 'rb') as f:
            for chunks in readChunks(f,size):
             ## works because we getting only one chunk
                key=chunks
 
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None)
    return cipher

def generate_sym_key_to_file(path,size): # go with 32 
    key = os.urandom(size)
    with open(path+'.txt', 'wb+') as f:
        f.write(key)

    return

