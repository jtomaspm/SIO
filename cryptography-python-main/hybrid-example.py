from assymmetric import generate as generateAssy
from assymmetric import encrypt as encryptAssy
from assymmetric import decrypt as decryptAssy
from symetric import encrypt as encryptSym
from symetric import decrypt as decryptSym
from symetric import generate_sym_key_to_file
from symetric import init_sym
'''
    Two ciphers, a symmetric to encrypt the file with a random key
    assymetric to encrypt the key
        '''
def main():
    generate_sym_key_to_file('symkey-notE',32)  
    generateAssy('publicK','privateK')
    encryptAssy('symkey-notE','KEY_ENCRYPTED',1) # 1 for binary mode
    decryptAssy('KEY_ENCRYPTED','KEY_DECRYPTED')
    cipher=init_sym('KEY_DECRYPTED')
    encryptSym('textToEncrypt',cipher,'TEXT-ENCRYPTED')
    decryptSym('TEXT-ENCRYPTED',cipher,'TEXT-DECRYPTED')
    return

if __name__ == "__main__":
    main()

