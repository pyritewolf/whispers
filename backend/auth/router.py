from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import settings
from db.session import get_session
from security import create_jwt_token
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


@router.post("/signin", response_model=UserOut)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = controller.authenticate_user(db, form_data.username, form_data.password)
    token = create_jwt_token({"id": user.id}, settings.COOKIE_EXPIRATION_SECONDS)
    response = JSONResponse(user.dict(by_alias=True), status_code=200)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        expires=settings.COOKIE_EXPIRATION_SECONDS,
    )
    return response
