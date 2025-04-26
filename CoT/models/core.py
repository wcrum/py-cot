import datetime
import re
from datetime import datetime
from typing import Optional, Any

from pydantic import ConfigDict, Field, GetCoreSchemaHandler, computed_field
from pydantic_core import CoreSchema, core_schema

from CoT.utils import CustomModel
from CoT.xml import unparse
from CoT.types import CoTTypes, CoTReservations


# MITRE Definition does not have addition subschema
class Detail(CustomModel):
    model_config = ConfigDict(extra="allow")


class Point(CustomModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    hae: float
    ce: float
    le: float



class Types(str):
    value: str

    @computed_field
    @property
    def description(self) -> str:
        searchType = self.split("-")
        searchType[1] = "."
        searchType = "-".join(searchType)

        if searchType not in CoTTypes:
            return "Unknown"
        
        return CoTTypes[searchType].get("desc")

    @computed_field
    @property
    def full(self) -> str:
        searchType = self.split("-")
        searchType[1] = "."
        searchType = "-".join(searchType)

        if searchType not in CoTTypes:
            return "Unknown"
        
        return CoTTypes[searchType].get("full")
    
    @computed_field
    @property
    def reservation(self) -> str:
        return CoTReservations[str(self).split("-")[1]]
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))
    
    

class Event(CustomModel):
    version: float = 2.0
    type: Types
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
        ).replace(
            '<?xml version="1.0" encoding="utf-8"?>',
            '<?xml version="1.0"?>',
        )
    

