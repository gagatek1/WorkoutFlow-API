from datetime import datetime

from sqlalchemy import select, tuple_
from sqlalchemy.orm import Session

from app.domain.workout.entity import WorkoutModel
from app.domain.workout.exceptions import WorkoutNotFoundError


class WorkoutRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, workout: WorkoutModel) -> None:
        self._session.add(workout)
        self._session.flush()

    def get_owned(self, workout_id: str, owner: str, *, for_update: bool = False) -> WorkoutModel:
        stmt = select(WorkoutModel).where(WorkoutModel.id == workout_id, WorkoutModel.owner_id == owner)
        workout = self._session.scalar(stmt.with_for_update() if for_update else stmt)
        if workout is None:
            raise WorkoutNotFoundError
        return workout

    def delete(self, workout: WorkoutModel) -> None:
        self._session.delete(workout)

    def list_page(self, owner: str, limit: int, after: tuple[datetime, str] | None) -> list[WorkoutModel]:
        stmt = select(WorkoutModel).where(WorkoutModel.owner_id == owner)
        if after is not None:
            stmt = stmt.where(tuple_(WorkoutModel.created_at, WorkoutModel.id) > tuple_(*after))
        stmt = stmt.order_by(WorkoutModel.created_at, WorkoutModel.id).limit(limit)
        return list(self._session.scalars(stmt))
