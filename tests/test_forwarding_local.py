from dnslib import DNSRecord
from src.dns_server import handle_dns_query

q = DNSRecord.question("google.com")
raw_bytes = q.pack()
resp_bytes = handle_dns_query(request_bytes=raw_bytes)
resp_record = DNSRecord.parse(resp_bytes)
print(resp_record.header.rcode)
print(len(resp_record.rr))