# Windows and Sysmon event IDs

## Security log
| ID | Meaning | Why it matters |
|----|---------|----------------|
| 1102 | Audit log cleared | Defence evasion |
| 4624 | Successful logon | Check logon type and source |
| 4625 | Failed logon | Brute force, stuffing |
| 4634 / 4647 | Logoff | Session length |
| 4648 | Logon with explicit credentials | runas, lateral movement |
| 4662 | Operation on a directory object | DCSync with replication GUIDs |
| 4672 | Special privileges assigned | Admin logons |
| 4688 | Process created (needs command-line auditing) | Execution |
| 4698 | Scheduled task created | Persistence |
| 4720 | User account created | Backdoor accounts |
| 4728 / 4732 / 4756 | Member added to global / local / universal group | Privilege escalation |
| 4768 | Kerberos TGT requested | Golden ticket baseline |
| 4769 | Kerberos service ticket requested | Kerberoasting (RC4 = 0x17) |
| 4771 / 4776 | Kerberos pre-auth failed / NTLM validation | Password spraying |
| 5136 / 5137 | Directory object modified / created | GPO and AD changes |
| 7045 (System) | New service installed | PsExec, persistence |

## Sysmon
| ID | Meaning |
|----|---------|
| 1 | Process creation |
| 2 | File creation time changed |
| 3 | Network connection |
| 6 | Driver loaded |
| 7 | Image (DLL) loaded |
| 8 | CreateRemoteThread |
| 10 | Process access (LSASS) |
| 11 | File created |
| 12 / 13 / 14 | Registry object / value / rename |
| 17 / 18 | Pipe created / connected |
| 19 / 20 / 21 | WMI filter / consumer / binding |
| 22 | DNS query |
| 25 | Process tampering |

## Logon types
2 interactive, 3 network, 4 batch, 5 service, 7 unlock, 8 network cleartext, 9 new credentials, 10 RDP, 11 cached.
