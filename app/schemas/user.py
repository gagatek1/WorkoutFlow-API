from typing import Optional

from pydantic import BaseModel, EmailStr


class UserEmail(BaseModel):
    email: EmailStr


class User(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
