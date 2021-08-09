from typing import Union, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from db.generic_crud import CRUDBase
from auth import schemas as auth_schemas
from users import models, schemas
from security import get_hashed_password


class CRUDUser(CRUDBase[models.User, auth_schemas.Register, schemas.UserOut]):
    def get_by(
        self, db: Session, field: str, value: Union[str, int]
    ) -> Optional[models.User]:
        condition = getattr(models.User, field) == value
        if field in ["email", "username"]:
            condition = func.lower(getattr(models.User, field)) == value.lower()
        return db.query(models.User).filter(condition).one_or_none()

    def create(self, db: Session, user: auth_schemas.Register) -> schemas.UserOut:
        user_dict = user.dict(exclude_unset=True)
        user_dict.pop("confirm_password")
        db_user = models.User(
            **user_dict, password=get_hashed_password(user_dict.pop("password", "")),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


crud = CRUDUser(models.User)
