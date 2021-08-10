from typing import Dict

from pydantic import SecretStr
from sqlalchemy.orm import Session

from security import get_hashed_password
from users import models as user_models


def seed_user(db: Session, obj: Dict = {}):
    user_dict = {
        "email": "finarfin@arafinwe.com",
        "password": "coolfirstageharper",
        "username": "finarfin",
        "recovery_token": None,
        **obj,
    }
    user_dict["password"] = get_hashed_password(SecretStr(user_dict["password"]))
    user = user_models.User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
