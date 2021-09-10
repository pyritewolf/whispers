from sqlalchemy.orm import Session

from users.schemas import UserOut
from tests.utils import seed_user, get_auth_for


def test_refresh_chat_token_with_no_auth(setup, db: Session):
    seed_user(db)
    response = setup.get("/api/me/refresh_chat_token", headers=get_auth_for())
    assert response.status_code == 401


def test_refresh_chat_token_with(setup, db: Session):
    user = seed_user(db)
    response = setup.get("/api/me/refresh_chat_token", headers=get_auth_for(user))
    assert response.status_code == 200
    user_out = UserOut.parse_obj(response.json())
    assert user.chat_embed_secret != user_out.chat_embed_secret
    db.refresh(user)
    assert user.chat_embed_secret == user_out.chat_embed_secret
