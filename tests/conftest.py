import pytest
from src.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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