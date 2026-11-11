# Start

![h6082](/media/demo-hero.svg)

**Hello 👋** This is an example tab. Everything here is plain markdown in `content/pages/demo.md` (the Czech version is `demo.cs.md`), feel free to rewrite or delete it.

## ☀️ Today
- [x] morning coffee
- [ ] go through notifications and PRs
- [ ] 30 minutes of reading
    - [ ] an article from the RSS next door
- [ ] back up photos

## 📝 Note
{{note}}
You can type right here on the page.
The field grows downwards and saves itself into the md file.
{{/note}}

## ⌨️ Browser shortcuts
- ++ctrl+l++ address bar
- ++ctrl+shift+t++ reopen closed tab
- ++ctrl+shift+v++ paste without formatting
- ++ctrl+f5++ reload without cache

# World

## 🌐 Service status
- [GitHub](https://github.com){.check} · code, issues, pull requests
- [Codeberg](https://codeberg.org){.check} · open-source git hosting
- [Wikipedia](https://www.wikipedia.org){.check} · encyclopedia
- [OpenStreetMap](https://www.openstreetmap.org){.check} · open maps
- [Mozilla](https://www.mozilla.org){.check} · Firefox and MDN
- [Cloudflare](https://www.cloudflare.com){.check} · CDN and DNS 1.1.1.1

<small>The dot refreshes every minute, hover to see the status code and latency.</small>

## 📰 Ars Technica
{{rss https://feeds.arstechnica.com/arstechnica/index 5}}

## 🖍️ xkcd
{{rss https://xkcd.com/atom.xml 3}}

# Create

## 🛠️ Development
### Documentation
- [MDN](https://developer.mozilla.org) · HTML, CSS, JavaScript
- [Python](https://docs.python.org/3/) · standard library
- [Rust](https://doc.rust-lang.org/book/) · The Book
### Tools
- [regex101](https://regex101.com) · debug regular expressions
- [explainshell](https://explainshell.com) · what a shell command does
- [crontab.guru](https://crontab.guru) · cron made readable
- [Can I use](https://caniuse.com) · browser support of web features

## 🎨 Design and inspiration
- [Coolors](https://coolors.co) · palette generator
- [Google Fonts](https://fonts.google.com) · free fonts
- [Unsplash](https://unsplash.com) · photos without licensing worries

## 📦 Snippet
```bash
# quick web server from the current folder
python3 -m http.server 8000
# what takes the most space
du -sh * | sort -h | tail
```

## 📊 Project
| task | status |
|---|:-:|
| design | ✓ |
| prototype | ✓ |
| tests | ⏳ |
| release | — |

# Overview

## 🖥️ Server
{{sys cpu mem load temp disk uptime demo}}

<small>**Demo mode**: made-up values. For real ones set `[system] enabled = true` in the config and remove `demo` from the block.</small>

## 🕓 Recent changes
{{history 5 demo}}

<small>**Demo mode**: made-up changes. For real ones remove `demo` from the block.</small>

## 💡 How to
> [!tip] Edit this tab
> On the **h6082** page at the top right click `demo.md`. The editor opens with a live preview.

> [!info] Own images
> Save them to `content/media/` and embed them with `![description](/media/file.png)`.

??? note "What is in here?"
    An image, tasks and a note editable right on the page, website status, RSS, server stats, change history, a table, code and callouts. Every element is described in the **markdown** tab on the h6082 page.

## ✉️ Contact
Write to {{email demo example.com}}. The address is protected from bots.
