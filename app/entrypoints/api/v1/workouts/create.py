from fastapi import APIRouter, Request, status

from app.domain.workout.command_handlers.create_workout import create_workout_handler
from app.domain.workout.commands.create_workout import CreateWorkoutCommand
from app.domain.workout.schemas import CreateWorkoutRequest, WorkoutResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["workouts"])


@router.post(
    "/workouts", status_code=status.HTTP_201_CREATED, description="Create a workout for the caller (date: today)."
)
def create_workout(body: CreateWorkoutRequest, request: Request) -> WorkoutResponse:
    with authorize_user(request.headers) as user:
        return create_workout_handler(CreateWorkoutCommand(owner_id=user.id, **body.model_dump()))
