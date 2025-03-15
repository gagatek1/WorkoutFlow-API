import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.schemas.auth import UserChangePassword


def change_password_service(data: UserChangePassword, cognito: Cognito):
    try:
        cognito.change_password(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NotAuthorizedException":
            raise HTTPException(status_code=401, detail="Invalid access token")
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        return JSONResponse(content={"message": "Password changed"}, status_code=200)
