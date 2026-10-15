from fastapi import APIRouter, Request

from app.domain.profile.command_handlers.update_profile import update_profile_handler
from app.domain.profile.commands.update_profile import UpdateProfileCommand
from app.domain.profile.schemas import ProfileResponse, UpdateProfileRequest
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["profiles"])


@router.put("/profiles/me", description="Create or update the caller's profile.")
def update_profile(body: UpdateProfileRequest, request: Request) -> ProfileResponse:
    with authorize_user(request.headers) as user:
        return update_profile_handler(UpdateProfileCommand(user_id=user.id, **body.model_dump()))
