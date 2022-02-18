from cryptography import x509
import datetime

with open("cert1.txt", "rb") as f:
    pem_data = f.read()
cert = x509.load_pem_x509_certificate(pem_data)
print(cert.serial_number)

def validate(cert):
    return (cert.not_valid_before<datetime.datetime.today()< cert.not_valid_after)

print(validate(cert))
