import datetime
import json
from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field

from CoT.utils import CustomModel
from CoT.xml import unparse


# MITRE Definition does not have addition subschema
class Detail(CustomModel):
    model_config = ConfigDict(extra="allow")


class Point(CustomModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    hae: float
    ce: float
    le: float


class Event(CustomModel):
    version: float = 2.0
    type: str = Field(pattern=r"\w+(-\w+)*(;[^;]*)?")
    uid: str
    time: datetime
    start: datetime
    stale: datetime
    how: str = Field(pattern=r"\w-\w")
    opex: Optional[str] = None
    qos: Optional[str] = None
    access: Optional[str] = None
    detail: Optional[Detail] = None
    point: Optional[Point] = None

    def xml(self):
        return unparse(
            {"event": CustomModel.deep_prefix_add(self.model_dump(exclude_none=True))}
        )
