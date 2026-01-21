import socket

UPSTREAM_DNS_HOST = "1.1.1.1"
UPSTREAM_DNS_PORT = 53
UPSTREAM_TIMEOUT_SEC = 2.0

def forward_to_upstream(request_bytes: bytes) -> bytes:
    """
    1. open UDP socket
    2. set timeout if necessary
    3. send request bytes to upstream (host, port)
    4. receive response bytes
    5. return response bytes
    6. on timeout raise an error
    """
    # Create UDP socket
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    with sock:
        sock.settimeout(UPSTREAM_TIMEOUT_SEC)
        # Send data
        sock.sendto(request_bytes, (UPSTREAM_DNS_HOST, UPSTREAM_DNS_PORT))
        # Receive response
        data, addr = sock.recvfrom(4096)
        return data




