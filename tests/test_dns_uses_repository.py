from src.repository.denylist import SQLAlchemyDenylistRepository
from dnslib import DNSRecord
from src.dns_server import handle_dns_query


def test_blocked_domain_returns_nxdomain_via_repository(session_factory):
    repo = SQLAlchemyDenylistRepository(session_factory)
    repo.add("porn.com")

    query = DNSRecord.question("porn.com")
    raw_bytes = query.pack()
    response_bytes = handle_dns_query(request_bytes=raw_bytes, repo=repo)
    resp = DNSRecord.parse(response_bytes)
    assert resp.header.rcode == 3

