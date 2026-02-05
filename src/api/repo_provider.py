from src.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.repository.denylist import SQLAlchemyDenylistRepository

DATABASE_URL = "sqlite:///data/save_my_dns.db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)

def get_repo() -> SQLAlchemyDenylistRepository:
    return SQLAlchemyDenylistRepository(session_factory)
