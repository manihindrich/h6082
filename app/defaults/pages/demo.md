// Default sample tab: a personal board. Make it your own, or delete it and start from scratch.
// Sample data: {.check .demo} is a made-up service status (.warn orange, .down red, ms=… response time),
// {{rss … demo}} shows made-up headlines, due dates @+3 and {{countdown +12}} count from today.
// On your own board write {.check} and {{rss URL}} without demo.

#++
![personal board](/media/demo-nastenka.svg)

#
##.
**Welcome to your board.** It's a plain markdown file: edit cards with ✎ right on the page, the whole file via {{gear}} in the top right.

📄 create a new tab in [settings](/settings)
🎬 everything markdown can do is in the [examples](/examples)
{: .muted }
/
##.
{{lang}} {{theme}}
/
##. 
### repository
[code.nolog.cz/hindrich/h6082](https://code.nolog.cz/hindrich/h6082)
[github.com/manihindrich/h6082](https://github.com/manihindrich/h6082) (mirror)

---
/
#
##. `📅 Today`

##* 📌 Pinned
**blinds** window 120 × 140 cm
**kids' shoes** EU 31 and 34
**licence plate** AB12 CDE
🏖️ Holiday {{countdown +12}}

## ✅ Tasks
- [ ] electricity bill @+2
- [ ] renew the domain @-1
- [ ] bike service @+6
- [ ] kids' clubs sign-up @+20
- [x] tax return @-5

## 🎁 Gift ideas
{{note}}
dad: coffee mug, a book about trains
Emma: lego, crayons
{{/note}}

#
##. `🧭 Bookmarks`

## 💼 Work
### 💬 Communication
- [Mail](https://proton.me/mail){.check .demo ms=41}
- [Slack](https://slack.com){.check .demo ms=58} · `#team`, `#incidents`
- [Google Meet](https://meet.google.com){.check .demo ms=37} · daily stand-up

### 🛠️ Tools
- [Jira](https://www.atlassian.com/software/jira){.check .demo ms=112} · my issues
- [Confluence](https://www.atlassian.com/software/confluence){.check .demo ms=97} · team wiki
- [GitHub](https://github.com/pulls){.check .demo ms=45} · pull requests
- [Figma](https://www.figma.com){.check .demo ms=73} · designs

Shortcuts: <kbd>Ctrl</kbd>+<kbd>K</kbd> search in Slack, <kbd>G</kbd> <kbd>I</kbd> in Jira
{: .muted }

## 🏡 Personal
### 💰 Money
[Wise](https://wise.com) [?](transfers and statements · log in with the app) · [Vanguard](https://investor.vanguard.com)

### 🧭 Travel
[OpenStreetMap](https://www.openstreetmap.org) · [Trainline](https://www.thetrainline.com) · [Windy radar](https://www.windy.com)

### 📦 Parcels
[17TRACK](https://www.17track.net) [?](one tracking page for all carriers)

#
##. `🟢 Services`

## 🏠 Home
| service | response |
|:--|--:|
| [Nextcloud](https://nextcloud.com){.check .demo ms=18} | 18 ms |
| [Jellyfin](https://jellyfin.org){.check .demo ms=24} | 24 ms |
| [Home Assistant](https://www.home-assistant.io){.check .demo ms=9} | 9 ms |
| [Immich](https://immich.app){.check .demo ms=31} | 31 ms |
| [Paperless](https://docs.paperless-ngx.com){.check .demo ms=22} | 22 ms |
| [Pi-hole](https://pi-hole.net){.check .demo .warn ms=64} [?](running, just wants you to log in again) | 64 ms |
| [Printer](http://printer.lan){.check .demo .down} [?](unplugged?) | — |

## 🌐 Network
| target | ping | loss |
|:--|--:|--:|
| [router](http://192.168.1.1){.check .demo ms=1} | 1 ms | 0 % |
| [NAS](http://nas.lan){.check .demo ms=2} | 2 ms | 0 % |
| [DNS 1.1.1.1](https://one.one.one.one){.check .demo ms=9} | 9 ms | 0 % |
| [internet](https://www.wikipedia.org){.check .demo ms=14} | 14 ms | 0 % |

#
##. `📊 Server`

## 🖥️ Home server
{{sys cpu mem load disk demo}}

## 💾 Backups
| | last |
|:--|--:|
| photos | today 3:00 ✓ |
| documents | today 3:05 ✓ |
| off-site | {{countdown -2}} ⚠ |

## 🕓 Who changed what
{{history 3 demo}}

#
##. `📰 Reading and help`

## 🗞️ Hacker News
{{rss https://news.ycombinator.com/rss 5 demo}}

##- 🌐 Internet is down
1. restart the router: socket on the left, wait 2 minutes
2. the **WAN** light must be green
3. still nothing? ISP support: 0800 123 456

##- 🐳 Update containers
```bash
cd /srv/stack
docker compose pull && docker compose up -d
docker image prune -f
```

##- 💾 Restore from backup
```bash
restic -r /mnt/nas/backup snapshots
restic -r /mnt/nas/backup restore latest --target /tmp/restore
```

##- ☎️ Contacts
| | |
|:--|--:|
| paediatrician | 020 7946 0123 |
| boiler service | 020 7946 0456 |
| insurance assistance | 0800 123 999 |
