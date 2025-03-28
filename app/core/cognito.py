import base64
import hashlib
import hmac
from os import getenv

import boto3
from dotenv import load_dotenv

from app.schemas.auth import (
    UserChangePassword,
    UserConfirmForgotPassword,
    UserForgotPassword,
    UserLogout,
    UserRefreshToken,
    UserSignIn,
    UserSignUp,
    UserVerify,
)

load_dotenv()

REGION_NAME = getenv("REGION_NAME")
AWS_COGNITO_APP_CLIENT_ID = getenv("AWS_COGNITO_APP_CLIENT_ID")
AWS_COGNITO_APP_CLIENT_SECRET = getenv("AWS_COGNITO_APP_CLIENT_SECRET")
AWS_COGNITO_USER_POOL_ID = getenv("AWS_COGNITO_USER_POOL_ID")


class Cognito:
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=REGION_NAME)

    @staticmethod
    def _generate_secret_hash(username: str) -> str:
        message = username + AWS_COGNITO_APP_CLIENT_ID
        secret = AWS_COGNITO_APP_CLIENT_SECRET
        digest = hmac.new(
            secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        return base64.b64encode(digest).decode()

    def user_signup(self, user: UserSignUp):
        secret_hash = self._generate_secret_hash(user.email)
        response = self.client.sign_up(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=user.email,
            Password=user.password,
            SecretHash=secret_hash,
        )
        return response

    def verify_account(self, data: UserVerify):
        secret_hash = self._generate_secret_hash(data.email)
        response = self.client.confirm_sign_up(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.confirmation_code,
            SecretHash=secret_hash,
        )

        return response

    def user_signin(self, user: UserSignIn):
        secret_hash = self._generate_secret_hash(user.email)
        response = self.client.initiate_auth(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": user.email,
                "PASSWORD": user.password,
                "SECRET_HASH": secret_hash,
            },
        )
        return response

    def new_token(self, data: UserRefreshToken):
        secret_hash = self._generate_secret_hash(data.user_id)
        response = self.client.initiate_auth(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": data.refresh_token,
                "SECRET_HASH": secret_hash,
            },
        )

        return response

    def change_password(self, data: UserChangePassword):
        response = self.client.change_password(
            PreviousPassword=data.old_password,
            ProposedPassword=data.new_password,
            AccessToken=data.access_token,
        )

        return response

    def forgot_password(self, data: UserForgotPassword):
        secret_hash = self._generate_secret_hash(data.email)
        response = self.client.forgot_password(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=data.email,
            SecretHash=secret_hash,
        )

        return response

    def confirm_forgot_password(self, data: UserConfirmForgotPassword):
        secret_hash = self._generate_secret_hash(data.email)
        response = self.client.confirm_forgot_password(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.confirmation_code,
            Password=data.new_password,
            SecretHash=secret_hash,
        )

        return response

    def logout(self, data: UserLogout):
        response = self.client.global_sign_out(AccessToken=data.access_token)

        return response

    def get_user(self, access_token: str):
        response = self.client.get_user(AccessToken=access_token)

        return response

    def change_user_email(self, access_token: str, new_email: str):
        response = self.client.update_user_attributes(
            AccessToken=access_token,
            UserAttributes=[
                {
                    "Name": "email",
                    "Value": new_email,
                },
            ],
        )

        return response
