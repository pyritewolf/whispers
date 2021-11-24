from urllib.parse import urlencode
import json

from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import settings
from db.session import get_session
from security import create_jwt_token
from auth.schemas import Register, Token, PasswordRecovery, NewPassword
from users.schemas import UserOut, UserAuthed, UserIn
from auth import controller


router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(
    user: Register,
    db: Session = Depends(get_session),
):
    new_user = await controller.handle_register(db=db, user=user)
    return new_user


@router.post("/onboard")
async def onboard(
    data: Token,
    db: Session = Depends(get_session),
) -> None:
    await controller.handle_onboarding(db=db, token=data.token)
    return None


@router.post("/signin", response_model=UserAuthed)
async def sign_in(
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


@router.post("/password_recovery")
async def password_recovery(
    data: PasswordRecovery,
    db: Session = Depends(get_session),
) -> None:
    await controller.handle_password_recovery(db=db, email=data.email)
    return None


@router.post("/new_password")
async def new_password(
    data: NewPassword,
    db: Session = Depends(get_session),
) -> None:
    await controller.handle_set_new_password(db=db, data=data)
    return None


@router.get("/signout")
async def sign_out(
    current_user: UserIn = Depends(controller.get_current_user),
):
    response = JSONResponse({}, status_code=status.HTTP_200_OK)
    response.delete_cookie("Authorization")
    return response


@router.get("/google", response_class=RedirectResponse)
def start_auth_with_google(
    request: Request,
    user=Depends(controller.get_current_user),
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


@router.get("/twitch", response_class=RedirectResponse)
def start_auth_with_twitch(
    request: Request,
    user=Depends(controller.get_current_user),
):
    claims = {
        "email": user.email,
    }

    twitch_auth_params = {
        "client_id": settings.TWITCH_OAUTH_CLIENT,
        "redirect_uri": f"{settings.CLIENT_URL}/oauth/twitch/callback",
        "response_type": "code",
        "scope": "chat:edit chat:read channel:moderate",
        "access_type": "offline",
        "claims": json.dumps(claims),
        # To add nonce and state for security later on
    }
    return RedirectResponse(
        url=f"https://id.twitch.tv/oauth2/authorize?{urlencode(twitch_auth_params)}"
    )


@router.post("/twitch/callback", response_model=UserOut)
async def complete_auth_with_twitch(
    data: Token,
    user=Depends(controller.get_current_user),
    db: Session = Depends(get_session),
) -> UserOut:
    db_user = await controller.auth_with_twitch(db, user, data.token)
    return UserOut.from_orm(db_user)
