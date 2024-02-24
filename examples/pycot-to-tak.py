import datetime
import socket

import CoT

now = datetime.datetime.now(datetime.timezone.utc)
stale = now + datetime.timedelta(minutes=2)

# Generate new CoT event
py_cot = CoT.Event(
    version="2.0",
    type="a-f-A-M-H-I",
    access="Unclassified",
    uid="Debug.Python",
    time=now,
    start=now,
    stale=stale,
    how="h-t",
    qos="2-i-c",
    point=CoT.models.Point(lat=0, lon=0, hae=0, ce=0, le=0),
)

TAK_IP = "127.0.0.1"
TAK_PORT = 4242

# Send to TAK
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(py_cot.xml(), encoding="utf-8"), (TAK_IP, TAK_PORT))
