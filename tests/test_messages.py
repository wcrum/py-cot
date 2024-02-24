import glob
import os

import pytest

import CoT

working_directory = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize("filename", glob.glob(working_directory + "/messages/*.cot"))
def test_cot_file(filename):
    print(os.path.dirname(os.path.abspath(__file__)))
    with open(filename, "r", encoding="utf-8") as file:
        xml_dict = CoT.xml.parse(file.read())
        xml_event = CoT.Event(**xml_dict)

        pycot_xml = xml_event.xml()
        pycot_event = CoT.Event(**CoT.xml.parse(pycot_xml))

        # Ensure that the set of the json is empty
        # Make sure both combined are not unique
        assert not set(pycot_event.model_dump_json()) ^ set(xml_event.model_dump_json())
