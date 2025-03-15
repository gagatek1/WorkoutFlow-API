from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
