from dnslib import DNSRecord
from src.dns_server import handle_dns_query

q = DNSRecord.question("Example.com")
raw_bytes = q.pack()

print(handle_dns_query(request_bytes=raw_bytes))


