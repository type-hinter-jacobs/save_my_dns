from dnslib import DNSRecord
from src.dns_server import handle_dns_query

q = DNSRecord.question("porn.com")
raw_bytes = q.pack()
resp_bytes = handle_dns_query(raw_bytes)
resp = DNSRecord.parse(resp_bytes)
print(resp.header.rcode)