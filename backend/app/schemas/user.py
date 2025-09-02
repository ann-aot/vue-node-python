from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(CustomBaseModel):
    email: str = Field(..., max_length=255)
    name: str = Field(..., max_length=255)
    avatar_url: Optional[str] = Field(None, max_length=512)
    dob: Optional[date] = None


class UserCreate(UserBase):
    google_sub: str = Field(..., max_length=64)


class UserResponse(UserBase):
    id: int
    google_sub: str
    created_at: datetime
    updated_at: Optional[datetime] = None

