# SOC analyst questions and short answers

**What is the difference between an event, an alert and an incident?**
An event is any logged occurrence. An alert is an event or pattern a rule flags for review. An incident is a confirmed security event that needs a response.

**Walk me through how you triage an alert.**
Read the rule and context, validate against raw logs, check the asset and user, look for related activity, decide true or false positive, set severity, then contain or escalate and document.

**What is a false positive and how do you reduce them?**
An alert on benign activity. Tune thresholds, add allowlists for known-good behaviour, add context (asset criticality, user role), and review rule performance regularly.

**Explain the phases of incident response.**
Preparation, detection and analysis, containment, eradication, recovery, lessons learned (NIST 800-61).

**What is MITRE ATT&CK used for?**
A knowledge base of adversary tactics and techniques. SOCs use it to map detections, find coverage gaps and describe attacker behaviour.

**What is an IOC versus an IOA?**
An IOC is evidence of compromise (hash, IP, domain). An IOA focuses on attacker behaviour, such as Office spawning PowerShell.

**How would you detect Kerberoasting?**
Event 4769 with RC4 encryption (0x17) for service accounts, many requests from one source in a short time.

**How would you investigate a suspicious PowerShell alert?**
Check parent process, command line and encoding, script block log 4104, network connections, persistence and the user context.

**What Windows event IDs do you know?**
4624/4625 logon success/failure, 4688 process creation, 4720 account created, 4732 group member added, 4769 Kerberos service ticket, 1102 log cleared, Sysmon 1 process, 3 network, 10 process access, 13 registry.

**What is Sysmon?**
A Sysinternals service that logs detailed process, network, file and registry activity to the Windows event log.

**What is a SIEM and what does it do?**
It collects and normalizes logs, correlates them, alerts and supports search and reporting.

**How do you handle a suspected compromised host?**
Isolate it, preserve evidence, scope the activity, remove persistence, reset credentials, rebuild if needed.

**Why do banks need a SOC?**
High-value targets and strict regulation: fraud, account takeover, insider risk, and compliance monitoring.

**Tell me about a project you did.**
Use the Banking SOC Simulation or the AD & Sysmon lab: describe the goal, what you built, a detection you wrote, and what you learned.
