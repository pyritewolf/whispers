from typing import Optional
from pydantic import SecretStr

from schemas import BaseSchema
from users.models import Role


class UserBase(BaseSchema):
    email: str
    role: Role = Role.user
    username: str


class UserOut(UserBase):
    id: int
    has_youtube_auth: bool = False


class UserAuthed(UserBase):
    id: int
    token: str


class UserIn(UserBase):
    id: int
    password: SecretStr
    recovery_token: Optional[str]
    has_youtube_auth: bool = False
    google_auth_token: Optional[str]
    google_refresh_token: Optional[str]


class UserUpdate(UserBase):
    id: int
