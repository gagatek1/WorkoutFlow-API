from datetime import date
from typing import Any
from uuid import uuid4

import factory
from sqlalchemy.orm import Session

from app.domain.exercise.entity import ExerciseModel
from app.domain.exercise.schemas import ExercisePart
from app.domain.profile.entity import ProfileModel
from app.domain.workout.entity import WorkoutModel
from app.shared.db import unit_of_work


def _ensure_profile(session: Session, user_id: str) -> None:
    if session.get(ProfileModel, user_id) is None:
        session.add(ProfileModel(user_id=user_id, first_name="A", last_name="B", total_weight=0, workout_quantity=0))
        session.flush()


class OrmFactory[T: ProfileModel | WorkoutModel | ExerciseModel](factory.Factory[T]):
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class: type[T], *args: Any, **kwargs: Any) -> T:
        entity = model_class(*args, **kwargs)
        with unit_of_work() as session:
            if not isinstance(entity, ProfileModel):
                _ensure_profile(session, entity.owner_id)
            session.add(entity)
        return entity


class ProfileModelFactory(OrmFactory[ProfileModel]):
    class Meta:
        model = ProfileModel

    user_id = "alice"
    first_name = "Alice"
    last_name = "Smith"
    total_weight = 0
    workout_quantity = 0


class WorkoutModelFactory(OrmFactory[WorkoutModel]):
    class Meta:
        model = WorkoutModel

    id = factory.LazyFunction(lambda: str(uuid4()))
    owner_id = "alice"
    name = factory.Sequence(lambda n: f"Workout {n}")
    date = date(2026, 1, 1)
    total_weight = 0


class ExerciseModelFactory(OrmFactory[ExerciseModel]):
    class Meta:
        model = ExerciseModel

    id = factory.LazyFunction(lambda: str(uuid4()))
    workout_id = factory.LazyAttribute(lambda o: WorkoutModelFactory.create(owner_id=o.owner_id).id)
    owner_id = "alice"
    name = factory.Sequence(lambda n: f"Exercise {n}")
    sets = 3
    reps = 10
    weight = 0
    part = ExercisePart.CHEST
