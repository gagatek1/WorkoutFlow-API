from pydantic import BaseModel, ConfigDict

from app.domain.exercise.schemas import ExercisePart
from app.shared.types import Count, Id, Name, UserId, Weight


class UpdateExerciseCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    workout_id: Id
    exercise_id: Id
    actor_id: UserId
    name: Name
    sets: Count
    reps: Count
    weight: Weight
    part: ExercisePart
