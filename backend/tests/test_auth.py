from urllib.parse import urlencode
import pytest

from sqlalchemy.orm import Session

from users.models import User
from tests.utils import seed_user, get_auth_for


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
    "patched_requests", [{"method": "post"}], indirect=["patched_requests"]
)
def test_register_with_used_email(patched_requests, setup, db: Session):
    data = _get_register_data()
    seed_user(db, {"email": data["email"]})
    data["confirm_password"] = f'not-the-same-{data["password"]}'
    response = setup.post("/api/auth/register", json=data)
    assert response.status_code == 422
    user = db.query(User).filter(User.email == data["email"]).one_or_none()
    assert user.username != data["username"]


@pytest.mark.parametrize(
    "patched_requests", [{"method": "post"}], indirect=["patched_requests"]
)
def test_register_with_used_username(patched_requests, setup, db: Session):
    data = _get_register_data()
    seed_user(db, {"username": data["username"]})
    data["confirm_password"] = f'not-the-same-{data["password"]}'
    response = setup.post("/api/auth/register", json=data)
    assert response.status_code == 422
    user = db.query(User).filter(User.username == data["username"]).one_or_none()
    assert user.email != data["email"]


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
    response = setup.post(
        "/api/auth/onboard",
        json={"token": None},
    )
    print(response.json())
    assert response.status_code == 422


def test_onboarding_wrong_token(setup, db: Session):
    seed_user(db, {"recovery_token": "original_token"})
    response = setup.post(
        "/api/auth/onboard",
        json={"token": "weird_token"},
    )
    assert response.status_code == 422


def test_onboarding(setup, db: Session):
    token = "safe-token"
    db_user = seed_user(db, {"recovery_token": token})
    assert db_user.recovery_token == token
    response = setup.post("/api/auth/onboard", json={"token": token})
    assert response.status_code == 200
    db.refresh(db_user)
    assert db_user.recovery_token is None


def test_signout(setup, db: Session):
    db_user = seed_user(db)
    response = setup.get("/api/auth/signout", headers=get_auth_for(db_user))
    assert response.status_code == 200
    assert "set-cookie" in response.headers
    assert response.headers["set-cookie"].startswith('Authorization=""; ')


def test_google_auth_invalid_token(setup, db):
    seed_user(db)
    response = setup.get("/api/auth/google", headers=get_auth_for())
    assert response.status_code == 401


def test_google_auth(setup, db):
    db_user = seed_user(db)
    response = setup.get(
        "/api/auth/google", headers=get_auth_for(db_user), allow_redirects=False
    )
    assert response.status_code == 307


def test_google_auth_callback_invalid_user_token(setup, db):
    seed_user(db)
    response = setup.post("/api/auth/google/callback", headers=get_auth_for())
    assert response.status_code == 401


@pytest.mark.parametrize(
    "patched_requests",
    [{"method": "post", "status_code": 401}],
    indirect=["patched_requests"],
)
def test_google_auth_callback_invalid_google_token(setup, db, patched_requests):
    db_user = seed_user(db)
    response = setup.post(
        "/api/auth/google/callback",
        headers=get_auth_for(db_user),
        json={"token": "whatever"},
    )
    assert response.status_code == 500


@pytest.mark.parametrize(
    "patched_requests",
    [
        {
            "method": "post",
            "response": {
                "access_token": "access",
                "refresh_token": "refresh",
                "expires_in": 1,
                "token_type": "Bearer",
            },
        }
    ],
    indirect=["patched_requests"],
)
def test_google_auth_callback(setup, db, patched_requests):
    db_user = seed_user(db)
    response = setup.post(
        "/api/auth/google/callback",
        headers=get_auth_for(db_user),
        json={"token": "whatever"},
    )
    db.refresh(db_user)
    assert response.status_code == 200
    assert db_user.google_auth_token == "access"
    assert db_user.google_refresh_token == "refresh"


def test_twitch_auth_invalid_token(setup, db):
    seed_user(db)
    response = setup.get("/api/auth/twitch", headers=get_auth_for())
    assert response.status_code == 401


def test_twitch_auth(setup, db):
    db_user = seed_user(db)
    response = setup.get(
        "/api/auth/twitch", headers=get_auth_for(db_user), allow_redirects=False
    )
    assert response.status_code == 307


def test_twitch_auth_callback_invalid_user_token(setup, db):
    seed_user(db)
    response = setup.post("/api/auth/twitch/callback", headers=get_auth_for())
    assert response.status_code == 401


@pytest.mark.parametrize(
    "patched_requests",
    [{"method": "post", "status_code": 401}],
    indirect=["patched_requests"],
)
def test_twitch_auth_callback_invalid_twitch_token(setup, db, patched_requests):
    db_user = seed_user(db)
    response = setup.post(
        "/api/auth/twitch/callback",
        headers=get_auth_for(db_user),
        json={"token": "whatever"},
    )
    assert response.status_code == 500


@pytest.mark.parametrize(
    "patched_requests",
    [
        {
            "method": "post",
            "response": {
                "access_token": "access",
                "refresh_token": "refresh",
                "expires_in": 1,
                "token_type": "Bearer",
            },
        }
    ],
    indirect=["patched_requests"],
)
def test_twitch_auth_callback(setup, db, patched_requests):
    db_user = seed_user(db)
    response = setup.post(
        "/api/auth/twitch/callback",
        headers=get_auth_for(db_user),
        json={"token": "whatever"},
    )
    db.refresh(db_user)
    assert response.status_code == 200
    assert db_user.twitch_auth_token == "access"
    assert db_user.twitch_refresh_token == "refresh"
