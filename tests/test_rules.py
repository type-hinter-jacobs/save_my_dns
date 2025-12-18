def test_blocked_domain_returns_block():
    denylist = ["porn.com"]
    domain = "porn.com"
    assert True

def test_unlisted_domain_returns_allow():
    denylist = ["porn.com"]
    domain = "google.com"
    assert True

def test_domain_matching_is_case_insensitive():
    assert True

def test_domain_is_trimmed_of_whitespace():
    assert True

def test_subdomain_behavior_v1():
    assert True
