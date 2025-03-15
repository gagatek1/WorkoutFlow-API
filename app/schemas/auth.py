from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    email: EmailStr
    password: str


class UserVerify(BaseModel):
    email: EmailStr
    confirmation_code: str
