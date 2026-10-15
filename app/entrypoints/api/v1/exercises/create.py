from typing import Annotated

from fastapi import APIRouter, Path, Request, status

from app.domain.exercise.command_handlers.create_exercise import create_exercise_handler
from app.domain.exercise.commands.create_exercise import CreateExerciseCommand
from app.domain.exercise.schemas import CreateExerciseRequest, ExerciseResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["exercises"])


@router.post(
    "/workouts/{workout_id}/exercises",
    status_code=status.HTTP_201_CREATED,
    description="Add an exercise to one of the caller's workouts; updates workout and profile totals.",
)
def create_exercise(
    workout_id: Annotated[str, Path(pattern=ID_PATTERN, description="Workout id")],
    body: CreateExerciseRequest,
    request: Request,
) -> ExerciseResponse:
    with authorize_user(request.headers) as user:
        return create_exercise_handler(
            CreateExerciseCommand(workout_id=workout_id, actor_id=user.id, **body.model_dump())
        )
