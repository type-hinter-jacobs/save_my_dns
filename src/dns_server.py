from dnslib import DNSRecord
from src.dns_parsing import extract_domain_from_query
from src.dns_forwarding import forward_to_upstream
from src.repository.denylist import SQLAlchemyDenylistRepository
from src.wiring import init_db, build_engine, build_session_factory, build_repo
import socket
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BIND_HOST = "127.0.0.1"
BIND_PORT = 5300

def handle_dns_query(request_bytes: bytes, repo: SQLAlchemyDenylistRepository) -> bytes:
    domain = extract_domain_from_query(request_bytes=request_bytes)
    blocked = repo.is_blocked(domain=domain)
    print(f"{domain} -> {blocked}")
    if blocked:
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
    udp_socket = None
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        engine = build_engine()
        init_db(engine=engine)
        session_factory = build_session_factory(engine=engine)
        repo = build_repo(session_factory=session_factory)
        udp_socket.bind((BIND_HOST, BIND_PORT))
        udp_socket.settimeout(1.0)
        logger.info("Server started, waiting for UDP packets...")
        logger.info(f"Listening on ({BIND_HOST}:{BIND_PORT})")
    except Exception:
        logger.exception(f"Could not start server")
        return
    try:
        while True:
            addr = None
            try:
                logger.debug("Waiting for query...")
                data, addr = udp_socket.recvfrom(4096)
                logger.debug(f"Received {len(data)} bytes from {addr}")
                response_bytes = handle_dns_query(request_bytes=data, repo=repo)
                logger.debug(f"Sending {len(response_bytes)} bytes back to {addr}")
                udp_socket.sendto(response_bytes, addr)
            except socket.timeout:
                continue
            except Exception:
                logger.exception(f"Error handling request from {addr}")
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    finally:
        if udp_socket is not None:
            udp_socket.close()


if __name__ == "__main__":
    run_server()
