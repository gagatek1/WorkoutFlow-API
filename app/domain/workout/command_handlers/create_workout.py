from datetime import UTC, datetime
from uuid import uuid4

from app.domain.profile.repository import ProfileRepository
from app.domain.workout.commands.create_workout import CreateWorkoutCommand
from app.domain.workout.entity import WorkoutModel
from app.domain.workout.repository import WorkoutRepository
from app.domain.workout.schemas import WorkoutResponse
from app.shared.db import unit_of_work


def create_workout_handler(command: CreateWorkoutCommand) -> WorkoutResponse:
    with unit_of_work() as session:
        profile = ProfileRepository(session).get_for_update(command.owner_id)
        workout = WorkoutModel(
            id=str(uuid4()),
            owner_id=command.owner_id,
            name=command.name,
            date=command.date or datetime.now(UTC).date(),
            total_weight=0,
        )
        WorkoutRepository(session).add(workout)
        profile.workout_quantity += 1
        return WorkoutResponse.model_validate(workout)
