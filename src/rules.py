# Rule implementation will go here

def evaluate_domain(domain, denylist):
  # if domain present in the denylist list return BLOCK
  if domain in denylist:
    return "BLOCK"
  #if domain not present in the denylist list return ALLOW
  else:
    return "ALLOW"
