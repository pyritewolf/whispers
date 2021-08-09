from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as DBEnum

from db import BaseModel


class Role(str, Enum):
    admin = "admin"
    user = "user"


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String)
    role = Column(DBEnum(Role), default=Role.user, nullable=False)
    username = Column(String, nullable=False, unique=True)
    recovery_token = Column(String)
