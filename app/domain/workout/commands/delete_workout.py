from pydantic import BaseModel, ConfigDict

from app.shared.types import Id, UserId


class DeleteWorkoutCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    workout_id: Id
    actor_id: UserId
