import boto3
import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.schemas.auth import UserForgotPassword


def forgot_password_service(data: UserForgotPassword, cognito: Cognito):
    try:
        cognito.forgot_password(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "UserNotFoundException":
            raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        return JSONResponse(
            content={"message": "Password reset code sent"}, status_code=200
        )
