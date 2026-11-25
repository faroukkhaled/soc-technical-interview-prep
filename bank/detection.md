# Detection engineering and threat hunting

### Q: What is MITRE ATT&CK used for?
- domain: detection
- level: 1
- keywords: tactics, techniques, coverage, map, adversary
A: A knowledge base of adversary tactics (the goal) and techniques (the method). SOCs map detections to techniques, find coverage gaps, plan hunts, and describe attacker behaviour in a shared language.

### Q: What is Sigma?
- domain: detection
- level: 2
- keywords: YAML, convert, rule
A: A vendor-neutral YAML format for detection rules (selections, conditions, log source, ATT&CK tags) that converts into queries for Splunk, Elastic, Sentinel and others. It makes rules shareable and testable.

### Q: How do you build and test a new detection?
- domain: detection
- level: 3
- keywords: hypothesis, false positive, tune
A: Start from a hypothesis or technique, find the telemetry, write the rule, generate the attack in a lab (Atomic Red Team), confirm it fires, run it against historical data to estimate false positives, tune with allow-lists and context, document triage steps, and review its performance regularly.

### Q: How do you reduce alert fatigue?
- domain: detection
- level: 2
- keywords: tune, context, severity
A: Remove or tune noisy rules, add asset and user context for severity, group related alerts into incidents, automate enrichment, track false positive rate per rule, and retire rules nobody acts on.

### Q: What is threat hunting and how is it different from alert triage?
- domain: detection
- level: 2
- keywords: hypothesis, proactive, alert, triage
A: Hunting is proactive and hypothesis driven: you search for attacker behaviour that did not alert. Triage is reactive: you investigate an alert that fired. Good hunts end as new detections.

### Q: Give an example hunt for living-off-the-land activity.
- domain: detection
- level: 3
- keywords: certutil, mshta, rare, baseline
A: Hypothesis: attackers use built-in binaries to avoid malware detection. Query process creation for certutil with urlcache or decode, mshta or regsvr32 with remote URLs, and rare parent and child pairs compared against a baseline (for example Office or WMI starting cmd and PowerShell). Review hits with the user and host context.

### Q: What is the difference between signature, anomaly and behaviour-based detection?
- domain: detection
- level: 2
- keywords: signature, anomaly, behaviour, known, baseline
A: Signatures match known-bad patterns (precise but evaded easily). Anomaly detection flags deviation from a baseline (finds new things, noisy). Behaviour-based detection looks for attacker actions such as credential access or persistence, which are harder to change.

### Q: How would you measure how good your SOC is?
- domain: detection
- level: 3
- keywords: false positive rate, coverage, escalation
A: Mean time to detect and respond, mean time to acknowledge, false positive rate per rule, ATT&CK coverage, percentage of alerts triaged within SLA, escalation accuracy, and findings from purple team exercises.
