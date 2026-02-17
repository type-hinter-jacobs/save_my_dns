from dnslib import DNSRecord
import socket

HOST = "127.0.0.1"
PORT = 5300

query = DNSRecord.question("google.com")
raw_bytes = query.pack()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)

sock.sendto(raw_bytes, (HOST, PORT))
data, addr = sock.recvfrom(4096)

response = DNSRecord.parse(data)
print("rcode", response.header.rcode)
print("answers:", len(response.rr))