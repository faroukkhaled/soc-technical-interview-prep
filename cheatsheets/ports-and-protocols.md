# Ports and protocols

| Port | Protocol | Note |
|------|----------|------|
| 20 / 21 | FTP | Cleartext |
| 22 | SSH / SFTP | |
| 23 | Telnet | Cleartext, should not exist |
| 25 / 465 / 587 | SMTP | Mail submission |
| 53 | DNS | UDP and TCP, tunnelling target |
| 67 / 68 | DHCP | |
| 80 / 443 | HTTP / HTTPS | |
| 88 | Kerberos | |
| 110 / 995 | POP3 / POP3S | |
| 123 | NTP | |
| 135 | RPC endpoint mapper | WMI, DCOM |
| 137-139 | NetBIOS | |
| 143 / 993 | IMAP / IMAPS | |
| 161 / 162 | SNMP | |
| 389 / 636 | LDAP / LDAPS | |
| 445 | SMB | Lateral movement |
| 514 | Syslog | |
| 1433 / 3306 / 5432 | MSSQL / MySQL / PostgreSQL | |
| 3389 | RDP | Exposed RDP is a top ransomware entry |
| 5985 / 5986 | WinRM | PowerShell remoting |
| 4444 | Metasploit default listener | Common C2 default |
