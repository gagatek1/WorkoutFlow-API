from app.domain.exercise.commands.delete_exercise import DeleteExerciseCommand
from app.domain.exercise.repository import ExerciseRepository
from app.shared.db import unit_of_work


def delete_exercise_handler(command: DeleteExerciseCommand) -> None:
    with unit_of_work() as session:
        exercises = ExerciseRepository(session)
        workout, profile = exercises.lock_totals(command.workout_id, command.actor_id)
        exercise = exercises.get_owned(command.workout_id, command.exercise_id, command.actor_id)
        workout.total_weight -= exercise.volume
        profile.total_weight -= exercise.volume
        exercises.delete(exercise)
