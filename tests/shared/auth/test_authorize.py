import pytest

from app.shared.auth.authorize import authenticate, authorize_user
from app.shared.clients.cognito import CognitoClient
from app.shared.errors import UnauthenticatedError
from tests.fixtures.api import CognitoUsers


class TestAuthorizeUser:
    def test_caller_id_is_the_cognito_sub(self, cognito_users: CognitoUsers, cognito: CognitoClient) -> None:
        token = cognito_users.sign_in("a@x.io")
        attributes = {a["Name"]: a["Value"] for a in cognito.get_user(token)["UserAttributes"]}

        with authorize_user({"authorization": f"Bearer {token}"}) as user:
            assert user.id == attributes["sub"]

    def test_user_without_sub_is_rejected(self, cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(cognito, "get_user", lambda _: {"Username": "alice", "UserAttributes": []})

        with pytest.raises(UnauthenticatedError):
            authenticate("Bearer token")

    @pytest.mark.usefixtures("cognito")
    @pytest.mark.parametrize("header", [None, "", "Bearer", "Basic abc", "Bearer not-a-token"])
    def test_rejects_missing_or_invalid_header(self, header: str | None) -> None:
        with pytest.raises(UnauthenticatedError):
            authenticate(header)
