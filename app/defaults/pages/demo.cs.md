// Výchozí ukázková záložka: osobní nástěnka. Uprav si ji po svém, nebo ji smaž a začni od nuly.
// Ukázková data: {.check .demo} je vymyšlený stav služby (.warn oranžová, .down červená, ms=… odezva),
// {{rss … demo}} ukáže vymyšlené titulky, termíny @+3 a {{countdown +12}} se počítají od dneška.
// Ve vlastní nástěnce piš {.check} a {{rss URL}} bez demo.

#++
![osobní nástěnka](/media/demo-nastenka.cs.svg)

#
##.
**Vítej na své nástěnce.** Je to obyčejný soubor v markdownu: karty s ✎ upravíš přímo na stránce, celý soubor přes {{gear}} vpravo nahoře.

📄 novou záložku založíš v [nastavení](/settings)
🎬 co všechno markdown umí, ukazují [ukázky](/examples)
{: .muted }


##.
{{lang}} {{theme}}


##. repozitář
[code.nolog.cz/hindrich/h6082](https://code.nolog.cz/hindrich/h6082)
[github.com/manihindrich/h6082](https://github.com/manihindrich/h6082) (mirror)
---
#
##. `📅 Dnes`

##* 📌 Připnuté
**žaluzie** okno 120 × 140 cm
**boty děti** 31 a 34
**SPZ** 4P2 1234
🏖️ Dovolená {{countdown +12}}

## ✅ Úkoly
- [ ] záloha na elektřinu @+2
- [ ] prodloužit doménu @-1
- [ ] servis kola @+6
- [ ] kroužky pro děti @+20
- [x] daňové přiznání @-5

## 🎁 Nápady na dárky
{{note}}
táta: hrnek na kávu, knížka o vlacích
Ema: lego, pastelky
{{/note}}

#
##. `🧭 Rozcestník`

## 💼 Práce
### 💬 Komunikace
- [Pošta](https://mail.proton.me){.check .demo ms=41}
- [Slack](https://slack.com){.check .demo ms=58} · `#tým`, `#incidenty`
- [Google Meet](https://meet.google.com){.check .demo ms=37} · denní stand-up

### 🛠️ Nástroje
- [Jira](https://www.atlassian.com/software/jira){.check .demo ms=112} · moje úkoly
- [Confluence](https://www.atlassian.com/software/confluence){.check .demo ms=97} · wiki týmu
- [GitHub](https://github.com/pulls){.check .demo ms=45} · pull requesty
- [Figma](https://www.figma.com){.check .demo ms=73} · návrhy

Rychlé klávesy: <kbd>Ctrl</kbd>+<kbd>K</kbd> hledání ve Slacku, <kbd>G</kbd> <kbd>I</kbd> v Jiře
{: .muted }

## 🏡 Osobní
### 💰 Peníze
[Fio banka](https://www.fio.cz) [?](platby a výpisy · přihlášení klíčem) · [Portu](https://www.portu.cz)

### 🧭 Na cesty
[Mapy.cz](https://mapy.cz) · [IDOS](https://idos.cz) · [ČHMÚ radar](https://www.chmi.cz)

### 🏛️ Úřady
[Portál občana](https://obcan.portal.gov.cz) · [Datová schránka](https://www.mojedatovaschranka.cz) [?](úřední pošta: zprávy se po 90 dnech mažou)

#
##. `🟢 Služby`

## 🏠 Doma
| služba | odezva |
|:--|--:|
| [Nextcloud](https://nextcloud.com){.check .demo ms=18} | 18 ms |
| [Jellyfin](https://jellyfin.org){.check .demo ms=24} | 24 ms |
| [Home Assistant](https://www.home-assistant.io){.check .demo ms=9} | 9 ms |
| [Immich](https://immich.app){.check .demo ms=31} | 31 ms |
| [Paperless](https://docs.paperless-ngx.com){.check .demo ms=22} | 22 ms |
| [Pi-hole](https://pi-hole.net){.check .demo .warn ms=64} [?](běží, jen chce znovu přihlásit) | 64 ms |
| [Tiskárna](http://tiskarna.lan){.check .demo .down} [?](vypnutá ze zásuvky?) | — |

## 🌐 Síť
| cíl | ping | ztráta |
|:--|--:|--:|
| [router](http://192.168.1.1){.check .demo ms=1} | 1 ms | 0 % |
| [NAS](http://nas.lan){.check .demo ms=2} | 2 ms | 0 % |
| [DNS 1.1.1.1](https://one.one.one.one){.check .demo ms=9} | 9 ms | 0 % |
| [internet](https://www.seznam.cz){.check .demo ms=14} | 14 ms | 0 % |

#
##. `📊 Server`

## 🖥️ Domácí server
{{sys cpu mem load disk demo}}

## 💾 Zálohy
| | poslední |
|:--|--:|
| fotky | dnes 3:00 ✓ |
| dokumenty | dnes 3:05 ✓ |
| mimo dům | {{countdown -2}} ⚠ |

## 🕓 Kdo co změnil
{{history 3 demo}}

#
##. `📰 Čtení a pomoc`

## 🗞️ Hacker News
{{rss https://news.ycombinator.com/rss 5 demo}}

##- 🌐 Nejde internet
1. restart routeru: zásuvka vlevo, počkat 2 minuty
2. kontrolka **WAN** musí svítit zeleně
3. pořád nic? porucha: 800 123 456

##- 🐳 Aktualizace kontejnerů
```bash
cd /srv/stack
docker compose pull && docker compose up -d
docker image prune -f
```

##- 💾 Obnova ze zálohy
```bash
restic -r /mnt/nas/zaloha snapshots
restic -r /mnt/nas/zaloha restore latest --target /tmp/obnova
```

##- ☎️ Kontakty
| | |
|:--|--:|
| pediatr | 377 123 456 |
| servis kotle | 603 111 222 |
| asistence pojišťovny | 1224 |
