from dnslib import DNSRecord

def extract_domain_from_query(request_bytes: bytes) -> str:
    qname = str(DNSRecord.parse(request_bytes).questions[0].qname)
    if qname.endswith("."):
        qname = qname[:-1]
    qname = qname.lower().strip()
    return qname

