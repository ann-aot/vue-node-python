from pydantic import BaseModel, Field, ConfigDict, field_serializer
from datetime import datetime


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StateBase(CustomBaseModel):
    name: str = Field(...,
                      min_length=1,
                      max_length=50,
                      description="State name"
                      )
    description: str | None = Field(None,
                                    max_length=200,
                                    description="State description"
                                    )
    is_active: bool = Field(True, description="Whether the state is active")
    sort_order: int = Field(0, ge=0, description="Sort order for display")


class StateCreate(StateBase):
    pass


class StateUpdate(CustomBaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    description: str | None = Field(None, max_length=200)
    is_active: bool | None = None
    sort_order: int | None = Field(None, ge=0)


class StateResponse(StateBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    @field_serializer("created_at", "updated_at", when_used="json")
    def serialize_dt(self, dt: datetime | None) -> str | None:
        return dt.isoformat() if dt else None
