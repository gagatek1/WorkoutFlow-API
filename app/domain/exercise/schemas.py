from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from app.shared.types import Count, Name, Weight


class ExercisePart(StrEnum):
    BACK = "back"
    BICEPS = "biceps"
    CHEST = "chest"
    CORE = "core"
    LEGS = "legs"
    SHOULDERS = "shoulders"
    TRICEPS = "triceps"


class CreateExerciseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: Name
    sets: Count
    reps: Count
    weight: Weight
    part: ExercisePart


class UpdateExerciseRequest(CreateExerciseRequest):
    pass


class ExerciseSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    part: ExercisePart


class ExerciseResponse(ExerciseSummaryResponse):
    workout_id: str
    sets: int
    reps: int
    weight: int


class ExerciseListResponse(BaseModel):
    items: list[ExerciseSummaryResponse]
    next_cursor: str | None
