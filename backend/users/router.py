from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_session
from auth.controller import get_current_user
from users import schemas
from users.controller import crud


router = APIRouter()


@router.get("/me/refresh_chat_token")
async def check_if_chat_is_available(
    user: schemas.UserIn = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> schemas.UserOut:
    return await crud.refresh_chat_token(db=db, user=user)
