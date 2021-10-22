from typing import Union, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from exceptions import get_pydanticlike_error
from db.generic_crud import CRUDBase
from auth import schemas as auth_schemas
from users import models, schemas
from security import get_hashed_password, create_jwt_token


class CRUDUser(CRUDBase[models.User, auth_schemas.Register, schemas.UserOut]):
    async def get_by(
        self, db: Session, field: str, value: Union[str, int]
    ) -> Optional[models.User]:
        condition = getattr(models.User, field) == value
        if field in ["email", "username"]:
            condition = func.lower(getattr(models.User, field)) == value.lower()
        return db.query(models.User).filter(condition).one_or_none()

    def get_chat_token(self, email: str):
        return create_jwt_token({"email": email})

    async def refresh_chat_token(
        self, db: Session, user: schemas.UserIn
    ) -> schemas.UserOut:
        db_user = await self.get_by(db, "email", user.email)
        db_user.chat_embed_secret = self.get_chat_token(user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return schemas.UserOut.from_orm(db_user)

    async def create(self, db: Session, user: auth_schemas.Register) -> models.User:
        pre_existing_user = await self.get_by(db, "email", user.email)
        if pre_existing_user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=get_pydanticlike_error(
                    "email", "Yikes, that email is already in use",
                ),
            )
        pre_existing_user = await self.get_by(db, "username", user.username)
        if pre_existing_user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=get_pydanticlike_error(
                    "username", "Oh no! Someone beat you to that username",
                ),
            )
        user_dict = user.dict(exclude_unset=True)
        user_dict.pop("confirm_password")
        db_user = models.User(
            **user_dict,
            password=get_hashed_password(user_dict.pop("password", "")),
            chat_embed_secret=self.get_chat_token(user.email),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


crud = CRUDUser(models.User)
