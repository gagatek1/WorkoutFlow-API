import boto3
import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.schemas.auth import UserConfirmForgotPassword


def confirm_forgot_password_service(data: UserConfirmForgotPassword, cognito: Cognito):
    try:
        cognito.confirm_forgot_password(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "CodeMismatchException":
            raise HTTPException(status_code=400, detail="Invalid confirmation code")
        elif e.response["Error"]["Code"] == "ExpiredCodeException":
            raise HTTPException(status_code=400, detail="Confirmation code expired")
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        return JSONResponse(content={"message": "Password changed"}, status_code=200)
