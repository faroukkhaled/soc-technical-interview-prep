# Linux, web and cloud basics

### Q: Which Linux logs do you check first for a suspicious SSH login?
- domain: linux
- level: 1
- keywords: auth.log, secure, last, journalctl, failed password
A: /var/log/auth.log (Debian) or /var/log/secure (RHEL) for Accepted and Failed password lines, plus last, lastb and journalctl -u ssh. Look for brute force followed by a success and logins from new sources.

### Q: What are common Linux persistence methods?
- domain: linux
- level: 2
- keywords: cron, systemd, authorized_keys, bashrc, ld.so.preload
A: Cron jobs, systemd services and timers, SSH authorized_keys, shell profile files (.bashrc), ld.so.preload, new users or sudoers entries, and SUID binaries.

### Q: What is SQL injection and how do you spot it in logs?
- domain: web
- level: 1
- keywords: union select, quotes, parameter, error, prepared statements
A: Untrusted input changes a database query. In web logs look for quotes, UNION SELECT, comments, sleep() and error responses in parameters. Prevent with prepared statements, input validation and least-privilege database accounts.

### Q: What is XSS and what are its types?
- domain: web
- level: 1
- keywords: stored, reflected, DOM, script, encoding
A: Cross-site scripting runs attacker script in a victim's browser. Stored (saved on the server), reflected (in the request) and DOM-based. Prevent with output encoding, a Content Security Policy and HttpOnly cookies.

### Q: What is the difference between authentication and authorisation, and what is IDOR?
- domain: web
- level: 2
- keywords: authentication, authorisation, IDOR
A: Authentication proves who you are, authorisation decides what you can do. IDOR is an authorisation flaw where changing an identifier in a request (account_id=1001 to 1002) exposes someone else's data.

### Q: What is the OWASP Top 10?
- domain: web
- level: 1
- keywords: broken access control, injection, awareness
A: A regularly updated list of the most critical web application risks, such as broken access control, cryptographic failures and injection. It is an awareness document and a common baseline for testing.

### Q: How do you detect risky activity in cloud or SaaS accounts?
- domain: cloud
- level: 2
- keywords: audit log, MFA, impossible travel
A: Review sign-in and audit logs for impossible travel, legacy authentication, MFA changes, new OAuth app consent, mailbox forwarding rules, and API key or role creation. Alert on privileged role changes and disabled logging.

### Q: What are symmetric and asymmetric encryption, and what is hashing?
- domain: fundamentals
- level: 1
- keywords: symmetric, asymmetric, hash, key, one-way
A: Symmetric uses one shared key (AES, fast). Asymmetric uses a key pair (RSA, ECC) for key exchange and signatures. A hash is a one-way fixed-size fingerprint (SHA-256) used for integrity, and passwords should be stored with a slow salted hash such as bcrypt or Argon2.
