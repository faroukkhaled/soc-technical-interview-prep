# Networking and traffic analysis

### Q: Describe the TCP three-way handshake and what a SYN scan looks like.
- domain: network
- level: 1
- keywords: SYN, SYN-ACK, ACK, half-open, RST
A: Client sends SYN, server replies SYN-ACK, client sends ACK. A SYN scan sends SYN to many ports and never completes the handshake (half-open), so logs show many SYNs and RSTs from one source to many ports or hosts.

### Q: Which ports and protocols should every analyst know?
- domain: network
- level: 1
- keywords: 22, 53, 80, 443, 445, 3389, 88, 389
A: 22 SSH, 25 SMTP, 53 DNS, 80 HTTP, 88 Kerberos, 110 POP3, 123 NTP, 135 RPC, 139 and 445 SMB, 143 IMAP, 389 LDAP, 443 HTTPS, 636 LDAPS, 1433 MSSQL, 3306 MySQL, 3389 RDP, 5985 and 5986 WinRM.

### Q: What is beaconing and how do you find it?
- domain: network
- level: 2
- keywords: jitter, destination, timer, variance
A: Malware calling home on a timer. Group connections by source, destination and process, compute the gaps, and look for low variance (a small coefficient of variation) with small jitter, plus low data volume and an uncommon destination. False positives: update checkers, monitoring agents, NTP.

### Q: How can DNS be abused by attackers and how do you detect it?
- domain: network
- level: 2
- keywords: tunnelling, DGA, TXT, entropy
A: DNS tunnelling encodes data in subdomains, DGAs generate many random domains, and TXT records can carry commands. Detect long or high-entropy labels, many unique subdomains under one domain, high NXDOMAIN rates, unusual TXT volume, and hosts bypassing the internal resolver.

### Q: What is the difference between a proxy, a firewall and a WAF?
- domain: network
- level: 1
- keywords: proxy, firewall, WAF, layer 7, web application
A: A firewall filters by address, port and state (layers 3 and 4, or more in next-gen firewalls). A proxy brokers client requests and can inspect and log web use. A WAF protects a web application at layer 7 against attacks like SQL injection and XSS.

### Q: What would you look for in a PCAP of a suspected infection?
- domain: network
- level: 2
- keywords: DNS, HTTP, user agent, follow stream, export
A: Start with conversations and protocol hierarchy, DNS queries, HTTP requests and user agents, TLS server names, and large uploads. Follow streams, export objects, and pull IOCs (IPs, domains, URLs, hashes) to search elsewhere.

### Q: How does a man-in-the-middle attack work on a local network, and how do you prevent it?
- domain: network
- level: 2
- keywords: ARP spoofing, gateway, TLS, 802.1X
A: ARP spoofing makes victims send traffic to the attacker as if it were the gateway. Prevent with dynamic ARP inspection, port security and 802.1X, and rely on TLS with certificate validation so intercepted traffic is useless.

### Q: What is lateral movement and which protocols are involved?
- domain: network
- level: 2
- keywords: SMB, RDP, WinRM, PsExec, WMI
A: Moving from one compromised host to others. Common methods: SMB with admin shares and PsExec, RDP, WinRM and PowerShell remoting, WMI and DCOM, scheduled tasks and remote services. Detect with type 3 and type 10 logons from unusual sources, new services (7045), and one account touching many hosts.
