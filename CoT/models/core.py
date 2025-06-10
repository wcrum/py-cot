import datetime
import re
from datetime import datetime
from typing import Optional, Any, Union, Literal

from pydantic import ConfigDict, Field, GetCoreSchemaHandler, computed_field, constr
from pydantic_core import CoreSchema, core_schema
from CoT.utils import CustomModel
from CoT.xml import unparse
from CoT.types import CoTTypes, CoTReservations, CoTHow
from pydantic import BaseModel
KeywordsPattern = constr(pattern=r"^[\w\- ]+(,[\w\- ]+)*$")

class Remarks(BaseModel):
    text: str

# https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV/blob/889eee292c43d3d2eafdd1f2fbf378ad5cd89ecc/takcot/mitre/CoT%20Image%20Schema%20%20(PUBLIC%20RELEASE).xsd
class Image(CustomModel):
    """
    Image metadata for Cursor On Target messages, based on MITRE schema.
    Specifically limited to geographically located (though not necessarily 
    geographically registered) image products.
    """
    # Fields required for image to display in TAK clients

    content: Optional[str] = None  # For base64 encoded image data
    url: Optional[str] = None  # URL link if image is not embedded
    source: Optional[str] = None  # CoT UID of the producer
    mime: str  # Required mime type for the image

    # Metadata for image display and postprocessing

    # Image type from NITF spec (MIL-STD-2500C APPENDIX A)
    type: Optional[Literal[
        "BP", # Black and White Picture
        "CP", # Color Picture
        "BARO", # Barometric pressure
        "CAT", # Computerized Axial Tomography scan
        "EO", # Electro-optical
        "FL", # Forward Looking Infrared
        "FP", # Fingerprints
        "HR", # High Resolution Radar
        "HS", # Hyperspectral
        "IR", # Infrared
        "MRI", # Magnetic Resonance Imaging
        "MS", # Multispectral
        "OP", # Optical
        "RD", # Radar
        "SAR", # Synthetic Aperture Radar
        "SARIQ", # Synthetic Aperture Radar Radio Hologram
        "SL", # Side Looking Radar
        "TI", # Thermal Infrared
    ]] = None  # Image type from NITF spec
    resolution: Optional[float] = None  # Meters per pixel
    size: Optional[int] = Field(None, ge=0)  # Approximate file size in bytes
    width: Optional[int] = Field(None, ge=0)  # Width in pixels
    height: Optional[int] = Field(None, ge=0)  # Height in pixels
    quality: Optional[str] = None  # Image quality vs compression trade-off. Floating point value between 0.0 and 1.0, where 1.0 is best quality.
    fov: Optional[float] = Field(None, ge=0, lt=360)  # Angular field of view in degrees
    version: Optional[float] = None  # Schema version
    reason: Optional[str] = None  # Reason image was produced
    bands: Optional[int] = Field(None, ge=0)  # Number of data bands within the image
    mimecsv: Optional[str] = None  # Supplementary mime types for container formats
    north: Optional[float] = Field(None, ge=0, lt=360)  # Orientation of north in degrees


class Track(CustomModel):
    """
    Track information for Cursor On Target messages, based on MITRE schema.
    Represents motion information including course, speed, and slope.
    """
    course: float = Field(ge=0, lt=360, description="Direction of motion with respect to true north. Measured in degrees.")
    speed: float = Field(ge=0.0, description="Magnitude of motion measured in meters per second")
    slope: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Vertical component of motion vector. Measured in degrees. Negative indicates downward motion.")
    eCourse: Optional[float] = Field(None, description="1-sigma error on a Gaussian distribution associated with the course attribute")
    eSpeed: Optional[float] = Field(None, description="1-sigma error on a Gaussian distribution associated with the speed attribute")
    eSlope: Optional[float] = Field(None, description="1-sigma error on a Gaussian distribution associated with the slope attribute")
    version: Optional[float] = None


# MITRE Definition does not have addition subschema
class Detail(CustomModel):
    model_config = ConfigDict(extras=True, populate_by_name=True)
    remarks: Optional[Remarks] = None
    image: Optional[Image] = None
    track: Optional[Track] = None


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
    

class How(str):
    value: str

    @computed_field
    @property
    def description(self) -> str:
        if self.value not in CoTHow:
            return "Unknown"
        
        return CoTHow[self.value]

class Event(CustomModel):
    version: float = 2.0
    type: Types
    uid: str
    time: datetime
    start: datetime
    stale: datetime
    how: How = Field(pattern=r"\w(-\w)+")
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


