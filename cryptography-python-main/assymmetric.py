import os 
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
import base64
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def generate(namePublic,namePrivate):
    pv = rsa.generate_private_key(
                public_exponent=65537,
                    key_size=2048,
                    )
    private_pem =pv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )
    public_pem = pv.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
           )
    privaten=namePrivate+ ".pem"
    with open(privaten, 'wb+') as f:
        f.write(private_pem)
    publicn=namePublic+".pem"
    with open(publicn, 'wb+') as f:
        f.write(public_pem)
   
def encrypt(name,outE,bin=0):

    ### load key
    with open("publicK.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                   key_file.read(),
                  )
    ########################


    if bin == 0:
        f=open(name+'.txt')
    else:
        f=open(name+'.txt','rb')
    for chunks in readChunks(f,2048):
        if bin == 0:
            encoded_message=chunks.encode()
        else:
            encoded_message=chunks
        ciphertext = public_key.encrypt(
               encoded_message,
               padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
          )
        with open(outE+'.txt','wb+') as ff:
            ff.write(ciphertext)
    f.close()
    ff.close()

def decrypt(enc,outD,bin=0):
    
    ### load key
    with open("privateK.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                   key_file.read(),
                   password=None,
                  )   
    ########################
    f=open(enc+'.txt',"rb")
    for chunks in readChunks(f,2048):
        plaintext = private_key.decrypt(
            chunks,
            padding.OAEP(
                  mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                       )
             )
        # can open with W+ only and write the .decoded()
        with open(outD+'.txt','wb+') as ff:
             ff.write(plaintext)
    f.close()
    ff.close()


def readChunks(fileO,var):
    """ Read file in variable chunk size
                """
    while True:
        data = fileO.read(var)
        if not data:
            break
        yield data
