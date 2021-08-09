import jwt
import bcrypt
from datetime import datetime, timedelta

from pydantic import SecretStr

from config import settings


def create_jwt_token(
    to_encode: dict, expiration_in_seconds: int, algorithm="HS512"
) -> str:
    expire = datetime.utcnow() + timedelta(seconds=int(expiration_in_seconds))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_KEY, algorithm=algorithm)
    return encoded_jwt.decode("utf-8")


def get_hashed_password(password: SecretStr):
    pw = password.get_secret_value().encode("utf8")
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: SecretStr, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.get_secret_value().encode("utf8"),
        hashed_password.encode("utf8"),
    )
