# Data Sourced from network.igs.org
import json
import CoT
import datetime
import socket

def generate_cot_event(station):
    # Required fields
    uid = station.get("name", "UNKNOWN")
    lat, lon, hae = station.get("llh", [0, 0, 0])
    
    now = datetime.datetime.now(datetime.timezone.utc)
    stale = now + datetime.timedelta(minutes=90)

    # Optional metadata
    contact = {"callsign": uid}
    remarks_parts = [
        f"Receiver: {station.get('receiver_type')}",
        f"Antenna: {station.get('antenna_type')}",
        f"Firmware: {station.get('firmware')}",
        f"City: {station.get('city')}",
        f"Country: {station.get('country')}",
        f"Serial: {station.get('serial_number')}",
    ]
    remarks = "\n".join(filter(None, remarks_parts))

    # Build CoT event
    event = CoT.Event(
        version="2.0",
        type="a-u-P-S",  # Arbitrary MIL-STD-2525C type for unit
        uid=uid,
        time=now,
        start=now,
        stale=stale,
        how="m-g",  # machine generated
        qos="2-i-c",
        access="Undefined",
        point=CoT.Point(
            lat=lat,
            lon=lon,
            hae=hae,
            ce=9999999,
            le=9999999,
        ),
        detail={
            "contact": contact,
            "remarks": CoT.models.Remarks(
                text=remarks,
            )
        }
    )
    return event.xml()

def main():
    # Downloaded from network.igs.org
    with open("igs_stations.json", "r") as f:
        stations = json.load(f)

    for station in stations:
        cot_xml = generate_cot_event(station)
        print(cot_xml)
        TAK_IP = "0.0.0.0"
        TAK_PORT = 9090

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TAK_IP, TAK_PORT))

        sock.sendall(bytes(cot_xml, encoding="utf-8"))

if __name__ == "__main__":
    main()