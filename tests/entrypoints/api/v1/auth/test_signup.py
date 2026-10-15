import pytest
from fastapi.testclient import TestClient

from app.domain.profile.query_service import ProfileQueryService

BODY = {"first_name": "Ada", "last_name": "Lovelace", "email": "c@x.io", "password": "Passw0rd!x"}


@pytest.mark.usefixtures("cognito", "db")
class TestSignupEndpoint:
    def test_creates_account_and_profile(self, client: TestClient) -> None:
        response = client.post("/api/v1/auth/signup", json=BODY)

        assert response.status_code == 201
        profile = ProfileQueryService().get_profile(response.json()["sub"])
        assert (profile.first_name, profile.workout_quantity, profile.total_weight) == ("Ada", 0, 0)

    def test_duplicate_is_409(self, client: TestClient) -> None:
        client.post("/api/v1/auth/signup", json=BODY)

        assert client.post("/api/v1/auth/signup", json=BODY).status_code == 409

    @pytest.mark.parametrize("change", [{"password": "short"}, {"first_name": ""}, {"last_name": None}])
    def test_rejects_invalid_body(self, client: TestClient, change: dict[str, object]) -> None:
        assert client.post("/api/v1/auth/signup", json={**BODY, **change}).status_code == 422
