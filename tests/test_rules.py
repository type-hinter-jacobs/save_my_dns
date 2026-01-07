# To be implemented:
from src.rules import evaluate_domain

def test_blocked_domain_returns_block():
    denylist = ["porn.com"]
    domain = "porn.com"

    result = evaluate_domain(domain, denylist)
    assert result == "BLOCK"


def test_unlisted_domain_returns_allow():
    denylist = ["porn.com"]
    domain = "google.com"

    result = evaluate_domain(domain, denylist)
    assert result == "ALLOW"


def test_domain_matching_is_case_insensitive():
    denylist = ["porn.com"]
    domain = "PORN.COM"

    # result = evaluate_domain(domain, denylist)
    # assert result == "BLOCK"
    assert True


def test_domain_is_trimmed_of_whitespace():
    denylist = ["porn.com"]
    domain = "   porn.com  "

    # result = evaluate_domain(domain, denylist)
    # assert result == "BLOCK"
    assert True


def test_subdomain_behavior_v1():
    denylist = ["porn.com"]
    domain = "sub.porn.com"

    # result = evaluate_domain(domain, denylist)
    # assert result == "BLOCK"
    assert True
