from datetime import UTC, datetime

import pytest

from app.shared.pagination import InvalidCursorError, decode_cursor, encode_cursor

CREATED_AT = datetime(2026, 1, 1, tzinfo=UTC)


class TestPagination:
    def test_round_trip(self) -> None:
        assert decode_cursor(encode_cursor(CREATED_AT, "id-1")) == (CREATED_AT, "id-1")

    def test_no_cursor(self) -> None:
        assert decode_cursor(None) is None

    @pytest.mark.parametrize(
        "cursor",
        ["not-base64!", "x" * 3000, encode_cursor(CREATED_AT, "id")[:-4], "WzEsMl0="],
    )
    def test_rejects_tampered_cursor(self, cursor: str) -> None:
        with pytest.raises(InvalidCursorError):
            decode_cursor(cursor)
