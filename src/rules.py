# Rule implementation will go here

def evaluate_domain(domain, denylist):
  # convert string to all lowercase letters
  domain = domain.strip().lower()
  # if domain present in the denylist list return BLOCK
  if domain in denylist:
    return "BLOCK"
  #if domain not present in the denylist list return ALLOW
  else:
    return "ALLOW"
