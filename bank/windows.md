# Windows and Active Directory

### Q: Which Windows event IDs do you use most for logon investigations?
- domain: windows
- level: 1
- keywords: 4624, 4625, 4634, 4648, logon type
A: 4624 successful logon, 4625 failed logon, 4634 or 4647 logoff, 4648 logon with explicit credentials, 4672 special privileges assigned. Always read the logon type: 2 interactive, 3 network, 10 remote interactive (RDP).

### Q: What do logon types 2, 3, 4, 5, 7, 9, 10 and 11 mean?
- domain: windows
- level: 2
- keywords: interactive, network, batch, service, unlock, RDP, cached
A: 2 interactive (console), 3 network (SMB, mapped drives), 4 batch (scheduled task), 5 service, 7 unlock, 9 NewCredentials (runas /netonly), 10 RemoteInteractive (RDP), 11 CachedInteractive (cached domain credentials). Type 3 from one source to many hosts suggests lateral movement. Type 10 from the internet is a red flag.

### Q: How would you detect Kerberoasting?
- domain: windows
- level: 2
- keywords: 4769, RC4, 0x17, service account
A: Event 4769 (Kerberos service ticket request) with ticket encryption type 0x17 (RC4) for user service accounts rather than machine accounts, and many requests from one source in a short time. Reduce noise by excluding krbtgt and accounts ending with $. Mitigate with long random service account passwords or gMSA and AES-only.

### Q: How would you detect DCSync?
- domain: windows
- level: 3
- keywords: 4662, replication, 1131f6aa, domain controller, DS-Replication-Get-Changes
A: Event 4662 where the properties include the DS-Replication-Get-Changes GUIDs (1131f6aa-9c07-11d1-f79f-00c04fc2dcd2 and 1131f6ad-...) and the subject is not a domain controller machine account. Also watch network traffic: DRSUAPI replication calls from a non-DC.

### Q: What is Pass-the-Hash and what traces does it leave?
- domain: windows
- level: 2
- keywords: NTLM, hash, 4624, type 3
A: Authenticating with an NTLM hash instead of the password. Traces: 4624 type 3 with NTLM authentication from workstations to servers, logon type 9 with seclogo process on the source, unusual admin accounts across many hosts. Mitigate with LAPS, disabling local admin reuse, Credential Guard and restricting NTLM.

### Q: What is a Golden Ticket and how might you spot one?
- domain: windows
- level: 3
- keywords: krbtgt, TGT, 4768, lifetime, forged
A: A forged TGT signed with the krbtgt account hash, giving domain-wide access. Signs: service ticket requests (4769) without a preceding TGT request (4768), TGT lifetimes beyond policy, RC4 tickets in an AES environment, accounts that do not exist. Response: reset krbtgt twice.

### Q: How would you investigate a suspicious PowerShell alert?
- domain: windows
- level: 2
- keywords: parent, command line, 4104, network, persistence
A: Check the parent process and user, read the full command line, decode any -EncodedCommand (UTF-16LE base64), look at script block log 4104, find network connections (Sysmon 3) and files written (Sysmon 11), then check persistence (Run keys, scheduled tasks, WMI) and other hosts with the same pattern.

### Q: Name common Windows persistence mechanisms.
- domain: windows
- level: 2
- keywords: scheduled task, service, WMI, startup folder
A: Run and RunOnce registry keys, scheduled tasks, new services, the Startup folder, WMI event subscriptions, DLL search order hijacking, Winlogon helper keys, and new local or domain accounts. Sysmon 13 (registry), 11 (file), 19-21 (WMI), and Security 4698 and 7045 cover most.

### Q: What is Sysmon and which events matter most?
- domain: windows
- level: 1
- keywords: process creation, network, process access, registry
A: A Sysinternals service that logs detailed host activity to the Windows event log. Key events: 1 process creation, 3 network connection, 7 image load, 8 CreateRemoteThread, 10 process access (LSASS), 11 file create, 13 registry value set, 19-21 WMI, 22 DNS query.

### Q: How do you detect credential dumping from LSASS?
- domain: windows
- level: 2
- keywords: LSASS, GrantedAccess, 0x1010, procdump, comsvcs
A: Sysmon event 10 where TargetImage is lsass.exe and GrantedAccess includes memory read rights such as 0x1010 or 0x1410, excluding known security tools. Also process creation of procdump with lsass, or rundll32 with comsvcs.dll MiniDump. Mitigate with Credential Guard and LSA protection (RunAsPPL).

### Q: Which event shows the audit log was cleared?
- domain: windows
- level: 1
- keywords: 1102, 104, clear, defence evasion
A: Security event 1102 means the Security log was cleared. System event 104 covers other logs. Log clearing is defence evasion (T1070.001) and almost never benign on a production host.

### Q: What is Group Policy and why do attackers care?
- domain: windows
- level: 2
- keywords: GPO, SYSVOL, push
A: Group Policy applies settings to domains, OUs and computers. Whoever can edit a GPO can push scripts, scheduled tasks or security setting changes to many machines at once, which makes it a favourite for ransomware deployment. Monitor GPO edits (5136, 5137) and SYSVOL changes.

### Q: What is the difference between local and domain accounts, and why does LAPS matter?
- domain: windows
- level: 2
- keywords: local, domain, LAPS, password, unique
A: Local accounts exist on one machine, domain accounts are managed by AD. If every machine has the same local admin password, one stolen hash gives access everywhere. LAPS gives each machine a unique, rotated local admin password.
