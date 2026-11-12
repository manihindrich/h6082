// Demo: Ondřej, správce serverů v menší hostingové firmě (Proxmox cluster, web, databáze,
// pošta, zálohy, monitoring). Hostnamy a adresy jsou smyšlené (dokumentační rozsahy RFC 5737).
// Řádky začínající // se na stránce nezobrazují.

#__ O nástěnce
## 🛡️ Demo usecase: správce serverů
![terminál s logem a přehled serverů](/media/demo-admin.cs.svg)

**Ondřej** spravuje osm serverů menší hostingové firmy a drží pohotovost. Nástěnka je jeho **rozcestník a první obrazovka při incidentu**:

- **ráno** projde bezpečnostní feedy (CISA, Debian, Ubuntu, SANS ISC). Když vyjde oprava balíku, který má nasazený, zapíše si ho do *Patch plánu*.
- **stav závislostí** (DNS resolvery, Let's Encrypt, registry) vidí podle teček. Když nejde vystavit certifikát, hned ví, jestli je problém u něj nebo u ACME.
- **při útoku** neskládá příkazy z hlavy: zkopíruje je z bloku *Incident* jedním klikem. Zvýrazněné řádky jsou místa, kam doplní IP, PID nebo cestu.
- **během incidentu** si píše časovou osu do bloku *Právě řeším* přes ✎, bez editoru. Z ní pak vznikne postmortem.
- **na každém serveru** běží tmux. Zkratky, které nepoužívá denně, má v tahu.

# Provoz
## `Provoz`

##* 🔥 Právě řeším
**12. 11. 09:40** web-02: nárůst 5xx, load 14
**09:46** zdroj: botnet na `/wp-login.php`, ~900 IP, ban přes fail2ban + nft set
**10:05** stabilní, load 2. Otevřené: proč nezabral rate limit v nginx

## 🖥️ Servery
| host | role | OS | IP |
|:--|:--|:--|:--|
| pve-01..03 | Proxmox cluster | PVE 8 | 192.0.2.11–13 |
| web-01, web-02 | nginx + PHP-FPM | Debian 12 | 192.0.2.21–22 |
| db-01 | PostgreSQL 16, replika na db-02 | Debian 12 | 192.0.2.31 |
| mail-01 | Postfix, Dovecot, Rspamd | Debian 12 | 192.0.2.41 |
| backup-01 | Proxmox Backup Server | PBS 3 | 192.0.2.51 |

- [Proxmox](https://192.0.2.11:8006) · [Grafana](https://grafana.example.cz) · [Uptime Kuma](https://status.example.cz) · [PBS](https://192.0.2.51:8007)
- [Rspamd](https://mail.example.cz/rspamd/) · [Wiki: runbooky](https://wiki.example.cz/ops)

## 🌐 Závislosti
- [Cloudflare DNS](https://1.1.1.1){check="tcp://1.1.1.1:53"} · resolver 1.1.1.1
- [Quad9](https://quad9.net){check="tcp://9.9.9.9:53"} · záložní resolver
- [Let's Encrypt ACME](https://acme-v02.api.letsencrypt.org/directory){.check} [?](Když tečka svítí červeně, certifikáty se teď neobnoví. Certbot to zkusí znovu sám.)
- [Debian security](https://security.debian.org){.check} · zrcadlo aktualizací
- [Docker Hub registry](https://registry-1.docker.io/v2/){.check} [?](Oranžová tečka s kódem 401 je v pořádku: registr běží a jen chce přihlášení)
- [GitHub](https://github.com){.check} · deploy klíče, CI

## 📊 Tento server
{{sys cpu mem load disk uptime demo}}

##* 🩹 Patch plán
| kdy | co | kde | stav |
|:--|:--|:--|:-:|
| dnes 22:00 | sudo (USN / DSA) | všechny | ⏳ |
| čt 22:00 | kernel + reboot, po jednom uzlu | pve-01..03 | ⏳ |
| ne 06:00 | PostgreSQL 16.x minor | db-02 → failover → db-01 | 📋 |
| hotovo | openssh | všechny | ✓ |

> [!warning]- Okno údržby
> Zákazníci jsou informovaní 48 h předem přes status stránku. Reboot uzlů clusteru vždy po jednom a až po migraci VM (`ha-manager` / live migrace).

#++ Incident
## `Incident`

## 🚨 Útok a analýza
> [!danger] Než cokoli smažeš
> Zachovej stopy: snapshot VM, kopie `/var/log` a výpis procesů a spojení. Bez nich se nedá zjistit, kudy útočník přišel.

### Kdo nejvíc bije do webu
```bash hl_lines="1"
LOG=/var/log/nginx/access.log
# top 20 IP
awk '{print $1}' "$LOG" | sort | uniq -c | sort -rn | head -20
# požadavky za minutu (špička = začátek útoku)
awk '{print substr($4, 2, 17)}' "$LOG" | uniq -c | tail -30
# nejčastější 404 a 5xx cesty (skenery, rozbitý deploy)
awk '$9 ~ /^(404|5..)$/ {print $9, $7}' "$LOG" | sort | uniq -c | sort -rn | head -20
```

### Hádání hesel přes SSH
```bash
# neúspěšná přihlášení za poslední hodinu podle IP (funguje pro ssh i sshd)
journalctl _COMM=sshd --since "-1h" \
  | grep -oP 'Failed \S+ for (invalid user )?\S+ from \K[0-9a-f.:]+' \
  | sort | uniq -c | sort -rn | head -20
# kdo se naposledy úspěšně přihlásil a odkud
last -Faiw | head -20
```

### Spojení a porty
```bash hl_lines="2"
# navázaná spojení na 443 podle IP klienta
ss -Htn state established '( sport = :443 )' \
  | awk '{sub(/:[0-9]+$/, "", $4); print $4}' | sort | uniq -c | sort -rn | head
# SYN flood? počet napůl otevřených spojení
ss -Htn state syn-recv | wc -l
# co poslouchá a který proces
ss -tulpn
```

### Podezřelé procesy a soubory
```bash hl_lines="6"
# kdo žere CPU
ps -eo pid,user,%cpu,%mem,etime,cmd --sort=-%cpu | head -15
# procesy, jejichž binárka byla smazaná (typické pro malware)
ls -l /proc/*/exe 2>/dev/null | grep '(deleted)'
# síťová spojení konkrétního procesu
lsof -nP -i -a -p PID
# PHP soubory změněné za poslední 2 dny (webshelly)
find /var/www -type f -name '*.php' -mtime -2 -printf '%TY-%Tm-%Td %TH:%TM  %p\n' | sort -r | head -50
```

### Persistence: cron, timery, klíče
```bash
# crontaby všech uživatelů
for u in $(cut -d: -f1 /etc/passwd); do crontab -l -u "$u" 2>/dev/null | sed "s/^/$u: /"; done
ls -la /etc/cron.* /var/spool/cron 2>/dev/null
systemctl list-timers --all
# authorized_keys a kdy se změnily
find / -xdev -name authorized_keys -printf '%TY-%Tm-%Td %TH:%TM  %p\n' 2>/dev/null
# změněné soubory z balíků (Debian)
dpkg --verify | grep -v ' c '
```

### Zablokovat a ověřit
```bash hl_lines="2 4"
# ban v fail2ban (jail sshd / nginx-botsearch)
fail2ban-client set sshd banip 203.0.113.7
# nft set s časovým limitem (set inet filter blocklist musí existovat)
nft add element inet filter blocklist '{ 203.0.113.7 timeout 24h }'
fail2ban-client status sshd
nft list set inet filter blocklist
```

### Certifikáty a TLS
```bash hl_lines="1"
HOST=example.cz
echo | openssl s_client -servername "$HOST" -connect "$HOST:443" 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
certbot certificates
```

## 🧾 Rychlý přehled serveru
```bash
uptime; free -h; df -hT -x tmpfs -x devtmpfs
systemctl --failed
journalctl -p err -b --no-pager | tail -30
du -xh / --max-depth=2 2>/dev/null | sort -rh | head -15
```
Když dochází místo: `#!bash journalctl --vacuum-size=500M` a `#!bash apt-get clean`.

## ⌨️ tmux
| zkratka | akce |
|:--|:--|
| ++ctrl+b++ ++d++ | odpojit se, session běží dál |
| ++ctrl+b++ ++"%"++ / ++ctrl+b++ ++'"'++ | rozdělit svisle / vodorovně |
| ++ctrl+b++ ++"["++ | režim posunu a kopírování |
| ++ctrl+b++ ++z++ | panel na celou obrazovku a zpět |
| ++ctrl+b++ ++s++ | seznam sessions |

Připojení k běžící session: `#!bash tmux attach -t ops || tmux new -s ops`

# Security
## `Security`

## 🔎 Nástroje
- [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · aktivně zneužívané CVE
- [Debian Security Tracker](https://security-tracker.debian.org/tracker/) · stav CVE v balících
- [Ubuntu CVE](https://ubuntu.com/security/cves) · stav oprav
- [AbuseIPDB](https://www.abuseipdb.com) · reputace IP [?](Před banem celé sítě ověř, jestli nejde o sdílenou IP nebo NAT velkého operátora)
- [Shodan](https://www.shodan.io) · co je z venku vidět
- [crt.sh](https://crt.sh) · Certificate Transparency [?](Odhalí certifikáty vystavené na tvoje domény, i ty, o kterých nevíš)
- [SSL Labs](https://www.ssllabs.com/ssltest/) · TLS konfigurace
- [CSIRT.CZ](https://csirt.cz) · [NÚKIB](https://nukib.gov.cz) · české CSIRT týmy

## 🚩 CISA alerts
{{rss https://www.cisa.gov/cybersecurity-advisories/alerts.xml 4}}

## 🐧 Debian a Ubuntu
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
*[ACME]: protokol pro automatické vystavování certifikátů
*[CSIRT]: tým pro řešení počítačových incidentů
