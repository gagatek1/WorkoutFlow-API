from pydantic import BaseModel

from app.models.exercise import ExercisePart


class Exercise(BaseModel):
    name: str
    sets: int
    reps_in_set: int
    weight: int
    part: ExercisePart
    workout_id: int
