# save_my_dns

My vision to create a DNS blocking/allowing program to create a safer websurfing environment for youth or anyone for that matter. The motivation for creating the program is due to a rise in pornography exposure and addiction across the world.


## -> THIS PROJECT DOES NOT MODIFY DNS SETTINGS AND ONLY BINDS TO "127.0.0.1". <-


# Project Lifecycle

## Stage 1: Rule Engine

-> Normalise domain names

-> Exact and subdomain matching

-> Unit tests


## Stage 2: DNS Parsing

-> Parse DNS query bytes

-> Extract qname from parsed bytes and normalise domain name


## Stage 3: DNS Decision Handler

-> BLOCK response: NXDOMAIN (rcode == 3)

-> ALLOW response: forward to upstream

-> Upstream failure: SERVFAIL (rcode == 2)


## Stage 4: Local UDP Server

-> Bind local host on high port - 5300

## How to run locally

-> Start server: **src/dns_server.py**

-> Start client: **tests/send_udp_query_local.py**
