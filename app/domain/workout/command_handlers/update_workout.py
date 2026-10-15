from app.domain.workout.commands.update_workout import UpdateWorkoutCommand
from app.domain.workout.repository import WorkoutRepository
from app.domain.workout.schemas import WorkoutResponse
from app.shared.db import unit_of_work


def update_workout_handler(command: UpdateWorkoutCommand) -> WorkoutResponse:
    with unit_of_work() as session:
        workout = WorkoutRepository(session).get_owned(command.workout_id, command.actor_id, for_update=True)
        workout.name = command.name
        workout.date = command.date
        return WorkoutResponse.model_validate(workout)
