from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    email: EmailStr
    password: str


class UserVerify(BaseModel):
    email: EmailStr
    confirmation_code: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserRefreshToken(BaseModel):
    user_id: str
    refresh_token: str
