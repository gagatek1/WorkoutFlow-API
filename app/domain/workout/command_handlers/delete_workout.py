from app.domain.exercise.repository import ExerciseRepository
from app.domain.profile.repository import ProfileRepository
from app.domain.workout.commands.delete_workout import DeleteWorkoutCommand
from app.domain.workout.exceptions import WorkoutHasExercisesError
from app.domain.workout.repository import WorkoutRepository
from app.shared.db import unit_of_work


def delete_workout_handler(command: DeleteWorkoutCommand) -> None:
    with unit_of_work() as session:
        workouts = WorkoutRepository(session)
        workout = workouts.get_owned(command.workout_id, command.actor_id, for_update=True)
        if ExerciseRepository(session).exists_in_workout(workout.id):
            raise WorkoutHasExercisesError
        ProfileRepository(session).get_for_update(command.actor_id).workout_quantity -= 1
        workouts.delete(workout)
