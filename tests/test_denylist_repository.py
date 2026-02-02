import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
from src.repository.denylist import SQLAlchemyDenylistRepository

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


def test_can_it_open(session_factory):
    session = session_factory()
    session.close()
    assert session is not None

def test_add_domain(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    repo.add("porn.com")
    assert repo.is_blocked("porn.com") is True

def test_is_blocked_returns_false_when_domain_missing(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    assert repo.is_blocked("porn.com") is False