from datetime import datetime
from typing import Optional

from app.models.user_models import UserMood
from pydantic import BaseModel, ConfigDict, Field, validator


class ResponseFullUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: int
    created: datetime
    mood: UserMood


class UpdateUser(BaseModel):
    id: int = Field(alias="user_id")
    mood: str

    @validator("mood")
    def mood_valid(cls, mood):
        return UserMood[mood.upper()]


class CreateWish(BaseModel):

    name: str
    url: Optional[str]
    prioritet: Optional[int]
    user_id: int
