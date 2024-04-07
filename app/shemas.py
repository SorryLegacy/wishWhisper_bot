from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, validator

from app.models.user_models import UserMood


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
