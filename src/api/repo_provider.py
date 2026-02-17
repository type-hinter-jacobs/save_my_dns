from src.repository.denylist import SQLAlchemyDenylistRepository
from src.wiring import init_db, build_engine, build_session_factory, build_repo


engine = build_engine()
init_db(engine=engine)
session_factory = build_session_factory(engine=engine)

def get_repo() -> SQLAlchemyDenylistRepository:
    return build_repo(session_factory=session_factory)
