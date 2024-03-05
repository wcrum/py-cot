import socket
import time
from datetime import UTC, datetime, timedelta, timezone

from skyfield.api import load, utc, wgs84

import CoT

ts = load.timescale()
t = ts.now()

now = datetime.now(timezone.utc)
stale = now + timedelta(minutes=2)

stations_url = "http://celestrak.com/NORAD/elements/gps-ops.txt"
satellites = load.tle_file(stations_url)

TAK_IP = "localhost"
TAK_PORT = 8999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TAK_IP, TAK_PORT))

d = datetime.now()
d = d.replace(tzinfo=utc)
ts = load.timescale()

while True:
    t = ts.from_datetime(d)
    for sat in satellites:
        geocentric = sat.at(t)
        lat, lon = wgs84.latlon_of(geocentric)

        satCoT = CoT.Event(
            type="a-u-G-U-U-S-R-S",
            uid=sat.name,
            access="Unclassified",
            how="h-e",
            time=now,
            start=now,
            stale=stale,
            point=CoT.Point(
                lat=lat.degrees,
                lon=lon.degrees,
                hae=90,
                le=90,
                ce=90,
            ),
            detail={"contact": {"callsign": sat.name}},
        )
        sock.sendall(bytes(satCoT.xml(), encoding="utf-8"))

    time.sleep(10)
