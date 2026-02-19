from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.repository.denylist import SQLAlchemyDenylistRepository
from src.models import Base
import os


def init_db(engine):
    """
    - initialisation function that creates tables at startup
    - can be called multiple times, safely
    """
    Base.metadata.create_all(engine)
    return None

def build_engine(db_url: str | None = None):
    """
    create and return a SQLAlchemy Engine bound to the passed database URL
    """
    DATABASE_URL = os.environ.get("SAVE_MY_DNS_DATABASE_URL")

    if db_url is None:
        if DATABASE_URL is None:
            db_url = "sqlite:///data/save_my_dns.db"
        else:
            db_url = DATABASE_URL
    engine = create_engine(url=db_url)
    return engine

def build_session_factory(engine):
    """
    create and return a SQLAlchemy session factory bound to the passed engine
    """
    session_factory = sessionmaker(bind=engine)
    return session_factory


def build_repo(session_factory):
    """
    create and return a SQLAlchemyDenylistRepository object using the passed session factory
    """
    return SQLAlchemyDenylistRepository(session_factory)