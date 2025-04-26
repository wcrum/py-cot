import socket
import pyais
import CoT
import datetime
import ssl
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates

UDP_IP = "0.0.0.0" # Listen on all interfaces
UDP_PORT = 9009

TAK_HOSTNAME = 'x.x.x.x'
TAK_PORT = 8089

# Load the .p12 file
p12_file_path = '/admin.p12'
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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on {UDP_IP}:{UDP_PORT}")

while True:
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

        decoded = pyais.decode(data)


        ais_dict = decoded.asdict()


        # {'msg_type': 1, 'repeat': 0, 'mmsi': 368088610, 'status': <NavigationStatus.UnderWayUsingEngine: 0>, 'turn': 0.0, 'speed': 28.0, 'accuracy': False, 'lon': -122.383025, 'lat': 37.806888, 'course': 159.7, 'heading': 156, 'second': 54, 'maneuver': <ManeuverIndicator.NotAvailable: 0>, 'spare_1': b'\x00', 'raim': False, 'radio': 100365}

        now = datetime.datetime.now(datetime.timezone.utc)
        stale = now + datetime.timedelta(minutes=2)

        event = CoT.Event(
            version="2.0",
            type="a-u-S-X-M",
            access="Undefined",
            uid="MMSI-{}".format(ais_dict['mmsi']),
            time=now,
            start=now,
            stale=stale,
            how="m-f",
            qos="2-i-c",
            point=CoT.Point(lat=float(ais_dict['lat']), lon=float(ais_dict['lon']), hae=9999999, ce=9999999, le=9999999),
            detail={"contact": {"callsign": "MMSI-{}".format(ais_dict['mmsi'])}},
        )

        data = event.xml()
        b = bytes(data, encoding="utf-8")


        with socket.create_connection((TAK_HOSTNAME, TAK_PORT)) as tcp_sock:
            with context.wrap_socket(tcp_sock, server_hostname=TAK_HOSTNAME) as send_sock:
                send_sock.sendall(b)
                data = send_sock.recv(1024)
    except:
        print("Failed to parse ship.")
        continue