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

# from src.rules import evaluate_domain

# DNS POC configuration
BIND_HOST = "127.0.0.1"
BIND_PORT = 5353

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
