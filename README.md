# Save My DNS

My vision to create a DNS blocking/allowing system is to create a safer websurfing environment for youth or anyone for that matter. The motivation for creating the program is due to a rise in pornography exposure and addiction across the world.

Save My DNS is a local DNS-based content filtering system designed to block specified domains through a live database-driven rule engine. The project aims to explore practical DNS filtering as a mechanism to reduce exposure to harmful content such as pornography by giving administrators full control over domain access.

#### Take NOTE:
- This project does not modify your DNS system settings.
- In its current state it is limited to running locally as it binds only to 127.0.0.1 and runs on a high local port.
- This project is still under development.

## Latest version capabilities
### DNS Engine + Server
- The UDP DNS server is bound to 127.0.0.1:5300 (local computer)
- Raw DNS query bytes are parsed
- Queried domain name gets extracted and normalised (remove whitespace, make lowercase, etc.)
- Subdomain matching
- Returns response codes:
  - NXDOMAIN (rcode == 3) when BLOCKED
  - SERVFAIL (rcode == 2) if upstream FAILS
  - when ALLOWED, forwards to upstream resolver

### System Persistence
- Use SQLite database
- Implement SQLAlchemy ORM models (define database tables)
- The database is accessed through a repository layer instead of directly querying SQLite
- Domain names are normalised before being stored in database ensuring consistent matching
- Domains can be enabled/disbaled without being deleted from database

### Admin API
- Used FastAPI to implement API
- API key for authentication
- API endpoints:
  - GET/blocked-domains
  - POST/blocked-domains
  - PATCH/blocked-domains{domain}
  - DELETE/blocked-domains{domain}
- Use Swagger to access API endpoints

### Tests implementation
- Unit tests
- Integration tests
- API authentication tests

### How to run locally
1. Clone the repository from GitHub
2. Create virtual environment:
    - python -m venv .venv
    - .venv\Scripts\activate
3. Install all dependencies:
   - python -m pip install -e .
4. Create .env file in root folder
5. Add API key to .env file:
   - SAVE_MY_DNS_ADMIN_KEY=add_your_key_here
6. Run the Admin API:
   - python -m uvicorn src.api.app:app --reload --port 8000
7. Access Swagger via http://127.0.0.1:8000/docs link
8. Use your API key in Swagger via the Authorize button 
9. Run DNS server in a second terminal:
   - python -m src.dns_server

### How to demo (ensure Admin API + DNS server is running)
1. Add a blocked domain via Swagger -> POST endpoint
2. Send a DNS query to the blocked domain
3. Observe:
   - BLOCKED -> rcode = 3
   - ALLOWED -> response gets forwarded

### What's Next
- Implementation of Admin UI (User Interface)
- Service Integration
