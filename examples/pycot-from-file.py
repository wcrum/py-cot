import datetime
import xml.etree.ElementTree as ElementTree

import CoT

with open("../tests/messages/MITRE-Message.xml", "r", encoding="utf-8") as file:
    event = CoT.Event(**CoT.xml.parse(file.read()))

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

# todo: Init type description from XML
# assert event.type.desc == "TANK"
# assert event.type.full == "Gnd/Equip/Vehic/Armor/Tank"
# assert event.type.relation == "hostile"
