import socket
import time
from datetime import UTC, datetime, timedelta, timezone

from skyfield.api import load, utc, wgs84

import CoT

now = datetime.now(timezone.utc)
stale = now + timedelta(minutes=2)

stations_url = "http://celestrak.com/NORAD/elements/gps-ops.txt"
satellites = load.tle_file(stations_url)

TAK_IP = "localhost"
TAK_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ts = load.timescale()

while True:
    t = ts.now()
    for sat in satellites:
        geocentric = sat.at(t)
        lat, lon = wgs84.latlon_of(geocentric)

        try:
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
                    hae=0,
                    le=0,
                    ce=0,
                ),
                detail={"contact": {"callsign": sat.name}},
            )
            sock.sendto(bytes(satCoT.xml(), encoding="utf-8"), ((TAK_IP, TAK_PORT)))
        except:
            print("Bad satellite TLE data.")
