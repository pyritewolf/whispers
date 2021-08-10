from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_session
from auth.schemas import Register, Token
from users.schemas import UserOut
from auth import controller


router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(
    user: Register, db: Session = Depends(get_session),
):
    return controller.handle_register(db=db, user=user)


@router.post("/onboard")
def onboard(
    data: Token, db: Session = Depends(get_session),
):
    return controller.handle_onboarding(db=db, token=data.token)
