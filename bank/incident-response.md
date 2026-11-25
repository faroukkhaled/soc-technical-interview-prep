# Incident response

### Q: Explain the phases of incident response.
- domain: ir
- level: 1
- keywords: preparation, detection, containment, eradication, recovery, lessons
A: NIST 800-61: preparation; detection and analysis; containment, eradication and recovery; post-incident activity (lessons learned). The older SANS model splits containment, eradication and recovery into three steps.

### Q: Walk me through how you triage an alert.
- domain: ir
- level: 1
- keywords: validate, context, severity, escalate, document
A: Read the rule and context, validate against raw logs, check the asset and user, look for related activity, decide true or false positive, set severity, then contain or escalate and document the decision and evidence.

### Q: How do you handle a suspected compromised host?
- domain: ir
- level: 2
- keywords: isolate, memory, scope, persistence, credentials, rebuild
A: Isolate it from the network (do not power it off, to keep memory), capture volatile data and disk images, scope the activity and other affected hosts, remove persistence, reset exposed credentials, and rebuild from a known-good image when trust is lost.

### Q: What is the order of volatility?
- domain: ir
- level: 2
- keywords: memory, network, disk, logs, volatile
A: Collect the most volatile first: CPU registers and cache, memory, network connections and routing tables, running processes, disk, remote logs, and archival media.

### Q: What is chain of custody and why does it matter?
- domain: ir
- level: 2
- keywords: evidence, hash, legal
A: A documented record of who collected, handled and stored each piece of evidence, with hashes to prove it was not altered. Without it the evidence may be rejected in legal or disciplinary proceedings.

### Q: How do you respond to a phishing email reported by a user?
- domain: ir
- level: 1
- keywords: headers, URL, attachment, sandbox, block
A: Check sender and headers (SPF, DKIM, DMARC), detonate URLs and attachments in a sandbox, find everyone who received or clicked it, block the sender, domain and URL, remove it from mailboxes, reset credentials of anyone who entered them, and add IOCs to detections.

### Q: A user's account shows a login from a new country. What do you do?
- domain: ir
- level: 2
- keywords: impossible travel, MFA, session, reset, VPN, device
A: Check for impossible travel, known VPN use, new device and MFA outcome. If suspicious, revoke sessions, force a password reset and MFA re-registration, review mailbox rules and recent activity such as forwarding or payee changes, and contact the user on a trusted channel.

### Q: What is ransomware response in the first hour?
- domain: ir
- level: 3
- keywords: isolate, backups, scope, identify, notify
A: Isolate affected hosts and segments, disable compromised accounts, protect backups, identify the strain and scope (shadow copy deletion, mass file renames), preserve evidence, notify management, legal and regulators as required, and decide on payment only through the formal crisis process.

### Q: What goes in an incident report?
- domain: ir
- level: 1
- keywords: timeline, impact, root cause, actions
A: Summary, timeline, affected systems and data, root cause, detection and response actions, indicators, impact, and recommendations. Keep facts separate from assumptions.
