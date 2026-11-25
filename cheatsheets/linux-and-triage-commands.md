# Handy commands

## Linux triage
```
last -a; lastb | head           # logins and failed logins
journalctl -u ssh --since today # SSH service log
ss -tulpn                       # listening sockets and owning process
ps auxf                         # process tree
crontab -l; ls /etc/cron.*      # scheduled jobs
find / -perm -4000 -type f 2>/dev/null   # SUID binaries
grep 'Failed password' /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr | head
```

## Windows triage
```
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625} -MaxEvents 50
Get-Process | Sort CPU -desc | Select -First 10
netstat -ano | findstr ESTABLISHED
schtasks /query /fo LIST /v
Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
```

## Decode a PowerShell -EncodedCommand (Linux)
```
echo 'SQBFAFgA...' | base64 -d | iconv -f UTF-16LE -t UTF-8
```

## Hashing a file
```
sha256sum file      # Linux
Get-FileHash file   # PowerShell
```
