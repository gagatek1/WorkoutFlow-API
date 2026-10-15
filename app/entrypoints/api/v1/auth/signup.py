from fastapi import APIRouter, status

from app.domain.identity.command_handlers.sign_up import sign_up_handler
from app.domain.identity.commands.sign_up import SignUpCommand
from app.domain.identity.schemas import SignUpRequest, SignUpResponse
from app.domain.profile.command_handlers.create_profile import create_profile_handler
from app.domain.profile.commands.create_profile import CreateProfileCommand

router = APIRouter(tags=["auth"])


@router.post(
    "/auth/signup",
    status_code=status.HTTP_201_CREATED,
    description="Sign up a new user and create their profile (public).",
)
def signup(body: SignUpRequest) -> SignUpResponse:
    account = sign_up_handler(SignUpCommand(email=body.email, password=body.password))
    create_profile_handler(
        CreateProfileCommand(user_id=account.sub, first_name=body.first_name, last_name=body.last_name)
    )
    return account
