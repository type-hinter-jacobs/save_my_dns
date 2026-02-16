import pytest
from src.repository.denylist import SQLAlchemyDenylistRepository
from src.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.app import app
from src.api.repo_provider import get_repo


@pytest.fixture()
def db_url(tmp_path):
    db_file = tmp_path / "test.db"
    return f"sqlite:///{db_file}"

@pytest.fixture()
def engine(db_url):
    db_engine = create_engine(db_url)
    return db_engine

@pytest.fixture()
def session_factory(engine):
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

@pytest.fixture()
def override_get_repo(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)

    def override():
        return repo

    app.dependency_overrides[get_repo] = override
    try:
        yield repo
    finally:
        app.dependency_overrides.clear()