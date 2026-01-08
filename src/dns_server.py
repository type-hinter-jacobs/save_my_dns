"""
Purpose of the DNS POC:

- Run a minimal local DNS responder that receives DNS queries
- Extracts the requested domain name
- Applies the existing rule engine: evaluate_domain(domain, denylist)
- Responds differently for ALLOW vs BLOCK
- Logs the decision (domain -> ALLOW/BLOCK)


Port it will be listening on:

- POC will be local-only (bind to 127.0.0.1)
- Use a high port first (e.g., 5353) to avoid admin privileges
"""

from src.rules import evaluate_domain
# from dnslib import ...

# DNS POC configuration
BIND_HOST = "127.0.0.1"
BIND_PORT = 5353

# list containg domain names that should be blocked
DENYLIST = ["porn.com"]

def handle_dns_query(request_bytes: bytes) -> bytes:
    """
    Handle a single DNS request

    Input:
      - request_bytes: raw UDP payload containing a DNS query

    Output:
      - response_bytes: raw UDP payload containing a DNS response

    Planned logic (next step with dnslib):
      1) Parse request_bytes into a DNSRecord
      2) domain = extract_domain_from_query(request_bytes)
      3) decision = evaluate_domain(domain, DENYLIST)
      4) If decision == "BLOCK": build NXDOMAIN response
      5) Else: (POC) build a minimal "allowed" response strategy (defined later)
      6) Return response_bytes
    """
    raise NotImplementedError("DNS handler not implemented yet (dnslib step next).")
    

def run_server():
    """
    POC entrypoint
    - will start listening on (BIND_HOST, BIND_PORT)
    - will receive DNS queries
    - will call evaluate_domain()
    - and send back DNS responses
    """
    raise NotImplementedError("DNS server not implemented yet.")


if __name__ == "__main__":
    run_server()
