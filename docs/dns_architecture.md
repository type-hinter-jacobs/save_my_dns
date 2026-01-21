-> DNS server runs locally

-> Listens on high port (53)

-> For ALLOW queries, bytes are forwarded to upstream DNS (1.1.1.1:53) via UDP with timeout

-> On upstream failure return SERVFAIL (rcode 2)

-> Make use of the rule engine for decisions, if BLOCK return NXDOMAIN (rcode 3)

-> Targeted testing only

-> No changes/configurations to system DNS settings
