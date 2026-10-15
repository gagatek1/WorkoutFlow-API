import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProfileModelFactory


@pytest.mark.usefixtures("db")
class TestGetProfileEndpoint:
    def test_returns_callers_own_profile(self, client: TestClient, tokens: Tokens) -> None:
        ProfileModelFactory.create()
        ProfileModelFactory.create(user_id="bob", first_name="Bob")

        response = client.get("/api/v1/profiles/me", headers=tokens.of("alice"))

        assert response.status_code == 200
        assert response.json() == {
            "id": "alice",
            "first_name": "Alice",
            "last_name": "Smith",
            "total_weight": 0,
            "workout_quantity": 0,
        }

    def test_other_profiles_are_not_addressable(self, client: TestClient, tokens: Tokens) -> None:
        ProfileModelFactory.create(user_id="bob")

        assert client.get("/api/v1/profiles/bob", headers=tokens.of("alice")).status_code == 404

    def test_missing_is_404(self, client: TestClient, tokens: Tokens) -> None:
        assert client.get("/api/v1/profiles/me", headers=tokens.of("ghost")).status_code == 404
