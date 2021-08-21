from urllib.parse import urlencode

from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import settings
from db.session import get_session
from security import create_jwt_token
from auth.schemas import Register, Token
from users.schemas import UserOut, UserAuthed
from auth import controller


router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(
    user: Register, db: Session = Depends(get_session),
):
    await controller.handle_register(db=db, user=user)


@router.post("/onboard")
def onboard(
    data: Token, db: Session = Depends(get_session),
):
    return controller.handle_onboarding(db=db, token=data.token)


@router.post("/signin", response_model=UserAuthed)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = await controller.authenticate_user(
        db, form_data.username, form_data.password
    )
    token = create_jwt_token({"id": user.id}, settings.COOKIE_EXPIRATION_SECONDS)
    response = JSONResponse(
        {**user.dict(by_alias=True), "token": token}, status_code=200
    )
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        expires=settings.COOKIE_EXPIRATION_SECONDS,
    )
    return response


@router.get("/google", response_class=RedirectResponse)
def start_auth_with_google(
    request: Request, user=Depends(controller.get_current_user),
):
    google_auth_params = {
        "client_id": settings.GOOGLE_OAUTH_CLIENT,
        "redirect_uri": f"{settings.CLIENT_URL}/oauth/google/callback",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/youtube",
        "access_type": "offline",
        "login_hint": user.email,
    }
    return RedirectResponse(
        url=f"https://accounts.google.com/o/oauth2/auth?{urlencode(google_auth_params)}"
    )


@router.post("/google/callback", response_model=UserOut)
async def complete_auth_with_google(
    data: Token,
    user=Depends(controller.get_current_user),
    db: Session = Depends(get_session),
) -> UserOut:
    db_user = await controller.auth_with_google(db, user, data.token)
    return UserOut.from_orm(db_user)
