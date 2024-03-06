import socket
import time
from datetime import datetime, timedelta, timezone

import CoT
from skyfield.api import Loader, load, wgs84

stations_url = "http://celestrak.com/NORAD/elements/gps-ops.txt"  # will locally download gps-ops.txt
satellites = load.tle_file(stations_url)

# LOAD OFFLINE FILE
# satellites = load.tle_file('gps-ops.txt')

TAK_IP = "localhost"
TAK_PORT = 1234

# UDP Connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# TCP Connection
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((TAK_IP, TAK_PORT))

ts = load.timescale()

while True:
    now = datetime.now(timezone.utc)
    stale = now + timedelta(minutes=2)

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
            # UDP Connection
            sock.sendto(bytes(satCoT.xml(), encoding="utf-8"), ((TAK_IP, TAK_PORT)))
            # TCP Connection
            # sock.sendall(bytes(satCoT.xml(), encoding="utf-8"))
        except:
            print("Bad satellite TLE data.")

    # Dont overload UDP / TCP Connections
    time.sleep(1)
