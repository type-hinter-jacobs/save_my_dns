from dnslib import DNSRecord
from src.dns_parsing import extract_domain_from_query

# Create a fake DNS query packet for a known domain
q = DNSRecord.question("Example.com")
raw_bytes = q.pack()

print(extract_domain_from_query(raw_bytes))