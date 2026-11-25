# MITRE ATT&CK enterprise tactics in order

1. Reconnaissance (TA0043)
2. Resource Development (TA0042)
3. Initial Access (TA0001): phishing T1566, valid accounts T1078, exploit public-facing app T1190
4. Execution (TA0002): PowerShell T1059.001, user execution T1204
5. Persistence (TA0003): Run keys T1547.001, scheduled task T1053.005, WMI subscription T1546.003
6. Privilege Escalation (TA0004)
7. Defence Evasion (TA0005): clear logs T1070.001, obfuscated files T1027
8. Credential Access (TA0006): LSASS T1003.001, Kerberoasting T1558.003, brute force T1110
9. Discovery (TA0007): account T1087, remote system T1018
10. Lateral Movement (TA0008): remote services T1021, SMB admin shares T1021.002
11. Collection (TA0009)
12. Command and Control (TA0011): application layer protocol T1071, ingress tool transfer T1105
13. Exfiltration (TA0010)
14. Impact (TA0040): inhibit system recovery T1490, data encrypted for impact T1486

Tip: in an interview, name the tactic (the goal) first, then a technique ID (the method).
