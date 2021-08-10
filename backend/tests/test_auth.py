from sqlalchemy.orm import Session

from users import models as user_models


def test_onboarding_no_token(setup, db: Session):
    db.add(
        user_models.User(
            email="finarfin@arafinwe.com",
            password="coolfirstageharper",
            username="finarfin",
            recovery_token="original_token",
        )
    )
    db.commit()
    response = setup.post("/api/auth/onboard", json={"token": None},)
    print(response.json())
    assert response.status_code == 422


def test_onboarding_wrong_token(setup, db: Session):
    db.add(
        user_models.User(
            email="finarfin@arafinwe.com",
            password="coolfirstageharper",
            username="finarfin",
            recovery_token="original_token",
        )
    )
    response = setup.post("/api/auth/onboard", json={"token": "weird_token"},)
    assert response.status_code == 422


def test_onboarding(setup, db: Session):
    token = "safe-token"
    db_user = user_models.User(
        email="finarfin@arafinwe.com",
        password="coolfirstageharper",
        username="finarfin",
        recovery_token=token,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    assert db_user.recovery_token == token
    response = setup.post("/api/auth/onboard", json={"token": token},)
    assert response.status_code == 200
    db.refresh(db_user)
    assert db_user.recovery_token is None
