from fastapi import APIRouter, Depends

from app.core.cognito import Cognito
from app.core.dependencies import get_cognito
from app.schemas.user import UserEmail
from app.services.user.update_service import get_token, update_email_service

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/email")
async def change_email(
    data: UserEmail,
    cognito: Cognito = Depends(get_cognito),
    user: dict = Depends(get_token),
):
    return update_email_service(data, user, cognito)
