from typing import Dict, Optional

from pydantic import SecretStr
from sqlalchemy.orm import Session

from security import get_hashed_password, create_jwt_token
from users import models as user_models


def seed_user(db: Session, obj: Dict = {}):
    user_dict = {
        "email": "finarfin@arafinwe.com",
        "password": "coolfirstageharper",
        "username": "finarfin",
        "recovery_token": None,
        "chat_embed_secret": "a token",
        **obj,
    }
    user_dict["password"] = get_hashed_password(SecretStr(user_dict["password"]))
    user = user_models.User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_auth_for(user: Optional[user_models.User] = None) -> Dict[str, str]:
    token = "superFakeToken"
    if user is not None:
        token = create_jwt_token({"id": user.id})
    return {"Authorization": f"Bearer {token}"}
