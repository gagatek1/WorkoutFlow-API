from app.domain.exercise.commands.update_exercise import UpdateExerciseCommand
from app.domain.exercise.repository import ExerciseRepository
from app.domain.exercise.schemas import ExerciseResponse
from app.shared.db import unit_of_work


def update_exercise_handler(command: UpdateExerciseCommand) -> ExerciseResponse:
    with unit_of_work() as session:
        exercises = ExerciseRepository(session)
        workout, profile = exercises.lock_totals(command.workout_id, command.actor_id)
        exercise = exercises.get_owned(command.workout_id, command.exercise_id, command.actor_id)
        old_volume = exercise.volume
        exercise.name = command.name
        exercise.sets = command.sets
        exercise.reps = command.reps
        exercise.weight = command.weight
        exercise.part = command.part
        workout.total_weight += exercise.volume - old_volume
        profile.total_weight += exercise.volume - old_volume
        return ExerciseResponse.model_validate(exercise)
