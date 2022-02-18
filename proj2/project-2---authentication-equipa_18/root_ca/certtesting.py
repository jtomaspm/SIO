from cryptography import x509

with open("app_sec.cert.pem", "rb") as f:
    pem_data = f.read()


with open("intermediate_01.cert.pem", "rb") as f:
    intermediate = f.read()


cert = x509.load_pem_x509_certificate(pem_data)
certint = x509.load_pem_x509_certificate(intermediate)

print(cert.issuer == certint.subject)
print(cert.serial_number)
print(cert.signature)



