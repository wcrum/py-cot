import socket
import ssl
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates

# Load the .p12 file
p12_file_path = 'examples/admin.p12'
p12_password = b'atakatak'

with open(p12_file_path, 'rb') as f:
    p12_data = f.read()

private_key, certificate, additional_certificates = load_key_and_certificates(p12_data, p12_password)

# Save cert and key to temp files
with open('client_cert.pem', 'wb') as cert_file:
    cert_file.write(certificate.public_bytes(Encoding.PEM))

with open('client_key.pem', 'wb') as key_file:
    key_file.write(private_key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()))

# Insecure context
context = ssl._create_unverified_context()
context.load_cert_chain(certfile='client_cert.pem', keyfile='client_key.pem')

# Connect to server
hostname = 'x.x.x.x'
port = 8089

import datetime
import CoT

now = datetime.datetime.now(datetime.timezone.utc)
stale = now + datetime.timedelta(minutes=2)

# Generate new CoT event
py_cot = CoT.Event(
    version="2.0",
    type="a-u-G-U-U-S-R-S",
    access="Undefined",
    uid="Debug.Python",
    time=now,
    start=now,
    stale=stale,
    how="h-g-i-g-o",
    qos="2-i-c",
    point=CoT.Point(lat=2, lon=2, hae=9999999, ce=9999999, le=9999999),
    detail={"contact": {"callsign": "Debug.Python"}},
)

data = py_cot.xml()
b = bytes(data, encoding="utf-8")

with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        ssock.sendall(b)
        data = ssock.recv(1024)