import pytest
from typing import Dict, Any

import requests
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


@pytest.fixture
def patched_requests(monkeypatch, request):
    method: str = request.param.get("method", "get")
    response: Dict[str, Any] = request.param.get("response", {})
    status_code: int = request.param.get("status_code", 200)

    def mocked_method(uri: str, **kwargs):
        """A method replacing requests[method]
        Returns either a mocked response object (with json method)
        or the default response object if the uri doesn't match
        one of those that have been supplied.
        """
        # create a mocked requests object
        mock = type("MockedReq", (), {})()
        # assign mocked json to requests.json
        mock.json = response
        mock.status_code = status_code
        if status_code != 200:
            mock.error = "something went wrong!"
        # assign obj to mock
        return mock

    # finally, patch requests.get with patched version
    monkeypatch.setattr(requests, method, mocked_method)
