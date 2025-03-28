from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    first_name: str
    last_name: str
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


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str
    access_token: str


class UserForgotPassword(BaseModel):
    email: EmailStr


class UserConfirmForgotPassword(BaseModel):
    email: EmailStr
    confirmation_code: str
    new_password: str


class UserLogout(BaseModel):
    access_token: str
