from urllib.parse import urlencode
import pytest

from sqlalchemy.orm import Session

from users.models import User
from tests.utils import seed_user


def _get_register_data():
    return {
        "email": "gothmog@angband.com",
        "password": "supersafepw",
        "username": "xXx_lordOfBalrogs_xXx",
        "confirm_password": "supersafepw",
    }


def test_login_wrong_password(setup, db: Session):
    user = seed_user(db)
    data = {
        "username": user.email,
        "password": "wild_weird_password",
    }
    response = setup.post(
        "/api/auth/signin",
        data=urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400


def test_login_with_email(setup, db: Session):
    known_password = "coolfirstageharper"
    user = seed_user(db, {"password": known_password})
    data = {
        "username": user.email,
        "password": known_password,
    }
    response = setup.post(
        "/api/auth/signin",
        data=urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200


def test_login_with_username(setup, db: Session):
    known_password = "coolfirstageharper"
    user = seed_user(db, {"password": known_password})
    data = {
        "username": user.username,
        "password": known_password,
    }
    response = setup.post(
        "/api/auth/signin",
        data=urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "patched_requests", [{"method": "post"}], indirect=["patched_requests"]
)
def test_register(patched_requests, setup, db: Session):
    data = _get_register_data()
    response = setup.post("/api/auth/register", json=data)
    assert response.status_code == 200
    user = db.query(User).filter(User.email == data["email"]).one_or_none()
    assert user is not None


@pytest.mark.parametrize(
    "patched_requests", [{"method": "post"}], indirect=["patched_requests"]
)
def test_register_with_wrong_pw(patched_requests, setup, db: Session):
    data = _get_register_data()
    data["confirm_password"] = f'not-the-same-{data["password"]}'
    response = setup.post("/api/auth/register", json=data)
    assert response.status_code == 422
    user = db.query(User).filter(User.email == data["email"]).one_or_none()
    assert user is None


@pytest.mark.parametrize(
    "patched_requests",
    [{"method": "post", "status_code": 400}],
    indirect=["patched_requests"],
)
def test_register_with_failing_email(patched_requests, setup, db: Session):
    data = _get_register_data()
    response = setup.post("/api/auth/register", json=data)
    assert response.status_code == 500
    user = db.query(User).filter(User.email == data["email"]).one_or_none()
    assert user is not None


def test_onboarding_no_token(setup, db: Session):
    seed_user(db, {"recovery_token": "original_token"})
    response = setup.post("/api/auth/onboard", json={"token": None},)
    print(response.json())
    assert response.status_code == 422


def test_onboarding_wrong_token(setup, db: Session):
    seed_user(db, {"recovery_token": "original_token"})
    response = setup.post("/api/auth/onboard", json={"token": "weird_token"},)
    assert response.status_code == 422


def test_onboarding(setup, db: Session):
    token = "safe-token"
    db_user = seed_user(db, {"recovery_token": token})
    assert db_user.recovery_token == token
    response = setup.post("/api/auth/onboard", json={"token": token})
    assert response.status_code == 200
    db.refresh(db_user)
    assert db_user.recovery_token is None
