from datetime import datetime

from sqlalchemy import exists, select, tuple_
from sqlalchemy.orm import Session

from app.domain.exercise.entity import ExerciseModel
from app.domain.exercise.exceptions import ExerciseNotFoundError
from app.domain.profile.entity import ProfileModel
from app.domain.profile.repository import ProfileRepository
from app.domain.workout.entity import WorkoutModel
from app.domain.workout.repository import WorkoutRepository


class ExerciseRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, exercise: ExerciseModel) -> None:
        self._session.add(exercise)
        self._session.flush()

    def get_owned(self, workout_id: str, exercise_id: str, owner: str) -> ExerciseModel:
        exercise = self._session.scalar(
            select(ExerciseModel).where(
                ExerciseModel.id == exercise_id, ExerciseModel.workout_id == workout_id, ExerciseModel.owner_id == owner
            )
        )
        if exercise is None:
            raise ExerciseNotFoundError
        return exercise

    def delete(self, exercise: ExerciseModel) -> None:
        self._session.delete(exercise)

    def exists_in_workout(self, workout_id: str) -> bool:
        return bool(self._session.scalar(select(exists().where(ExerciseModel.workout_id == workout_id))))

    def list_page(self, workout_id: str, limit: int, after: tuple[datetime, str] | None) -> list[ExerciseModel]:
        stmt = select(ExerciseModel).where(ExerciseModel.workout_id == workout_id)
        if after is not None:
            stmt = stmt.where(tuple_(ExerciseModel.created_at, ExerciseModel.id) > tuple_(*after))
        stmt = stmt.order_by(ExerciseModel.created_at, ExerciseModel.id).limit(limit)
        return list(self._session.scalars(stmt))

    def lock_totals(self, workout_id: str, owner: str) -> tuple[WorkoutModel, ProfileModel]:
        workout = WorkoutRepository(self._session).get_owned(workout_id, owner, for_update=True)
        return workout, ProfileRepository(self._session).get_for_update(owner)
