from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


LENGTH_OPTIONS = {
            "1" : 1024,
            "2" : 2048,
            "3" : 3072,
            "4" : 4096
        }


def get_RSA_keys(key_length):
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public_key = private_key.public_key()
    return(private_key, public_key)


def save_to_file(keys):
    priv_pem = keys[0].private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.TraditionalOpenSSL,
       encryption_algorithm=serialization.NoEncryption()
    )

    pub_pem = keys[1].public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("private_key.txt", "w") as f:
        to_write = ""
        for line in priv_pem.splitlines(0):
            to_write += line.decode("utf-8")
        f.write(to_write)
            
    with open("public_key.txt", "w") as f:
        to_write = ""
        for line in pub_pem.splitlines(0):
            to_write += line.decode("utf-8")
        f.write(to_write)


def main():
    print("Choose key length:")
    for key in LENGTH_OPTIONS.keys():
        print(f"{key}: {LENGTH_OPTIONS[key]}")
    key_length = 0
    while True:
        if key_length in LENGTH_OPTIONS.keys():
            break
        key_length = input("Enter a valid option: ")
    key_length = LENGTH_OPTIONS[key_length]
    keys = get_RSA_keys(key_length)
    save_to_file(keys)
    

main()
