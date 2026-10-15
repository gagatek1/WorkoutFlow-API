from app.domain.exercise.commands.create_exercise import CreateExerciseCommand
from app.domain.exercise.entity import ExerciseModel
from app.domain.exercise.repository import ExerciseRepository
from app.domain.exercise.schemas import ExerciseResponse
from app.shared.db import unit_of_work


def create_exercise_handler(command: CreateExerciseCommand) -> ExerciseResponse:
    with unit_of_work() as session:
        exercises = ExerciseRepository(session)
        workout, profile = exercises.lock_totals(command.workout_id, command.actor_id)
        exercise = ExerciseModel(
            workout_id=command.workout_id,
            owner_id=command.actor_id,
            name=command.name,
            sets=command.sets,
            reps=command.reps,
            weight=command.weight,
            part=command.part,
        )
        exercises.add(exercise)
        workout.total_weight += exercise.volume
        profile.total_weight += exercise.volume
        return ExerciseResponse.model_validate(exercise)
