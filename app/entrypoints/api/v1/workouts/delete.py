from typing import Annotated

from fastapi import APIRouter, Path, Request, Response, status

from app.domain.workout.command_handlers.delete_workout import delete_workout_handler
from app.domain.workout.commands.delete_workout import DeleteWorkoutCommand
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["workouts"])


@router.delete(
    "/workouts/{workout_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    description="Delete one of the caller's workouts (it must have no exercises).",
)
def delete_workout(
    workout_id: Annotated[str, Path(pattern=ID_PATTERN, description="Workout id")], request: Request
) -> None:
    with authorize_user(request.headers) as user:
        delete_workout_handler(DeleteWorkoutCommand(workout_id=workout_id, actor_id=user.id))
