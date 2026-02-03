from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base

DATABASE_URL = "sqlite:///data/save_my_dns.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)