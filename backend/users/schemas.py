from typing import Optional
from pydantic import SecretStr

from schemas import BaseSchema
from users.models import Role


class UserBase(BaseSchema):
    email: str
    role: Role = Role.user
    username: str
    recovery_token: Optional[str]


class UserOut(UserBase):
    pass


class UserIn(UserBase):
    password: SecretStr


class UserUpdate(UserBase):
    id: int
