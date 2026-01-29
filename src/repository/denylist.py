class SQLAlchemyDenylistRepository:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def add(self, domain):
        raise NotImplementedError

    def is_blocked(self, domain):
        raise NotImplementedError