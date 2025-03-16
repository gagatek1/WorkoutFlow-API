from typing import Optional

from pydantic import BaseModel


class Workout(BaseModel):
    name: Optional[str] = None
    date: Optional[str] = None
