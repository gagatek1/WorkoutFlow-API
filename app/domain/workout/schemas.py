import datetime as dt

from pydantic import BaseModel, ConfigDict

from app.shared.types import Name


class CreateWorkoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: Name
    date: dt.date | None = None


class UpdateWorkoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: Name
    date: dt.date


class WorkoutSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    date: dt.date


class WorkoutResponse(WorkoutSummaryResponse):
    total_weight: int


class WorkoutListResponse(BaseModel):
    items: list[WorkoutSummaryResponse]
    next_cursor: str | None
