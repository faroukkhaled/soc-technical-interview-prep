# Fundamentals

### Q: What is the difference between an event, an alert and an incident?
- domain: fundamentals
- level: 1
- keywords: event, alert, incident, rule, response
A: An event is any logged occurrence. An alert is an event or pattern that a rule flags for review. An incident is a confirmed security event that needs a response. Most events never become alerts and most alerts are not incidents.

### Q: Explain the CIA triad with a banking example.
- domain: fundamentals
- level: 1
- keywords: confidentiality, integrity, availability
A: Confidentiality: only the customer and authorised staff see an account (attack: data theft). Integrity: balances and transfers cannot be altered undetected (attack: tampering with a payment instruction). Availability: online banking is up when customers need it (attack: DDoS or ransomware).

### Q: What is a false positive and a false negative, and which is worse?
- domain: fundamentals
- level: 1
- keywords: false positive, false negative, tune
A: A false positive is an alert on benign activity. A false negative is a real attack that raised no alert. False negatives are usually worse because the attack goes unseen, but a flood of false positives causes alert fatigue, which leads to false negatives in practice. Tune thresholds, add allow-lists and context, and measure rule performance.

### Q: What is defence in depth?
- domain: fundamentals
- level: 1
- keywords: layers, prevent, detect, respond
A: Several independent layers of control (network segmentation, endpoint protection, identity controls, logging, backups) so that one failure does not mean compromise. It combines prevent, detect and respond controls.

### Q: What is the principle of least privilege and where does it matter most for a SOC?
- domain: fundamentals
- level: 1
- keywords: admin, service accounts, access, credential
A: Give accounts only the access needed for their job. It limits the blast radius of a stolen credential. The SOC watches privileged and service accounts closely: admin group changes, logons outside normal hours, and service accounts used interactively.

### Q: What is the difference between threat, vulnerability and risk?
- domain: fundamentals
- level: 1
- keywords: threat, vulnerability, risk, likelihood, impact
A: A threat is something that can cause harm (a ransomware group). A vulnerability is a weakness (an unpatched server). Risk is the likelihood that a threat exploits a vulnerability multiplied by the impact.

### Q: What is a SIEM and what does it do?
- domain: fundamentals
- level: 1
- keywords: collect, correlate, alert, search
A: A SIEM collects logs, normalises them to a common schema, correlates events across sources, raises alerts and supports search, dashboards and retention for investigations and compliance. A SOAR adds automated playbooks on top.

### Q: What is the difference between IDS and IPS?
- domain: fundamentals
- level: 1
- keywords: block, inline, passive
A: An IDS watches a copy of traffic (passive) and alerts. An IPS sits inline and can block. Inline placement risks outages from false positives, so IPS rules are tuned more carefully.

### Q: What is an IOC versus an IOA?
- domain: fundamentals
- level: 2
- keywords: hash, IP, domain, behaviour
A: An IOC is evidence of compromise that is often atomic and short-lived (a file hash, IP or domain). An IOA describes attacker behaviour, such as Office spawning PowerShell. IOAs survive tooling changes, IOCs are cheap to evade.

### Q: What is the Pyramid of Pain?
- domain: fundamentals
- level: 2
- keywords: hash, IP, domain, TTP, tools
A: David Bianco's model of how much it hurts an adversary when you detect each indicator type: hash values (trivial), IP addresses, domain names, network and host artefacts, tools, and TTPs (tough). Detections at the top force attackers to change behaviour.
