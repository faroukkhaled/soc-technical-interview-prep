# Banking and fraud

### Q: Why do banks need a SOC?
- domain: banking
- level: 1
- keywords: regulation, fraud, account takeover, insider, compliance
A: Banks are high-value targets with strict regulation. The SOC monitors for fraud and account takeover, insider misuse, malware and phishing against staff and customers, and provides evidence for compliance.

### Q: How would you detect account takeover in online banking?
- domain: banking
- level: 2
- keywords: new device, password reset, new payee
A: Chain the signals: login from a new device or country, failed attempts beforehand, password reset or MFA change, new payee added, then a transfer much larger than the customer's history. Individually weak signals become critical in sequence.

### Q: What is credential stuffing and how is it different from brute force?
- domain: banking
- level: 2
- keywords: leaked, reuse, many accounts
A: Credential stuffing tries leaked username and password pairs against many accounts, relying on password reuse. Brute force tries many passwords against one account. Stuffing shows many distinct accounts failing from one or several sources, with a low failure count per account.

### Q: What is structuring (smurfing)?
- domain: banking
- level: 2
- keywords: threshold, reporting, just below
A: Splitting a large amount into several transfers just under a reporting threshold to avoid scrutiny. Detect repeated amounts just below the limit from one customer or into one beneficiary in a short window.

### Q: What is a money mule and what pattern do they create?
- domain: banking
- level: 2
- keywords: fan-in, fan-out, receive, forward
A: An account that receives and quickly forwards illicit funds. Typical pattern: many incoming payments from unrelated sources (fan-in), then fast withdrawal or onward transfer (fan-out).

### Q: What insider threat signals would a bank SOC monitor?
- domain: banking
- level: 2
- keywords: mass viewing, access, working hours, exports
A: Mass viewing of customer records, access outside working hours or to accounts without a case, access to VIP or staff accounts, large exports or uploads, USB use, and access by staff who have given notice. Handle discreetly with HR and compliance.

### Q: What regulations or standards come up in banking security?
- domain: banking
- level: 2
- keywords: PCI DSS, ISO 27001, GDPR, central bank
A: PCI DSS for card data, ISO 27001 for management systems, SWIFT Customer Security Programme for payment messaging, data protection law such as GDPR or local equivalents, and central bank cyber regulations. Check which apply in your country.

### Q: What is the difference between SMS OTP, TOTP and phishing-resistant MFA?
- domain: banking
- level: 2
- keywords: SMS, TOTP, FIDO2, phishing, SIM swap
A: SMS OTP can be intercepted (SIM swap) or phished. TOTP codes from an app are better but still phishable in real time. FIDO2 or passkeys bind authentication to the real site, so they resist phishing.
