from pydantic import BaseModel, ConfigDict, Field

from app.shared.types import PersonName


class UpdateProfileRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: PersonName
    last_name: PersonName


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str = Field(validation_alias="user_id")
    first_name: str
    last_name: str
    total_weight: int
    workout_quantity: int
