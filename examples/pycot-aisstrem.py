import socket
import ssl
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
import asyncio
import websockets
import json
import datetime
import CoT


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

def get_sar(mmsi: str) -> bool:
    """Get the AIS Search-And-Rescue (SAR) status of a given MMSI.

    Search and Rescue Aircraft:
        AIS and DSC equipment used on search and rescue aircraft use the format
        111213M4I5D6X7X8X9 where the digits 4, 5 and 6 represent the MID and X
        is any figure from 0 to 9. In the United States, these MMSIs are
        currently only used by the U.S. Coast Guard.
        Src: https://www.navcen.uscg.gov/?pageName=mtmmsi

    :param mmsi: str MMSI as decoded from AIS data.
    :return:
    """
    sar = False
    _mmsi = str(mmsi)
    if _mmsi[:3] == "111":
        sar = True
    elif _mmsi[:5] in ["30386", "33885"]:  # US Coast Guard
        sar = True
    return sar

def create_cot_event(message: dict):
    now = datetime.datetime.now(datetime.timezone.utc)
    stale = now + datetime.timedelta(minutes=2)

    print(message['Message']['PositionReport'])
    print(message)

    return CoT.Event(
        version="2.0",
        type="a-u-S-X-M",
        access="Undefined",
        uid="MMSI-{}".format(message['MetaData']['MMSI']),
        time=now,
        start=now,
        stale=stale,
        how="m-f",
        qos="2-i-c",
        point=CoT.Point(lat=float(message["Message"]["PositionReport"]["Latitude"]), lon=float(message["Message"]["PositionReport"]["Longitude"]), hae=9999999, ce=9999999, le=9999999),
        detail={"contact": {"callsign": message["MetaData"]["ShipName"]}},
    )

async def connect_ais_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {
            "APIKey": "",
            "BoundingBoxes": [[[-90, -180], [90, 180]]],
            "FilteringMMSI": ["368207620", "367719770", "211476060"],
            "FilderingMessageTypes": ["PositionReport"]
        }
        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]
            if message_type == "PositionReport":
                ais_message = message['Message']['PositionReport']
                cot_event = create_cot_event(message)
                data = cot_event.xml()
                b = bytes(data, encoding="utf-8")

                with socket.create_connection((hostname, port)) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        ssock.sendall(b)
                        data = ssock.recv(1024)


def main():
    asyncio.run(asyncio.run(connect_ais_stream()))
    
if __name__ == "__main__":
    main() 