from typing import Annotated

from fastapi import APIRouter, Path, Request, Response, status

from app.domain.exercise.command_handlers.delete_exercise import delete_exercise_handler
from app.domain.exercise.commands.delete_exercise import DeleteExerciseCommand
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["exercises"])


@router.delete(
    "/workouts/{workout_id}/exercises/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    description="Delete an exercise; updates workout and profile totals.",
)
def delete_exercise(
    workout_id: Annotated[str, Path(pattern=ID_PATTERN, description="Workout id")],
    exercise_id: Annotated[str, Path(pattern=ID_PATTERN, description="Exercise id")],
    request: Request,
) -> None:
    with authorize_user(request.headers) as user:
        delete_exercise_handler(DeleteExerciseCommand(workout_id=workout_id, exercise_id=exercise_id, actor_id=user.id))
