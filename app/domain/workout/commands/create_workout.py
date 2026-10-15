import datetime as dt

from pydantic import BaseModel, ConfigDict

from app.shared.types import Name, UserId


class CreateWorkoutCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    owner_id: UserId
    name: Name
    date: dt.date | None = None
