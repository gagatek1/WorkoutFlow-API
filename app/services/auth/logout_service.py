import boto3
import botocore
from fastapi import HTTPException

from app.core.cognito import Cognito
from app.schemas.auth import UserLogout


def logout_service(data: UserLogout, cognito: Cognito):
    try:
        response = cognito.logout(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NotAuthorizedException":
            raise HTTPException(status_code=401, detail="Invalid access token")
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        return response
