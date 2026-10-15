import base64
import hashlib
import hmac
from collections.abc import Callable
from functools import cache
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from app.settings import cognito_settings
from app.shared.errors import ExternalServiceError


class CognitoError(ExternalServiceError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Identity provider error: {code}")


class CognitoClient:
    def __init__(self, client: Any) -> None:
        self._client = client
        self._client_id = cognito_settings.app_client_id
        self._client_secret = cognito_settings.app_client_secret.get_secret_value()
        self._user_pool_id = cognito_settings.user_pool_id

    def secret_hash(self, username: str) -> dict[str, str]:
        if not self._client_secret:
            return {}
        digest = hmac.new(self._client_secret.encode(), (username + self._client_id).encode(), hashlib.sha256).digest()
        return {"SecretHash": base64.b64encode(digest).decode()}

    def _call(self, operation: Callable[..., dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
        try:
            return operation(**kwargs)
        except ClientError as exc:
            raise CognitoError(exc.response.get("Error", {}).get("Code", "Unknown")) from exc
        except BotoCoreError as exc:
            raise CognitoError("Unavailable") from exc

    def sign_up(self, email: str, password: str) -> dict[str, Any]:
        return self._call(
            self._client.sign_up,
            ClientId=self._client_id,
            Username=email,
            Password=password,
            **self.secret_hash(email),
        )

    def confirm_sign_up(self, email: str, code: str) -> None:
        self._call(
            self._client.confirm_sign_up,
            ClientId=self._client_id,
            Username=email,
            ConfirmationCode=code,
            **self.secret_hash(email),
        )

    def initiate_auth(self, flow: str, username: str, parameters: dict[str, str]) -> dict[str, Any]:
        secret = self.secret_hash(username)
        if secret:
            parameters = {**parameters, "SECRET_HASH": secret["SecretHash"]}
        response = self._call(
            self._client.initiate_auth, ClientId=self._client_id, AuthFlow=flow, AuthParameters=parameters
        )
        return response.get("AuthenticationResult") or {}

    def change_password(self, access_token: str, old_password: str, new_password: str) -> None:
        self._call(
            self._client.change_password,
            AccessToken=access_token,
            PreviousPassword=old_password,
            ProposedPassword=new_password,
        )

    def forgot_password(self, email: str) -> None:
        self._call(self._client.forgot_password, ClientId=self._client_id, Username=email, **self.secret_hash(email))

    def confirm_forgot_password(self, email: str, code: str, new_password: str) -> None:
        self._call(
            self._client.confirm_forgot_password,
            ClientId=self._client_id,
            Username=email,
            ConfirmationCode=code,
            Password=new_password,
            **self.secret_hash(email),
        )

    def global_sign_out(self, access_token: str) -> None:
        self._call(self._client.global_sign_out, AccessToken=access_token)

    def get_user(self, access_token: str) -> dict[str, Any]:
        return self._call(self._client.get_user, AccessToken=access_token)

    def update_email(self, access_token: str, email: str) -> None:
        self._call(
            self._client.update_user_attributes,
            AccessToken=access_token,
            UserAttributes=[{"Name": "email", "Value": email}],
        )


@cache
def get_cognito() -> CognitoClient:
    config = Config(connect_timeout=2, read_timeout=5, retries={"mode": "standard", "max_attempts": 2})
    return CognitoClient(boto3.client("cognito-idp", region_name=cognito_settings.region, config=config))
