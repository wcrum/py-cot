from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, EmailStr, Field, HttpUrl

import CoT
from CoT.utils import CustomModel


class MITRERemarks(CustomModel):
    source: Optional[str] = None
    time: Optional[datetime] = None
    to: Optional[str] = None
    keywords: Optional[str] = Field(None, pattern=r"[\w\- ]+(,[\w\- ]+)*")
    version: Optional[float] = None
    text: Optional[str] = None


class MITREFlowTags(CustomModel):
    version: float = Field(None, description="Schema version.")
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")


class MITREUid(CustomModel):
    version: Optional[float] = Field(
        None, ge=0, description="The version of the UID schema"
    )
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")


class MITREAttitude(CustomModel):
    roll: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Roll of entity in degrees. Positive indicates listing to the right.",
    )
    pitch: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Pitch of entity in degrees. Positive indicates nose point up.",
    )
    yaw: Optional[float] = Field(
        None,
        ge=-180,
        le=180,
        description="Yaw of entity in degrees. Positive indicates turned to the right.",
    )
    eRoll: Optional[float] = Field(
        None,
        ge=0,
        description="1-sigma error of roll with respect to a zero mean normal Gaussian distribution.",
    )
    ePitch: Optional[float] = Field(
        None,
        description="1-sigma error of pitch with respect to a zero mean normal Gaussian distribution.",
    )
    eYaw: Optional[float] = Field(
        None,
        description="1-sigma error of yaw with respect to a zero mean normal Gaussian distribution.",
    )


class MITRESpin(CustomModel):
    roll: float = Field(
        ...,
        description="Degrees per second with positive indicating to the pilot's right",
    )
    pitch: float = Field(
        ..., description="Degrees per second with positive indicating nose up."
    )
    yaw: Optional[float] = Field(
        None, description="Degrees per second with positive indicating right."
    )
    eRoll: Optional[float] = Field(
        None,
        ge=0,
        description="1-sigma error of roll with respect to a zero mean normal Gaussian distribution.",
    )
    ePitch: Optional[float] = Field(
        None,
        ge=0,
        description="1-sigma error of pitch with respect to a zero mean normal Gaussian distribution.",
    )
    eYaw: Optional[float] = Field(
        None,
        ge=0,
        description="1-sigma error of yaw with respect to a zero mean normal Gaussian distribution.",
    )


class MTIRESpatial(CustomModel):
    attitude: MITREAttitude
    spin: MITRESpin
    version: Optional[float] = Field(
        None,
        description="Version tag for this sub schema. Necessary to ensure upward compatibility with future revisions.",
    )


class MITRELink(CustomModel):
    relation: str = Field(
        ..., description="The type of relationship this link describes."
    )
    uid: str = Field(..., description="The unique identifier of the related object.")
    type: str = Field(..., description="The CoT type of the referenced object.")
    url: Optional[HttpUrl] = Field(
        None, description="URL to retrieve the linked object."
    )
    remarks: Optional[str] = Field(
        None, description="Additional comments about the link."
    )
    mime: Optional[str] = Field(
        None, description="Internet Media type of the referenced object."
    )
    version: Optional[float] = Field(None, description="Version tag for compatibility.")
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")


class MITRETrack(CustomModel):
    course: float = Field(
        ...,
        ge=0,
        le=360,
        description="Direction of motion with respect to true north in degrees",
    )
    speed: float = Field(
        ..., ge=0, description="Magnitude of motion measured in meters per second"
    )
    slope: Optional[float] = Field(
        None,
        ge=-90,
        le=90,
        description="Vertical component of motion vector in degrees",
    )
    eCourse: Optional[float] = Field(
        None,
        description="1-sigma error on a Gaussian distribution associated with the course attribute",
    )
    eSpeed: Optional[float] = Field(
        None,
        description="1-sigma error on a Gaussian distribution associated with the speed attribute",
    )
    eSlope: Optional[float] = Field(
        None,
        description="1-sigma error on a Gaussian distribution associated with the slope attribute",
    )
    version: Optional[float] = Field(None, description="Schema version")


class MITRERequest(CustomModel):
    notify: HttpUrl = Field(
        ..., description="Network endpoint for status notifications."
    )
    wilcoby: Optional[datetime] = Field(
        None, description="Deadline for WILCO/CANTCO acknowledgement."
    )
    priority: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Request's relative priority."
    )
    version: Optional[float] = Field(
        None, description="Version tag for this sub schema."
    )
    to: Optional[str] = Field(
        None, description="CoT UID of the specific entity addressed."
    )
    authority: Optional[str] = Field(
        None, description="CoT UID of the entity authorizing the request."
    )
    streamto: Optional[str] = Field(
        None, description="Additional streaming directions."
    )


class MITREDetail(CustomModel):
    remarks: Optional[MITRERemarks]
    flowTags: Optional[MITREFlowTags] = Field(alias="_flow-tags_")
    spatial: Optional[MITRESpin]
    uid: Optional[MITREUid]
    track: Optional[MITRETrack]
    request: Optional[MITRERequest]


class MITREContact(CustomModel):
    callsign: Optional[str] = None
    freq: Optional[float] = None
    email: Optional[EmailStr] = None
    dsn: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    modulation: Optional[str] = None
    hostname: Optional[str] = None
    version: Optional[float] = None


class Event(CoT.Event):
    detail: Optional[MITREDetail]
