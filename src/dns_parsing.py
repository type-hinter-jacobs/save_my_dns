"""
DNS parsing helpers

Next step:
- Use dnslib to parse incoming DNS query bytes
- Extract the queried domain name (qname) as a normalized string
"""

def extract_domain_from_query(request_bytes: bytes) -> str:
    """
    Given raw DNS request bytes, return the queried domain name.

    Planned dnslib approach (to implement locally):
      1) Parse bytes into a DNSRecord
      2) Read qname from the question section
      3) Convert to a string domain
      4) Normalise string (strip + lowercase)
    """
    raise NotImplementedError("Domain extraction not implemented yet.")
