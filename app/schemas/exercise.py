from typing import Optional

from pydantic import BaseModel

from app.models.exercise import ExercisePart


class Exercise(BaseModel):
    name: str
    sets: int
    reps_in_set: int
    weight: int
    part: ExercisePart
    workout_id: int


class UpdateExercise(BaseModel):
    name: Optional[str] = None
    sets: Optional[int] = None
    reps_in_set: Optional[int] = None
    weight: Optional[int] = None
    part: Optional[ExercisePart] = None
