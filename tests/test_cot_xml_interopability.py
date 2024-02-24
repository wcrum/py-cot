import json

import CoT

xml_cot = """<?xml version="2.0"?>
    <event
        version="2.0"
        type="a-h-G-E-V-A-T"
        access="Unclassified"
        uid="FBCB2.T-117"
        time="2002-10-05T18:00:23.00Z"
        start="2002-10-05T18:00:23.00Z"
        stale="2002-10-05T18:00:23.00Z"
        how="m-i">
    <point lat="26.4321" lon="-82.0554" hae="0" ce="32" le="221"/>
    </event>
"""

py_cot = CoT.Event(
    version="2.0",
    type="a-h-G-E-V-A-T",
    access="Unclassified",
    uid="FBCB2.T-117",
    time="2002-10-05T18:00:23.00Z",
    start="2002-10-05T18:00:23.00Z",
    stale="2002-10-05T18:00:23.00Z",
    how="m-i",
    point=CoT.models.Point(lat=26.4321, lon=-82.0554, hae=0, ce=32, le=221.0),
)

json_cot = """{
    "event": {
        "version": 2.0,
        "type": "a-h-G-E-V-A-T",
        "access": "Unclassified",
        "uid": "FBCB2.T-117",
        "time": "2002-10-05T18:00:23.00Z",
        "start": "2002-10-05T18:00:23.00Z",
        "stale": "2002-10-05T18:00:23.00Z",
        "how": "m-i",
        "point": {
            "lat": 26.4321,
            "lon": -82.0554,
            "hae": 0.0,
            "ce": 32.0,
            "le": 221.0
        }
    }
}"""


def test_json_to_xml_check():
    # Checking if two strings are the same is a terrible
    # way of checking if the XML data is the same
    # to test if the XML == PyCoT XML
    # I am first creating an element in PyCoT
    # Turning it into XML, loading it back as if it was
    # Just XML and then comparing that to the loaded XML
    # At the end both values should be the same

    t1 = CoT.Event(**CoT.xml.parse(py_cot.xml()))

    t2 = CoT.Event(**CoT.xml.parse(xml_cot))

    t3 = CoT.Event(**json.loads(json_cot)["event"])

    assert t1.model_dump_json() == t2.model_dump_json() == t3.model_dump_json()
