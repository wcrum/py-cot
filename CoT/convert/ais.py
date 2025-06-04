import datetime
from CoT.models.core import Event, Point

def FromAIS(data: bytes) -> Event:
    try:
        import pyais
        _pyais_available = True
    except ImportError:
        _pyais_available = False

    if not _pyais_available:
        raise ImportError("The 'pyais' library is required for FromAIS but is not installed. Install it with: pip install pycot[ais]")
    
    ais_decoded = pyais.decode(data)
    ais_dict = ais_decoded.asdict()

    now = datetime.datetime.now(datetime.timezone.utc)
    stale = now + datetime.timedelta(minutes=2)

    return Event(
        version="2.0",
        type="a-u-S-X-M",
        access="Undefined",
        uid="MMSI-{}".format(ais_dict['MetaData']['MMSI']),
        time=now,
        start=now,
        stale=stale,
        how="m-f",
        qos="2-i-c",
        point=Point(lat=float(ais_dict["Message"]["PositionReport"]["Latitude"]), lon=float(ais_dict["Message"]["PositionReport"]["Longitude"]), hae=9999999, ce=9999999, le=9999999),
        detail={"contact": {"callsign": ais_dict["MetaData"]["ShipName"]}},
    )

def FromGeoJSON(dict) -> Event:
    pass