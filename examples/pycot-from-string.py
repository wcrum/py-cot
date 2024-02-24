import datetime

import CoT

string = """<?xml version="2.0"?>
    <event
        version="2.0"
        type="a-h-G-E-V-A-T"
        access="Unclassified"
        uid="FBCB2.T-117"
        time="2002-10-05T18:00:23Z"
        start="2002-10-05T18:00:23Z"
        stale="2002-10-05T18:00:23Z"
        how="m-i">
    <point lat="26.4321" lon="-82.0554" hae="0" ce="32" le="221"/>
    </event>
"""

event = CoT.Event(**CoT.xml.parse(string)["event"])

assert event.uid == "FBCB2.T-117"
assert event.access == "Unclassified"

assert event.time == datetime.datetime.strptime(
    "2002-10-05T18:00:23Z", "%Y-%m-%dT%H:%M:%S%z"
)
assert event.start == datetime.datetime.strptime(
    "2002-10-05T18:00:23Z", "%Y-%m-%dT%H:%M:%S%z"
)
assert event.time == datetime.datetime.strptime(
    "2002-10-05T18:00:23Z", "%Y-%m-%dT%H:%M:%S%z"
)

assert event.type == "a-h-G-E-V-A-T"
assert event.type.desc == "TANK"
assert event.type.full == "Gnd/Equip/Vehic/Armor/Tank"
assert event.type.relation == "hostile"
