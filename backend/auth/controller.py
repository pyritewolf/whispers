from typing import Optional

from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi import HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2

from config import settings
from security import create_jwt_token
from exceptions import CREDENTIALS_EXCEPTION, get_pydanticlike_error
from mailing import MailingService
from auth import schemas
from users import schemas as user_schemas
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


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="api/auth")


def handle_register(db: Session, user: schemas.Register) -> user_schemas.UserOut:
    db_user = crud.create(db=db, user=user)
    token = create_jwt_token(
        {"id": db_user.id}, settings.RESET_PASSWORD_EXPIRATION_SECONDS
    )
    url = f"{settings.CLIENT_URL}/onboarding?token={token}"
    db_user = crud.update(db=db, db_obj=db_user, obj_in={"recovery_token": token})

    succesfully_sent = MailingService.get_instance().send(
        template="register.html.jinja2",
        to=db_user.email,
        variables={"url": url, "username": db_user.username},
        subject="Welcome to Whispers!",
    )

    if not succesfully_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=get_pydanticlike_error(
                "user", "We couldn't send you your registration email. Try again?",
            ),
        )

    return db_user
