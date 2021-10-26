from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as DBEnum
from sqlalchemy.ext.hybrid import hybrid_property

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
    chat_embed_secret = Column(String)
    google_auth_token = Column(String)
    google_refresh_token = Column(String)
    twitch_auth_token = Column(String)
    twitch_refresh_token = Column(String)

    @hybrid_property
    def has_auth(self) -> bool:
        return self.has_youtube_auth or self.has_twitch_auth

    @hybrid_property
    def has_youtube_auth(self) -> bool:
        return (
            self.google_auth_token is not None and self.google_refresh_token is not None
        )

    @hybrid_property
    def has_twitch_auth(self) -> bool:
        return (
            self.twitch_auth_token is not None and self.twitch_refresh_token is not None
        )
