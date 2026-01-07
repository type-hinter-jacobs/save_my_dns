def evaluate_domain(domain, denylist):
  # convert list elements to lowercase and strip whitespaces
  denylist = [d.strip().lower() for d in denylist]
  # convert string to all lowercase letters
  domain = domain.strip().lower()

  for blocked_domain in denylist:
    # if domain present in the denylist list return BLOCK
    if domain == blocked_domain:
      return "BLOCK"
    # if domain of subdomain is present in the denylist list return BLOCK
    elif domain.endswith("." + blocked_domain):
      return "BLOCK"
  # if domain not present in the denylist list return ALLOW
  return "ALLOW"
    
