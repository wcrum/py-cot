import datetime
import socket

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

TAK_IP = "x.x.x.x"
TAK_PORT = 8089

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TAK_IP, TAK_PORT))

sock.sendall(bytes(py_cot.xml(), encoding="utf-8"))
