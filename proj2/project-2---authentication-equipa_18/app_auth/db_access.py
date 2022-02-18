from cryptography.fernet import Fernet
import os

def generate_key(key_file):
    key =  Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)

def load_key(key_file):
    with open(key_file, 'rb') as f:
        key = f.read()

    return Fernet(key)

def encrypt_db(enc_file, key_file, db_file):
    generate_key(key_file)
    f = load_key(key_file)
    
    with open(db_file, 'rb') as original_file:
        original = original_file.read()
        
    encrypted = f.encrypt(original)

    with open(enc_file, 'wb') as enc_file:
        enc_file.write(encrypted)

    if os.path.exists(db_file):
        os.remove(db_file)

    
def decrypt_db(enc_file, key_file, db_file):

    f = load_key(key_file)
    
    with open(enc_file, 'rb') as original_file:
        original = original_file.read()
        
    decrypted = f.decrypt(original)

    with open(db_file, 'wb') as res:
        res.write(decrypted)
    
    if os.path.exists(key_file):
        os.remove(key_file)

    if os.path.exists(enc_file):
        os.remove(enc_file)