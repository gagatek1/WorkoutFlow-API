from pydantic import BaseModel

class UserSignUp(BaseModel):
    email: str
    password: str