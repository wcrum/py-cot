<div align="center">
    <img src="https://pbs.twimg.com/profile_images/1204604531415212032/S8R5zrhc_400x400.jpg" height="150px"></img>
    <h1>PyCot</h1>
    <subtitle>Python Cursor on Target Library</subtitle>
</div> 

# Summary

PyCot is developed to assist and streamline integration with programs that utilize Cursor on Target (CoT). This tool seeks to help generate, validate, and parse XML data that is defined from either MITRE or the MIL-STD.

## Why?

I needed an easy way to interface with CoT messages, I could not find one available.

## Usage

```shell
pipx install PyCot
```

```python
import CoT
import datetime
import socket

now = datetime.datetime.now(datetime.timezone.utc)
stale = now + datetime.timedelta(minutes=2)

# Generate new Cursor on Target Event
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
    point=CoT.Point(lat=90, lon=90, hae=9999999, ce=9999999, le=9999999),
    detail={"contact": {"callsign": "Debug.Python"}},
)

# Your TAK IPv4 / Port
TAK_IP = "x.x.x.x"
TAK_PORT = 9000

# Sending UDP -> TAK Insecure Anonymous Port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TAK_IP, TAK_PORT))

sock.sendall(bytes(py_cot.xml(), encoding="utf-8"))
```