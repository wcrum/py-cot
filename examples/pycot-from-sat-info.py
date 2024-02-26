from datetime import datetime, timedelta, timezone

from skyfield.api import load, wgs84

import CoT

ts = load.timescale()
t = ts.now()

now = datetime.now(timezone.utc)
stale = now + timedelta(minutes=2)

stations_url = "http://celestrak.com/NORAD/elements/gps-ops.txt"
satellites = load.tle_file(stations_url)

for sat in satellites:
    geocentric = sat.at(t)
    lat, lon = wgs84.latlon_of(geocentric)

    satCoT = CoT.Event(
        type="a-.-G-U-U-S-R-S",
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
    )
