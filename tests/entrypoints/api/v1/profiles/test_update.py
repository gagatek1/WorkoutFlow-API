import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.entrypoints.api.api_gateway_handler import app
from app.entrypoints.api.v1.auth import signup
from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProfileModelFactory

NAMES = {"first_name": "Ala", "last_name": "N"}


@pytest.mark.usefixtures("db")
class TestUpdateProfileEndpoint:
    def test_updates_only_callers_profile(self, client: TestClient, tokens: Tokens) -> None:
        ProfileModelFactory.create()
        ProfileModelFactory.create(user_id="bob", first_name="Bob")

        response = client.put("/api/v1/profiles/me", json=NAMES, headers=tokens.of("alice"))

        assert response.json()["first_name"] == "Ala"
        assert client.get("/api/v1/profiles/me", headers=tokens.of("bob")).json()["first_name"] == "Bob"

    @pytest.mark.usefixtures("cognito")
    def test_account_whose_profile_failed_at_signup_can_recover(
        self, tokens: Tokens, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def database_down(*_: object) -> None:
            raise OperationalError("INSERT", {}, Exception("connection refused"))

        monkeypatch.setattr(signup, "create_profile_handler", database_down)
        client = TestClient(app, raise_server_exceptions=False)
        account = {**NAMES, "email": "c@x.io", "password": "Passw0rd!x"}
        assert client.post("/api/v1/auth/signup", json=account).status_code == 500
        headers = tokens.of("new-user")
        assert client.post("/api/v1/workouts", json={"name": "Push"}, headers=headers).status_code == 404

        assert client.put("/api/v1/profiles/me", json=NAMES, headers=headers).status_code == 200
        assert client.post("/api/v1/workouts", json={"name": "Push"}, headers=headers).status_code == 201

    @pytest.mark.parametrize(
        "body",
        [{"first_name": "", "last_name": "N"}, {"first_name": "A"}, {**NAMES, "total_weight": 9}],
    )
    def test_rejects_invalid_body(self, client: TestClient, tokens: Tokens, body: dict[str, object]) -> None:
        assert client.put("/api/v1/profiles/me", json=body, headers=tokens.of("alice")).status_code == 422
