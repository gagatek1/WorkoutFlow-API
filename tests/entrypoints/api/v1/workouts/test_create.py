import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProfileModelFactory


@pytest.mark.usefixtures("db")
class TestCreateWorkoutEndpoint:
    def test_creates_workout_for_caller(self, client: TestClient, tokens: Tokens) -> None:
        ProfileModelFactory.create()

        response = client.post(
            "/api/v1/workouts", json={"name": "Push", "date": "2026-03-01"}, headers=tokens.of("alice")
        )

        assert response.status_code == 201
        assert response.json()["date"] == "2026-03-01"
        assert client.get("/api/v1/profiles/me", headers=tokens.of("alice")).json()["workout_quantity"] == 1

    def test_caller_without_profile_is_404(self, client: TestClient, tokens: Tokens) -> None:
        assert client.post("/api/v1/workouts", json={"name": "Push"}, headers=tokens.of("ghost")).status_code == 404

    @pytest.mark.parametrize(
        "body", [{"name": ""}, {}, {"name": "Push", "date": "yesterday"}, {"name": "Push", "owner_id": "bob"}]
    )
    def test_rejects_invalid_body(self, client: TestClient, tokens: Tokens, body: dict[str, object]) -> None:
        assert client.post("/api/v1/workouts", json=body, headers=tokens.of("alice")).status_code == 422
