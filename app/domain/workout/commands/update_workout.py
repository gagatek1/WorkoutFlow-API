import datetime as dt

from pydantic import BaseModel, ConfigDict

from app.shared.types import Id, Name, UserId


class UpdateWorkoutCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    workout_id: Id
    actor_id: UserId
    name: Name
    date: dt.date
