def evaluate_domain(domain, denylist):
  # convert list elements to lowercase and strip whitespaces
  denylist = [domain.strip().lower() for domain in denylist]
  # convert string to all lowercase letters
  domain = domain.strip().lower()

  for blocked_domain in denylist:
    # if domain present in the denylist list return BLOCK
    if domain == blocked_domain:
      return "BLOCK"
    # if domain of subdomain is present in the denylist list return BLOCK
    else if domain.endswith("." + blocked_domain):
      return "BLOCK"
    # if domain not present in the denylist list return ALLOW
    else:
      return "ALLOW"
