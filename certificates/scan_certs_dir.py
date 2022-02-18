from cryptography import x509
import os

path = '/etc/ssl/certs/'
obj = os.scandir(path)

certs = {}

def scan_dir(obj):
    for entry in obj:
        if entry.is_dir():
            scan_dir(os.scandir(path + entry.name))
        if entry.is_file():
            try:
                with open(path + entry.name, "rb") as f:
                    temp = f.read()
                    cert  = x509.load_pem_x509_certificate(temp)
                    certs[cert.subject] = (temp, cert)
            except:
                continue


scan_dir(obj)

for entry in certs.keys():
    print(entry)
    print()
    print()
    print(certs[entry][0])
    print()
    print()

def get_entry_path(entry):
    with open(entry, "rb") as f:
        temp = f.read()
        cert = x509.load_pem_x509_certificate(temp)
        c2 = cert
        path = [c2.issuer]
        while True:
            flag = False
            for i in certs.keys():
                c1 = certs[i][1]
                if c1.issuer is c2.subject:
                    path = [c1.issuer] + path
                    c2 = c1
                    flag = True
                    break

            if not flag:
                break
        return path


print(get_entry_path(path + "Starfield_Root_Certificate_Authority_-_G2.pem"))











