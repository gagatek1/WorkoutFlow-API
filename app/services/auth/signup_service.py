import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.models.user_profile import UserProfile
from app.schemas.auth import UserSignUp


def signup_service(user: UserSignUp, cognito: Cognito, db):
    try:
        response = cognito.user_signup(user)

        create_user_profile_model = UserProfile(
            first_name=user.first_name,
            last_name=user.last_name,
            user_id=response["UserSub"],
        )

        db.add(create_user_profile_model)
        db.commit()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "UsernameExistsException":
            raise HTTPException(
                status_code=409, detail="An account with the given email already exists"
            )
        else:
            raise HTTPException(status_code=500, detail=e.response["Error"]["Code"])
    else:
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            content = {
                "message": "User created successfully",
                "sub": response["UserSub"],
            }
            return JSONResponse(content=content, status_code=201)
