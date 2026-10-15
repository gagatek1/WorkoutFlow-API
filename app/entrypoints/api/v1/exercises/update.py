from typing import Annotated

from fastapi import APIRouter, Path, Request

from app.domain.exercise.command_handlers.update_exercise import update_exercise_handler
from app.domain.exercise.commands.update_exercise import UpdateExerciseCommand
from app.domain.exercise.schemas import ExerciseResponse, UpdateExerciseRequest
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["exercises"])


@router.put(
    "/workouts/{workout_id}/exercises/{exercise_id}",
    description="Update an exercise; updates workout and profile totals.",
)
def update_exercise(
    workout_id: Annotated[str, Path(pattern=ID_PATTERN, description="Workout id")],
    exercise_id: Annotated[str, Path(pattern=ID_PATTERN, description="Exercise id")],
    body: UpdateExerciseRequest,
    request: Request,
) -> ExerciseResponse:
    with authorize_user(request.headers) as user:
        return update_exercise_handler(
            UpdateExerciseCommand(workout_id=workout_id, exercise_id=exercise_id, actor_id=user.id, **body.model_dump())
        )
