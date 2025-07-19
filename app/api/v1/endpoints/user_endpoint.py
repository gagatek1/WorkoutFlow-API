from fastapi import APIRouter, Depends

from app.core.cognito import Cognito
from app.core.database import db_dependency
from app.core.dependencies import get_cognito
from app.core.security import get_token as security_get_token
from app.schemas.user import User, UserEmail
from app.services.user.get_service import get_service, me_service
from app.services.user.update_email_service import (get_token,
                                                    update_email_service)
from app.services.user.update_service import update_service

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/email")
async def change_email(
    data: UserEmail,
    cognito: Cognito = Depends(get_cognito),
    user: dict = Depends(get_token),
):
    return update_email_service(data, user, cognito)


@user_router.put("/")
async def update_profile(
    update_profile: User,
    db: db_dependency,
    cognito_user: dict = Depends(get_token),
):
    return update_service(update_profile, db, cognito_user)


@user_router.get("/{user_id}")
async def get_profile(
    user_id, db: db_dependency, cognito_user: dict = Depends(security_get_token)
):
    return get_service(user_id, db)


@user_router.get("/")
async def get_my_profile(
    db: db_dependency, cognito_user: dict = Depends(security_get_token)
):
    return me_service(db, cognito_user)
