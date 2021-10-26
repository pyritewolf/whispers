from typing import Optional, Dict
from urllib.parse import urlencode

import requests
import jwt
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi import HTTPException, status, Depends
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2

from config import settings
from schemas import BaseSchema
from db.session import get_session
from security import create_jwt_token, verify_password, get_hashed_password
from exceptions import CREDENTIALS_EXCEPTION, get_pydanticlike_error
from mailing import MailingService
from auth import schemas
from users import schemas as user_schemas, models
from users.controller import crud


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        authorization = False
        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param
        if cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise CREDENTIALS_EXCEPTION
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="api/auth/signin")


async def handle_register(db: Session, user: schemas.Register) -> user_schemas.UserOut:
    db_user = await crud.create(db=db, user=user)
    token = create_jwt_token(
        {"id": db_user.id}, settings.RESET_PASSWORD_EXPIRATION_SECONDS
    )
    url = f"{settings.CLIENT_URL}/onboarding?token={token}"
    new_user = user_schemas.UserOut.from_orm(
        crud.update(db=db, db_obj=db_user, obj_in={"recovery_token": token})
    )
    succesfully_sent = MailingService.get_instance().send(
        template="register.html.jinja2",
        to=new_user.email,
        variables={"url": url, "username": new_user.username},
        subject="Welcome to Whispers!",
    )
    if not succesfully_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=get_pydanticlike_error(
                "user",
                "We couldn't send you your registration email. Try again?",
            ),
        )
    return new_user


async def handle_onboarding(db: Session, token: str) -> None:
    db_user = await crud.get_by(db, "recovery_token", token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=get_pydanticlike_error(
                "token",
                "This link is invalid!",
            ),
        )
    crud.update(db=db, db_obj=db_user, obj_in={"recovery_token": None})


async def handle_password_recovery(db: Session, email: str) -> None:
    db_user = await crud.get_by(db, "email", email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=get_pydanticlike_error(
                "email", "Oops! Something went wrong. Try again?"
            ),
        )
    token = create_jwt_token(
        {"id": db_user.id}, settings.RESET_PASSWORD_EXPIRATION_SECONDS
    )
    crud.update(db=db, db_obj=db_user, obj_in={"recovery_token": token})
    new_password_url = f"{settings.CLIENT_URL}/new_password?token={token}"
    password_recovery_url = f"{settings.CLIENT_URL}/password_recovery"
    succesfully_sent = MailingService.get_instance().send(
        template="password_recovery.html.jinja2",
        to=db_user.email,
        variables={
            "new_password_url": new_password_url,
            "username": db_user.username,
            "password_recovery_url": password_recovery_url,
        },
        subject="Forgot your password? 😱",
    )
    if not succesfully_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=get_pydanticlike_error(
                "email", "Oops! Something went wrong. Try again?"
            ),
        )
    return None


async def handle_set_new_password(db: Session, data: schemas.NewPassword) -> None:
    db_user = await crud.get_by(db, "recovery_token", data.token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=get_pydanticlike_error(
                "password",
                "This link is invalid! Restart the password recovery",
            ),
        )
    db_user.password = get_hashed_password(data.password)
    db_user.recovery_token = None
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


async def authenticate_user(
    db: Session, user_identifier: str, password: str
) -> user_schemas.UserOut:
    user = await crud.get_by(db, "email", user_identifier)
    if not user:
        user = await crud.get_by(db, "username", user_identifier)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_pydanticlike_error("auth", "Wrong user or password, pal"),
        )
    return user_schemas.UserOut.from_orm(user)


async def get_token_contents(schema: BaseSchema, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=["HS512"])
        return schema.parse_obj(payload)
    except:  # noqa: E722
        return None
    return None


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
) -> user_schemas.UserIn:
    token_data = await get_token_contents(schemas.UserToken, token=token)
    if token_data is None:
        token_data = await get_token_contents(schemas.ChatToken, token=token)
        if token_data is None:
            raise CREDENTIALS_EXCEPTION
        user = await crud.get_by(db, "email", token_data.email)
    else:
        user = await crud.get_by(db, "id", token_data.id)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user_schemas.UserIn.from_orm(user)


async def _get_google_tokens(
    db: Session, user: user_schemas.UserIn, request_args: Dict[str, str]
) -> models.User:
    request_args.update(
        {
            "client_id": settings.GOOGLE_OAUTH_CLIENT,
            "client_secret": settings.GOOGLE_OAUTH_SECRET,
        }
    )
    response = requests.post(
        "https://accounts.google.com/o/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=urlencode(request_args),
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=get_pydanticlike_error(
                "oauth",
                "Something went wrong while fetching your tokens from Google.",
            ),
        )
    response_json = response.json()
    tokens = schemas.GoogleAuthTokens.parse_obj(response_json)
    token_data = {
        "google_auth_token": tokens.access_token,
    }
    if tokens.refresh_token:
        token_data["google_refresh_token"] = tokens.refresh_token
    user = await crud.get_by(db, "id", user.id)
    return crud.update(
        db=db,
        db_obj=user,
        obj_in=token_data,
    )


async def auth_with_google(
    db: Session, user: user_schemas.UserIn, code: str
) -> user_schemas.UserOut:
    auth_completion = {
        "code": code,
        "redirect_uri": f"{settings.CLIENT_URL}/oauth/google/callback",
        "grant_type": "authorization_code",
    }
    db_user = await _get_google_tokens(db, user, auth_completion)
    return user_schemas.UserOut.from_orm(db_user)


async def refresh_google_tokens(
    db: Session, user: user_schemas.UserIn
) -> user_schemas.UserIn:
    auth_completion = {
        "refresh_token": user.google_refresh_token,
        "grant_type": "refresh_token",
    }
    db_user = await _get_google_tokens(db, user, auth_completion)
    return user_schemas.UserIn.from_orm(db_user)


async def _get_twitch_tokens(
    db: Session, user: user_schemas.UserIn, request_args: Dict[str, str]
) -> models.User:
    request_args.update(
        {
            "client_id": settings.TWITCH_OAUTH_CLIENT,
            "client_secret": settings.TWITCH_OAUTH_SECRET,
        }
    )
    response = requests.post(
        "https://id.twitch.tv/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=urlencode(request_args),
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=get_pydanticlike_error(
                "oauth",
                "Something went wrong while fetching your tokens from Twitch.",
            ),
        )
    response_json = response.json()
    tokens = schemas.TwitchAuthTokens.parse_obj(response_json)
    token_data = {
        "twitch_auth_token": tokens.access_token,
    }
    if tokens.refresh_token:
        token_data["twitch_refresh_token"] = tokens.refresh_token
    user = await crud.get_by(db, "id", user.id)
    return crud.update(
        db=db,
        db_obj=user,
        obj_in=token_data,
    )


async def auth_with_twitch(
    db: Session, user: user_schemas.UserIn, code: str
) -> user_schemas.UserOut:
    auth_completion = {
        "code": code,
        "redirect_uri": f"{settings.CLIENT_URL}/oauth/twitch/callback",
        "grant_type": "authorization_code",
    }
    db_user = await _get_twitch_tokens(db, user, auth_completion)
    return user_schemas.UserOut.from_orm(db_user)


async def refresh_twitch_tokens(
    db: Session, user: user_schemas.UserIn
) -> user_schemas.UserIn:
    auth_completion = {
        "refresh_token": user.twitch_refresh_token,
        "grant_type": "refresh_token",
    }
    db_user = await _get_twitch_tokens(db, user, auth_completion)
    return user_schemas.UserIn.from_orm(db_user)
