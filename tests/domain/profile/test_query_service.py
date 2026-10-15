import pytest

from app.domain.profile.exceptions import ProfileNotFoundError
from app.domain.profile.query_service import ProfileQueryService
from tests.fixtures.factories import ProfileModelFactory


@pytest.mark.usefixtures("db")
class TestProfileQueryService:
    def test_get_profile(self) -> None:
        ProfileModelFactory.create()

        assert ProfileQueryService().get_profile("alice").first_name == "Alice"

    def test_get_missing_raises_not_found(self) -> None:
        with pytest.raises(ProfileNotFoundError):
            ProfileQueryService().get_profile("ghost")
