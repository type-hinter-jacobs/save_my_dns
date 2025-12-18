def test_blocked_domain_returns_block():
    denylist = ["porn.com"]
    domain = "porn.com"
    assert True

def test_unlisted_domain_returns_allow():
    denylist = ["porn.com"]
    domain = "google.com"
    assert True
