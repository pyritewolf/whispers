import pytest

import alembic.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from db.base_model import BaseModel
from config import settings
from main import app


engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    alembic.config.main(argv=["upgrade", "head"])


@pytest.fixture(autouse=True)
def setup():
    client = TestClient(app)
    yield client


@pytest.fixture()
def db():
    session = SessionLocal()
    yield session
    session.close()
    for tbl in reversed(BaseModel.metadata.sorted_tables):
        if not tbl.schema:
            engine.execute(tbl.delete())
