from fastapi import APIRouter, Depends
from starlette import status

from app.core.cognito import Cognito
from app.core.dependencies import get_cognito
from app.schemas.auth import UserSignIn, UserSignUp, UserVerify
from app.services.auth.signin_service import signin_service
from app.services.auth.signup_service import signup_service
from app.services.auth.verify_service import verify_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_user(user: UserSignUp, cognito: Cognito = Depends(get_cognito)):
    return signup_service(user, cognito)


@auth_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user(user: UserVerify, cognito: Cognito = Depends(get_cognito)):
    return verify_service(user, cognito)


@auth_router.post("/signin", status_code=status.HTTP_200_OK)
async def signin_user(user: UserSignIn, cognito: Cognito = Depends(get_cognito)):
    return signin_service(user, cognito)
