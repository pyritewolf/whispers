from typing import Optional
from datetime import datetime

from pydantic import SecretStr, validator

from schemas import BaseSchema


class Register(BaseSchema):
    email: str
    password: SecretStr
    username: str
    confirm_password: SecretStr

    @validator("confirm_password")
    def check_if_passwords_match(cls, v, values):
        if v != values["password"]:
            raise ValueError("Passwords don't match, buddy!")
        return v


class Token(BaseSchema):
    token: str

    @validator("token", pre=True)
    def check_token_is_present(cls, v):
        if not v:
            raise ValueError("This link is invalid!")
        return v


class PasswordRecovery(BaseSchema):
    email: str


class NewPassword(Token):
    password: SecretStr
    confirm_password: SecretStr

    @validator("confirm_password")
    def check_if_passwords_match(cls, v, values):
        if v != values["password"]:
            raise ValueError("Passwords don't match, buddy!")
        return v


class UserToken(BaseSchema):
    id: int


class ChatToken(BaseSchema):
    email: str
    created_at: datetime


class GoogleAuthTokens(BaseSchema):
    access_token: str
    token_type: str
    expires_in: str
    refresh_token: Optional[str] = None


class TwitchAuthTokens(BaseSchema):
    access_token: str
    token_type: str
    expires_in: str
    refresh_token: Optional[str] = None
