from xmltodict import parse as _parse
from xmltodict import unparse


def parse(xml: str):
    return _parse(xml, attr_prefix="")["event"]
