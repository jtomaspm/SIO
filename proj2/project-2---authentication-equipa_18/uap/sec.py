import requests
from os import walk
from cryptography import x509
import hashlib

# html special character tokens
swap_list = [
    ["&", "&#38"],
    ["#", "&#35"],
    ["\"", "&#34"],
    ["'", "&#39"],
    ["(", "&#40"],
    [")", "&#41"],
    ["/", "&#47"],
    [";", "&#59"],
    ["<", "&#60"],
    [">", "&#62"]
]


# transform input into safe string
def swap_sp_char_for_token(string):
    for item in swap_list:
        string = string.replace(item[0], item[1])
    return string


# check for special characters
def check_for_sp_chars(string):
    for item in swap_list:
        if item[0] in string:
            return True
    return False


def verifyCertificates(domain):
    r = requests.get("http://" + domain + "/getCertificates")
    c = r.json()
    certificates = {}
    for key in c.keys():
        certificates[key] = x509.load_pem_x509_certificate(c[key].encode())
            
            
    #check for valid domain
    if domain in str(certificates["server"].subject):
        #check for valid certificate chain
        if certificates["server"].issuer == certificates["intermediate"].subject and certificates["intermediate"].issuer == certificates["ca"].subject and certificates["ca"].issuer == certificates["ca"].subject:
            #check for trusted CA
            ca_files = next(walk("certificates/"), (None, None, []))[2]
            for f in ca_files:
                print(f)
                print("######################################################")
                if str(f).split(".")[-1] == "pem":
                    cert = x509.load_pem_x509_certificate(open("certificates/"+f).read().encode())
                    if cert == certificates["ca"]:
                        return True

    return False

#get challenge responce
def get_cr(password, nonce):
    hashed_hex = hashlib.md5(password.encode() + nonce.encode()).hexdigest()
    hash_bin = str((bin(int(hashed_hex, 16))[2:]))
    while len(hash_bin)/4 != int(len(hash_bin)/4):
        hash_bin = "0" + hash_bin
    return hash_bin