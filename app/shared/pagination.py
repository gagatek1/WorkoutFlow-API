import base64
import binascii
import json
from datetime import datetime

from app.shared.errors import InvalidInputError

MAX_CURSOR_LENGTH = 2048


class InvalidCursorError(InvalidInputError):
    default_message = "Invalid cursor"


def encode_cursor(created_at: datetime, row_id: str) -> str:
    payload = json.dumps([created_at.isoformat(), row_id], separators=(",", ":"))
    return base64.urlsafe_b64encode(payload.encode()).decode()


def decode_cursor(cursor: str | None) -> tuple[datetime, str] | None:
    if cursor is None:
        return None
    try:
        if len(cursor) > MAX_CURSOR_LENGTH:
            raise ValueError
        created_at, row_id = json.loads(base64.urlsafe_b64decode(cursor.encode()))
        if not isinstance(created_at, str) or not isinstance(row_id, str):
            raise ValueError
        return datetime.fromisoformat(created_at), row_id
    except (ValueError, TypeError, binascii.Error) as exc:
        raise InvalidCursorError from exc
