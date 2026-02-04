from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.repository.exceptions import DomainAlreadyBlocked, DomainNotFound
from src.models import BlockedDomain


class SQLAlchemyDenylistRepository:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def add(self, domain):
        session = None
        try:
            new_entry = BlockedDomain.create(domain=domain)
            session = self._session_factory()
            session.add(new_entry)
            session.commit()
        except IntegrityError:
            if session is not None:
                session.rollback()
            raise DomainAlreadyBlocked()
        finally:
            if session is not None:
                session.close()

    def remove(self, domain):
        session = None
        try:
            domain = BlockedDomain.normalise_domain(raw=domain)
            session = self._session_factory()
            query = select(BlockedDomain).where(BlockedDomain.domain == domain)
            row = session.scalars(query).first()
            if row is not None:
                session.delete(row)
                session.commit()
            else:
                raise DomainNotFound()
        finally:
            if session is not None:
                session.close()

    def is_blocked(self, domain):
        session = None
        try:
            domain = BlockedDomain.normalise_domain(raw=domain)
            session = self._session_factory()
            query = select(BlockedDomain).where(BlockedDomain.domain == domain, BlockedDomain.enabled.is_(True))
            row = session.scalars(query).first()
            if row is not None:
                return True
            else:
                return False
        finally:
            if session is not None:
                session.close()

    def set_enabled(self, domain, enabled):
        session = None
        try:
            domain = BlockedDomain.normalise_domain(raw=domain)
            session = self._session_factory()
            query = select(BlockedDomain).where(BlockedDomain.domain == domain)
            row = session.scalars(query).first()
            if row is not None:
                row.enabled = enabled
                session.commit()
            else:
                raise DomainNotFound()
        finally:
            if session is not None:
                session.close()

