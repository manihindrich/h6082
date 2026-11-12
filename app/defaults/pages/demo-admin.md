// Demo: Ondřej, server administrator at a smaller hosting company (Proxmox cluster, web, databases,
// mail, backups, monitoring). Hostnames and addresses are made up (RFC 5737 documentation ranges).
// Lines starting with // are not shown on the page.

#__ About this board
## 🛡️ Demo use case: a server administrator
![terminal with a log and a server overview](/media/demo-admin.svg)

**Ondřej** looks after eight servers of a smaller hosting company and is on call. The board is his **signpost and first screen during an incident**:

- **in the morning** he goes through the security feeds (CISA, Debian, Ubuntu, SANS ISC). When a fix comes out for a package he has deployed, he adds it to the *Patch plan*.
- **the status of dependencies** (DNS resolvers, Let's Encrypt, registries) is shown by the dots. When a certificate can't be issued, he knows right away whether the problem is on his side or with ACME.
- **during an attack** he doesn't assemble commands from memory: he copies them from the *Incident* block with one click. Highlighted lines are the places where he fills in an IP, PID or path.
- **during an incident** he writes the timeline into the *Working on now* block with ✎, without the editor. The postmortem is then written from it.
- **every server** runs tmux. The shortcuts he doesn't use daily are on a cheat sheet.

# Operations
## `Operations`

##* 🔥 Working on now
**12 Nov 09:40** web-02: rise in 5xx, load 14
**09:46** source: botnet on `/wp-login.php`, ~900 IPs, ban via fail2ban + nft set
**10:05** stable, load 2. Open: why the nginx rate limit didn't kick in

## 🖥️ Servers
| host | role | OS | IP |
|:--|:--|:--|:--|
| pve-01..03 | Proxmox cluster | PVE 8 | 192.0.2.11–13 |
| web-01, web-02 | nginx + PHP-FPM | Debian 12 | 192.0.2.21–22 |
| db-01 | PostgreSQL 16, replica on db-02 | Debian 12 | 192.0.2.31 |
| mail-01 | Postfix, Dovecot, Rspamd | Debian 12 | 192.0.2.41 |
| backup-01 | Proxmox Backup Server | PBS 3 | 192.0.2.51 |

- [Proxmox](https://192.0.2.11:8006) · [Grafana](https://grafana.example.cz) · [Uptime Kuma](https://status.example.cz) · [PBS](https://192.0.2.51:8007)
- [Rspamd](https://mail.example.cz/rspamd/) · [Wiki: runbooks](https://wiki.example.cz/ops)

## 🌐 Dependencies
- [Cloudflare DNS](https://1.1.1.1){check="tcp://1.1.1.1:53"} · resolver 1.1.1.1
- [Quad9](https://quad9.net){check="tcp://9.9.9.9:53"} · backup resolver
- [Let's Encrypt ACME](https://acme-v02.api.letsencrypt.org/directory){.check} [?](When the dot is red, certificates won't renew right now. Certbot will retry on its own.)
- [Debian security](https://security.debian.org){.check} · update mirror
- [Docker Hub registry](https://registry-1.docker.io/v2/){.check} [?](An orange dot with code 401 is fine: the registry is running and just wants a login)
- [GitHub](https://github.com){.check} · deploy keys, CI

## 📊 This server
{{sys cpu mem load disk uptime demo}}

##* 🩹 Patch plan
| when | what | where | status |
|:--|:--|:--|:-:|
| today 22:00 | sudo (USN / DSA) | all | ⏳ |
| Thu 22:00 | kernel + reboot, one node at a time | pve-01..03 | ⏳ |
| Sun 06:00 | PostgreSQL 16.x minor | db-02 → failover → db-01 | 📋 |
| done | openssh | all | ✓ |

> [!warning]- Maintenance window
> Customers are informed 48 h in advance via the status page. Cluster nodes are always rebooted one at a time and only after migrating the VMs (`ha-manager` / live migration).

#++ Incident
## `Incident`

## 🚨 Attack and analysis
> [!danger] Before you delete anything
> Preserve the traces: a VM snapshot, a copy of `/var/log` and a listing of processes and connections. Without them you can't find out how the attacker got in.

### Who hits the web the most
```bash hl_lines="1"
LOG=/var/log/nginx/access.log
# top 20 IPs
awk '{print $1}' "$LOG" | sort | uniq -c | sort -rn | head -20
# requests per minute (peak = start of the attack)
awk '{print substr($4, 2, 17)}' "$LOG" | uniq -c | tail -30
# most frequent 404 and 5xx paths (scanners, broken deploy)
awk '$9 ~ /^(404|5..)$/ {print $9, $7}' "$LOG" | sort | uniq -c | sort -rn | head -20
```

### SSH password guessing
```bash
# failed logins in the last hour by IP (works for ssh and sshd)
journalctl _COMM=sshd --since "-1h" \
  | grep -oP 'Failed \S+ for (invalid user )?\S+ from \K[0-9a-f.:]+' \
  | sort | uniq -c | sort -rn | head -20
# who last logged in successfully and from where
last -Faiw | head -20
```

### Connections and ports
```bash hl_lines="2"
# established connections to 443 by client IP
ss -Htn state established '( sport = :443 )' \
  | awk '{sub(/:[0-9]+$/, "", $4); print $4}' | sort | uniq -c | sort -rn | head
# SYN flood? number of half-open connections
ss -Htn state syn-recv | wc -l
# what is listening and which process
ss -tulpn
```

### Suspicious processes and files
```bash hl_lines="6"
# who is eating the CPU
ps -eo pid,user,%cpu,%mem,etime,cmd --sort=-%cpu | head -15
# processes whose binary was deleted (typical for malware)
ls -l /proc/*/exe 2>/dev/null | grep '(deleted)'
# network connections of a specific process
lsof -nP -i -a -p PID
# PHP files changed in the last 2 days (webshells)
find /var/www -type f -name '*.php' -mtime -2 -printf '%TY-%Tm-%Td %TH:%TM  %p\n' | sort -r | head -50
```

### Persistence: cron, timers, keys
```bash
# crontabs of all users
for u in $(cut -d: -f1 /etc/passwd); do crontab -l -u "$u" 2>/dev/null | sed "s/^/$u: /"; done
ls -la /etc/cron.* /var/spool/cron 2>/dev/null
systemctl list-timers --all
# authorized_keys and when they changed
find / -xdev -name authorized_keys -printf '%TY-%Tm-%Td %TH:%TM  %p\n' 2>/dev/null
# changed files from packages (Debian)
dpkg --verify | grep -v ' c '
```

### Block and verify
```bash hl_lines="2 4"
# ban in fail2ban (jail sshd / nginx-botsearch)
fail2ban-client set sshd banip 203.0.113.7
# nft set with a timeout (set inet filter blocklist must exist)
nft add element inet filter blocklist '{ 203.0.113.7 timeout 24h }'
fail2ban-client status sshd
nft list set inet filter blocklist
```

### Certificates and TLS
```bash hl_lines="1"
HOST=example.cz
echo | openssl s_client -servername "$HOST" -connect "$HOST:443" 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
certbot certificates
```

## 🧾 Quick server overview
```bash
uptime; free -h; df -hT -x tmpfs -x devtmpfs
systemctl --failed
journalctl -p err -b --no-pager | tail -30
du -xh / --max-depth=2 2>/dev/null | sort -rh | head -15
```
When space runs out: `#!bash journalctl --vacuum-size=500M` and `#!bash apt-get clean`.

## ⌨️ tmux
| shortcut | action |
|:--|:--|
| ++ctrl+b++ ++d++ | detach, the session keeps running |
| ++ctrl+b++ ++"%"++ / ++ctrl+b++ ++'"'++ | split vertically / horizontally |
| ++ctrl+b++ ++"["++ | scroll and copy mode |
| ++ctrl+b++ ++z++ | pane to full screen and back |
| ++ctrl+b++ ++s++ | list of sessions |

Attach to a running session: `#!bash tmux attach -t ops || tmux new -s ops`

# Security
## `Security`

## 🔎 Tools
- [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · actively exploited CVEs
- [Debian Security Tracker](https://security-tracker.debian.org/tracker/) · CVE status in packages
- [Ubuntu CVE](https://ubuntu.com/security/cves) · fix status
- [AbuseIPDB](https://www.abuseipdb.com) · IP reputation [?](Before banning a whole network, check whether it is a shared IP or the NAT of a large provider)
- [Shodan](https://www.shodan.io) · what is visible from outside
- [crt.sh](https://crt.sh) · Certificate Transparency [?](Reveals certificates issued for your domains, even ones you don't know about)
- [SSL Labs](https://www.ssllabs.com/ssltest/) · TLS configuration
- [CSIRT.CZ](https://csirt.cz) · [NÚKIB](https://nukib.gov.cz) · Czech CSIRT teams

## 🚩 CISA alerts
{{rss https://www.cisa.gov/cybersecurity-advisories/alerts.xml 4}}

## 🐧 Debian and Ubuntu
### Debian DSA
{{rss https://www.debian.org/security/dsa-long 4}}

### Ubuntu USN
{{rss https://ubuntu.com/security/notices/rss.xml 4}}

## 📡 SANS Internet Storm Center
{{rss https://isc.sans.edu/rssfeed_full.xml 3}}

## 📰 BleepingComputer
{{rss https://www.bleepingcomputer.com/feed/ 4}}

## 💥 Exploit-DB
{{rss https://www.exploit-db.com/rss.xml 4}}

*[KEV]: Known Exploited Vulnerabilities
*[CVE]: Common Vulnerabilities and Exposures
*[DSA]: Debian Security Advisory
*[USN]: Ubuntu Security Notice
*[ACME]: protocol for automated certificate issuance
*[CSIRT]: Computer Security Incident Response Team
*[NÚKIB]: National Cyber and Information Security Agency (Czech Republic)
