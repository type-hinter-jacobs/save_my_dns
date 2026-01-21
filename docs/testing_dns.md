PURPOSE

-> Test the DNS core POC locally

-> Focus on safe and reversible testing



SCOPE OF TESTING

-> Local machine/host only

-> No system wide DNS changes

-> No API service

-> No persistence



SAFETY RULES

-> No permanent changes to system DNS settings

-> Ensure a way to revert DNS changes/configurations

-> Know how to stop DNS process if unexpected behaviour occurs



Testing Tools

-> Cmd Prompt

-> nslookup did not work for DNS testing. A python UDP query client was created and used to test DNS

-> Python runtime



TEST SCENARIOS

-> Create scenarios to test against the rule engine



IDEAL RESULT

-> DNS processes run without crashes

-> Blocked domain behave differently from allowed domains (blocked domains return "non-existent domain" or NXDOMAIN type failure) 
