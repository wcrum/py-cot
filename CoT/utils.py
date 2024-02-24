from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class CustomModel(BaseModel):
    @field_serializer("dt", check_fields=False)
    def serialize_dt(self, dt: datetime, _info):
        return dt.timestamp()

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        populate_by_name=True,
    )
