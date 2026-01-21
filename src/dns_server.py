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

from dnslib import DNSRecord
from src.rules import evaluate_domain
from src.dns_parsing import extract_domain_from_query
from src.dns_forwarding import forward_to_upstream
import socket


# DNS POC configuration
BIND_HOST = "127.0.0.1"
BIND_PORT = 5300

# list containg domain names that should be blocked
DENYLIST = ["porn.com"]


def handle_dns_query(request_bytes: bytes) -> bytes:
    """
    Handle a single DNS request

    Input:
      - request_bytes: raw UDP payload containing a DNS query

    Output:
      - response_bytes: raw UDP payload containing a DNS response
    """
    domain = extract_domain_from_query(request_bytes=request_bytes)
    decision = evaluate_domain(domain=domain, denylist=DENYLIST)
    print(f"{domain} -> {decision}")
    if decision == "BLOCK":
        request_record = DNSRecord.parse(request_bytes)
        response_record = request_record.reply()
        response_record.header.rcode = 3
        response_bytes = response_record.pack()
        return response_bytes
    else:
        try:
            return forward_to_upstream(request_bytes=request_bytes)
        except (socket.timeout, OSError):
            request_record = DNSRecord.parse(request_bytes)
            response_record = request_record.reply()
            response_record.header.rcode = 2
            response_bytes = response_record.pack()
            return response_bytes



def run_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.bind((BIND_HOST, BIND_PORT))

    print("Server started, waiting for UDP packets...")
    print(f"Listening on ({BIND_HOST}:{BIND_PORT})")

    while True:
        try:
            print("Waiting for query...")
            data, addr = udp_socket.recvfrom(4096)
            print(f"Received {len(data)} bytes from {addr}")
            response_bytes = handle_dns_query(request_bytes=data)
            print(f"Sending {len(response_bytes)} bytes back to {addr}")
            udp_socket.sendto(response_bytes, addr)
        except Exception as e:
            print(f"Error handling request from {addr}: {e}")


if __name__ == "__main__":
    run_server()
