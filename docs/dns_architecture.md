-> DNS server runs locally

-> Listens on high port (5353)

-> For ALLOW queries, bytes are forwarded to upstream DNS (1.1.1.1:53) via UDP with timeout

-> Make use of the rule engine for decisions, if BLOCK return NXDOMAIN

-> Targeted testing only

-> No changes/configurations to system DNS settings
