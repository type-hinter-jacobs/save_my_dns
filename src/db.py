from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
import os


DATABASE_URL = os.environ.get("SAVE_MY_DNS_DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)