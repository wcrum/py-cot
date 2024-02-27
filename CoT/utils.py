import datetime
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer, model_serializer

TIME_FORMAT = "{:%Y-%m-%dT%H:%M:%S}.{:02.0f}Z"

from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Self

from pydantic import BaseModel, model_serializer


class CustomModel(BaseModel):
    #   -W ignore::pydantic.warnings.PydanticDeprecatedSince20
    model_config = ConfigDict(
        populate_by_name=True,
    )

    @model_serializer(mode="wrap")
    def serialize(
        self, original_serializer: Callable[[Self], dict[str, Any]]
    ) -> dict[str, Any]:
        for field_name, field_info in self.model_fields.items():
            if isinstance(getattr(self, field_name), datetime):
                setattr(
                    self,
                    field_name,
                    TIME_FORMAT.format(
                        getattr(self, field_name),
                        getattr(self, field_name).microsecond / 10000.0,
                    ),
                )

            elif isinstance(getattr(self, field_name), timedelta):
                result[field_name] = getattr(self, field_name).total_seconds()

        result = original_serializer(self)

        return result

    @classmethod
    def deep_prefix_add(self, obj, prefix="@"):
        second_dict = obj.copy()

        for key, value in obj.items():
            if isinstance(value, dict):
                second_dict[key] = CustomModel.deep_prefix_add(value)
                continue

            if key == "text":
                second_dict["#{key}"] = value
            else:
                second_dict[f"{prefix}{key}"] = value

            del second_dict[key]
        return second_dict
