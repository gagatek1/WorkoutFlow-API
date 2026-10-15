from pydantic import BaseModel, ConfigDict

from app.shared.types import PersonName, UserId


class UpdateProfileCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    user_id: UserId
    first_name: PersonName
    last_name: PersonName
