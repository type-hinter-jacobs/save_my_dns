import pytest
from src.repository.denylist import SQLAlchemyDenylistRepository
from src.repository.exceptions import DomainAlreadyBlocked, DomainNotFound


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

def test_add_duplicate_domain_raises_domainalreadyblocked(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    repo.add("porn.com")
    with pytest.raises(DomainAlreadyBlocked):
        repo.add("porn.com")

def test_remove_missing_domain_raises_domainnotfound(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    with pytest.raises(DomainNotFound):
        repo.remove("porn.com")

def test_disable_domain_unblocks_it(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    repo.add("porn.com")
    repo.set_enabled("porn.com", False)
    assert repo.is_blocked("porn.com") is False

def test_reenable_domain_blocks_again(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    repo.add("porn.com")
    repo.set_enabled("porn.com", False)
    repo.set_enabled("porn.com", True)
    assert repo.is_blocked("porn.com") is True

def test_set_enabled_missing_domain_raises_domainnotfound(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    with pytest.raises(DomainNotFound):
        repo.set_enabled("porn.com", False)

def test_list_all_returns_domains_sorted_alphabetically_with_enabled_flags(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    repo.add("  yyy.com")
    repo.add("aAa.com  ")
    repo.add("CCc.com")
    repo.set_enabled("ccc.com", False)
    items = repo.list_all()
    domains = [item.domain for item in items]
    assert domains == ["aaa.com", "ccc.com", "yyy.com"]