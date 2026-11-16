# Documentation
## 📘 Documentation
Configuration, operation and security of h6082. You configure it in `config.toml` (**configuration** in the [Documentation and configuration](/settings) card) and in `.env`. Markdown and its elements are shown in the [markdown showcase](/markdown).
/

[Getting started](#features) · [How it works](#how-it-works) · [Operation](#updates) · [Security](#protection) · [Editor](#editor) · [Configuration](#config-format) · [Appearance](#cfg-layout) · [Endpoints](#pages-and-files)
{: .center .big }

---
/
# Getting started
##. `Getting started`

---
#
## Features
### Content
- tabs as md files, columns of different widths, and cards
- full markdown: tables, callouts, tasks, code with a copy button
- your own images from the `content/media/` folder
- web editor with highlighting, shortcuts and autosave
- `##*` cards, notes and tasks editable right on the page
- version history with diff and restore
### Live widgets
- instant refresh after saving
- service status (HTTP, TCP) right next to links
- RSS and server status as cards
### Appearance
- 32 themes and an auto mode that follows the system
- interface and documentation in English and Czech
- layout, font, colors and typography in `config.toml`

## Requirements
| | estimate |
|:--|:--|
| CPU | anything, even a Raspberry Pi; ~0 % when idle |
| memory | ~60 MB, upper limit 256 MB (compose limit) |
| disk | ~80 MB image + your content (a few MB) |
| system | Linux, macOS or Windows with Docker and Compose |
| network | only for RSS and service status |

**Difficulty: easy** ★☆☆☆☆, installation takes about 5 minutes: copy `.env`, fill in a password and run one command. Everything else is done in the browser.

##- Dependencies
| component | version |
|---|---|
| Docker + Compose | v2 |
| Python (alpine) | 3.12 |
| Markdown | 3.7 |
| pymdown-extensions | 10.12 |
| Pygments | 2.18.0 |
| defusedxml | 0.7.1 |
| JetBrains Mono | 2.304 |

The build needs internet access (PyPI, GitHub). At runtime only service checks and RSS go out, and only to addresses written in the md files.

#
## Installation
```bash
cp .env.example .env
# in .env: UID and GID (id), editor password
docker compose up -d --build
```

Local settings live in `.env`:
```bash
H6082_UID=1000          # id -u
H6082_GID=1000          # id -g
H6082_BIND=127.0.0.1    # this computer only
H6082_PORT=8088
H6082_EDITOR_USER=h6082
H6082_EDITOR_PASSWORD=… # openssl rand -base64 24
H6082_ALLOWED_HOSTS=    # extra hostnames, e.g. a domain behind a reverse proxy
H6082_READONLY=         # 1 = public read-only page (see Read-only mode)
H6082_DEMO=             # 1 = demo: read-only, but edits in the visitor's browser
H6082_CLIENT_IP_HEADER= # demo behind a proxy: header with the visitor's IP, e.g. CF-Connecting-IP
H6082_DISK_ROOT=/var/empty
```
After changing `.env`, run `docker compose up -d`. Exposing the page to the network is covered in the Security block.

`extra_hosts: host.docker.internal:host-gateway` lets you check services running directly on the host. The service must also listen on the docker bridge, not just on `127.0.0.1`.

## Running and maintenance
```bash
# build + start
docker compose up -d --build
# log
docker compose logs -f h6082
# restart / stop
docker compose restart h6082
docker compose down
# update the app
git pull && docker compose up -d --build
# backup (data + settings)
tar czf h6082.tgz content/ .env
# uninstall and clean up old layers
docker compose down --rmi local
docker image prune -f
```
The container has `restart: unless-stopped`, so it starts again after Docker restarts.
Content and config take effect right after saving, no restart needed. What an update changes and what it doesn't is described in the Updates card.

---
/
# How it works
##. `How it works`

---
#-
## How it works
1. the server loads `pages/<tab>.md` (or a translation for the current language)
2. splits the text into columns and cards
3. renders the markdown and caches the result
4. when a file changes, it sends a message to open pages (SSE)

## Live changes
An open page refreshes itself after saving, typically within 0.5 s (`live_reload`). The server watches the modification time of files in `content/` and sends the browser a message over SSE (`/events`). The browser swaps the content without flicker and keeps the scroll position.

Green dot in the top right = the connection is active. It reconnects by itself after a container restart. Behind a reverse proxy, turn off buffering for `/events`.

Without live reload, file modification times are checked on every request:
- `pages/*.md` and `system/*/*.md` → the tab is regenerated (a new image regenerates everything)
- `config.toml` → all tabs are regenerated
- a new or deleted `.md` → the tab bar changes

TOML syntax error: the last valid config stays in effect and a warning goes to the log. Unknown keys are ignored and logged too.

#
## Files
```text
docker-compose.yml
Dockerfile
.env            (local, do not commit)
.env.example
app/
  server.py
  static/
  defaults/          part of the image: built-in pages, demo, images, default config
content/             only your data — updates never touch it
  config.toml        your configuration (copied from the default on first start)
  pages/*.md         your tabs (+ translations *.cs.md)
  system/<lang>/     your edited built-in pages (optional)
  media/             your images
```
- `docker-compose.yml`: the container and its hardening
- `.env`: local settings and the editor password, template is `.env.example`. It is in `.gitignore`.
- `config.toml`: configuration (this tab)
- `app/defaults/`: what ships with the app — the built-in settings, markdown, documentation and examples pages in each language, the demo tabs, their images and the default `config.toml`
- `pages/*.md`: your tabs, with optional translations `name.cs.md` and `name.en.md` (see Languages)
- `system/<lang>/`: your own copies of built-in pages, created by saving in the editor
- `server.py`: generator, HTTP server, API (editor, checks, RSS)
- `.trash/`: deleted files, created on the first delete
- `.history/`: file versions, created on the first change
- `static/`: CSS, font, app icons
- `media/`: your own images for tabs (`/media/<file>`); files with the same name in `app/defaults/media/` serve as a fallback

The `content/` folder is mounted into the container as writable so the web editor can save to it. The container runs as UID:GID from `.env`, so the files stay yours. Changes to `app/` need a rebuild.


---
/
# Operation
##. `Operation`

---
#
## Updates
An update replaces only the app (the image). **Your data in `content/` and `.env` stays unchanged**:

| part | after an update |
|---|---|
| your tabs, notes, tasks | unchanged |
| `content/config.toml` | unchanged; new options use their default until you set them |
| built-in pages (settings, markdown, documentation, examples) | new version from the image |
| your edited built-in page | stays yours; *restore default* in the editor brings back the new default |
| demo tabs | copied only on the very first start (marker `content/.seeded`), never again |

First start with an empty `content/`: the default `config.toml` and the demo tabs are copied there. Deleted demos therefore never come back.

A deployment adds its domain with the `H6082_ALLOWED_HOSTS` environment variable (comma-separated) instead of editing `[api] allowed_hosts` in your config.

On the server, updates are done by the deploy workflow (the `h6082-deploy` repository).

#
## Read-only mode
`H6082_READONLY=1` turns the app into a public read-only page, e.g. a demo on the internet:

- nothing can be saved: the editor, new files, deleting, notes, tasks, theme, language and history return `403` and their controls are hidden
- content comes only from the image (`app/defaults/`): no volume, nothing is seeded or overwritten
- live reload (`/events`), server status (`/api/sys`) and change history are off
- visitors pick theme and language only in their own browser (cookie), the server stores nothing
- service status and RSS keep working, only for targets written in the md files in the image

Run it with a read-only file system and no volume (see `h6082-deploy-demo`). Even a bug in the app then has nowhere to write, and a restart is always clean.

**Demo mode** (`H6082_DEMO=1`) is a read-only mode in which visitors can try the app:

- they edit pages in the editor, tick and add tasks, write notes and change `##*` cards
- they create, rename, hide and delete pages and their translations; the tab bar and the file list in settings show it right away
- they can view config.toml in the editor, read-only
- changes are stored only in their browser (`localStorage`) and last until they press *reset demo* in the coloured bar at the top; the server writes nothing. The reset also returns the language, theme, folded cards and editor layout to the defaults
- the server renders the page with their changes via `/api/render` and stores nothing; RSS and status checks from the visitor's text are not run
- history and loading the default config stay visible but dimmed, do nothing, and on hover, focus or tap show "You can't try this in the demo"

#
## Sample data
Shows **made-up data** instead of real values. Useful for examples, documentation and public pages, because it reveals nothing about the server or your file names and needs no internet. It has nothing to do with the `H6082_DEMO` demo mode (see Read-only mode) and works in every mode.

| element | sample data | real data |
|---|---|---|
| service status | `{.check .demo}`: green, `.warn` orange (401), `.down` red (timeout), `ms=24` response time | `{.check}` |
| RSS | `{{rss URL 5 demo}}`: made-up headlines based on the feed address | `{{rss URL 5}}` |
| server | `{{sys demo}}` | `{{sys}}` + `[system] enabled = true` |
| either, by config | `{{sys auto}}`, `{{history 5 auto}}`: sample data while the feature is off | the same once it is on in the config |
| history | `{{history 5 demo}}` | `{{history 5}}` |

- none of this asks the server or downloads anything; it works even where real data is off (read-only mode, demo mode)
- the response time of `{.check .demo}` without `ms=` is always the same for the same address
- in animated examples ([examples](/examples) and the small examples in [markdown](/markdown)) live widgets are always made up, no need to write `demo`; tasks, notes and `##*` cards there are changed only by the animation

```md
- [Nextcloud](https://nextcloud.com){.check .demo ms=18}
- [Pi-hole](https://pi-hole.net){.check .demo .warn}
{{rss https://news.ycombinator.com/rss 5 demo}}
{{sys cpu mem disk demo}}
{{history 3 demo}}
```
The demo tab uses only sample data.

---
/
# Security
##. `Security`

---
#
## 🛡️ Protection
- listens only on `127.0.0.1`
- the editor and every write (notes, tasks, theme, language) are protected by a password (`H6082_EDITOR_PASSWORD` in `.env`)
- runs only its own scripts (CSP). `<script>` and `javascript:` in md don't work.
- other sites can't frame the page, read it via DNS rebinding or call the API
- the container has a read-only file system, no extra privileges, and memory and process limits
- checks and RSS go only to addresses from md
- writes are atomic, deleting is just a move to the trash
- images are served with CSP `sandbox`, so a script in an SVG won't run
- fonts are verified with SHA-256 at build time

## 🔒 Writes and network
- the API requires the `X-H6082` header. A foreign site in the browser can't send it without CORS, so other pages can't change your files.
- writes are atomic via a temporary file and rename, a file is never left half-written
- conflict check: the editor won't overwrite a change made elsewhere
- size limit `max_size_kb`
- system files (`settings`, `markdown`, `documentation`, `examples`, `config.toml`) can't be deleted, only your copy of a built-in page can be restored to the default; deleting is just a move to `content/.trash/`
- `/api/check` and `/api/rss` work only with targets and feeds written in md files, so the server can't be abused to scan the network
- RSS is parsed with `defusedxml` (protection against XML bombs and external entities). Only `http(s)` links get into the page, inserted as text, not as HTML.
- checks and RSS follow redirects only to `http(s)` and at most 3×

#
## ⚠️ Recommendations
- **anyone who can see the page can see the md content.** Passwords, tokens and private addresses don't belong there!
- `.env` contains the password and doesn't belong in a repository (it is in `.gitignore`)
- expose the page to the network only through a reverse proxy with HTTPS, and add the server name to `[api] allowed_hosts`
- write e-mail addresses as `{{email name domain}}` so bots can't read them
- **hidden tabs are not private.** They are reachable at `/<name>` and listed on the [settings](/settings) page.
- **the password protects only writing; anyone who can reach the page can read it.** On a public server, put the whole site behind a login in the reverse proxy.
- server status (`/api/sys`) is off (`[system] enabled`). Examples use `{{sys demo}}` with made-up data. Turn it on only where server details don't matter.
- in examples use `{{history demo}}`, the real history shows file names and edit times
- history keeps deleted text too. If you accidentally put a secret into a file, also delete the file's history in the editor via **history**.

## 🚫 Intentionally left out
Host processes, docker containers and network. They would require weakening the container isolation.

#
## 🔧 Technical details
- **Editor password** (`H6082_EDITOR_PASSWORD` in `.env`): HTTP Basic for `/edit/…` and all APIs that write. It is compared in constant time, and after a failed attempt the server responds with a 1 s delay.
- **CSP**: only the app's scripts run (a random nonce for each response). `<script>`, `onclick=` and `javascript:` from md don't run.
- **Frames**: `frame-ancestors 'self'` and `X-Frame-Options: SAMEORIGIN` protect against clickjacking.
- **Headers**: `nosniff`, `Referrer-Policy: same-origin`, `Cross-Origin-Resource-Policy` and `Cross-Origin-Opener-Policy: same-origin`.
- **Host**: all pages respond only to a `Host` from `[api] allowed_hosts`, otherwise 421 (protection against DNS rebinding).
- **Limits**: 30 s connection timeout, max. 32 `/events` connections, `Content-Length` check, max. file size `max_size_kb`.
- **Container**: read-only file system (writes only to `content/` and `/tmp`), `cap_drop: ALL`, `no-new-privileges`, limit of 256 MB RAM and 64 processes.
- **Build**: package versions are pinned, fonts are verified with SHA-256 (`ADD --checksum`). `.dockerignore` lets only `app/` into the build.
- **Writes**: the editor may write only to `content/config.toml`, `content/pages/*.md` and `content/system/<lang>/*.md`
- **Request origin**: the API accepts only an `Origin` from `[api] allowed_hosts`

---
/
# Editor and content
##. `Editor and content`

---
#+
## Editor
Saves automatically after a short pause in typing, ++ctrl+s++ saves right away. A live preview is on the right.

- **editor | preview divider**: drag it with the mouse; a double-click centers it again, ++arrow-left++ ++arrow-right++ work on the focused divider. The width is remembered in the browser.
- **preview** (button next to *view*) or ++alt+p++: hides / shows the preview
- **hide from the bar** (eye icon next to the file name): crossed-out eye = the tab is not in the bar, you open it only from settings or via `/<name>`; stored in `[tabs] hidden`
- **default config** (back-arrow icon, only for `config.toml`): loads the app's current default config into the editor; ++ctrl+z++ undoes it and the previous version stays in history. A deploy never overwrites your config, so this is how you get new comments and options.
- **rename / delete** (pencil and trash icons next to the file name): renaming takes translations, history and references in `config.toml` along; deleting moves the file to `content/.trash/`. For an edited system page, *restore default* is here instead.
- **line numbers**: the icon in the bar (next to *preview*) shows / hides them; the choice is remembered in the browser
- **pairing**: `` ( [ { < " ' ` `` close automatically, typing the closing bracket just skips over it, ++backspace++ deletes an empty pair
- **lists and quotes**: ++enter++ continues `-`, `1.`, `- [ ]` and `>`; ++enter++ on an empty item ends the list. ```` ```lang ```` + ++enter++ closes the code block.
- **indent**: ++tab++ / ++shift+tab++ indents a list item or all selected lines
- **selected text**: typing `*` wraps it in italics, another `*` makes it bold; `_` italics, `~` ~~strikethrough~~, `=` ==highlight==, `` ` `` code (several lines → a ```` ``` ```` block). Spaces at the edges of the selection stay outside, with several lines each one is wrapped separately and list markers stay in place.
- **pasting a URL** over selected text creates a link `[text](url)`
- **suggestions**: after `#` at the start of a line, `{{`, `> [!`, `{.`, `](/` or `- [` the editor offers syntax (columns, `##.` `##-` `##+` cards, shortcodes including `{{countdown}}`, classes …); ++enter++ / ++tab++ accepts, ++esc++ closes. See [Editor suggestions](#editor-suggestions).
- won't overwrite a file changed elsewhere (vim, git), offers *load from file* or *overwrite*
- invalid TOML is saved, but the last valid config stays in effect
- **history** shows file versions, diff and restore
- access is protected by the password from `.env`

| shortcut | action |
|---|---|
| ++ctrl+b++ | **bold** |
| ++ctrl+i++ | *italics* |
| ++ctrl+e++ | `code`, a block for several lines |
| ++ctrl+k++ | link `[text]()`, from a selected URL `[](url)` |
| ++ctrl+shift+x++ | ~~strikethrough~~ |
| ++ctrl+shift+h++ | ==highlight== |
| ++ctrl+shift+8++ | bullets `- ` |
| ++ctrl+shift+7++ | numbered list `1. ` |
| ++ctrl+shift+9++ | tasks `- [ ] ` |
| ++ctrl+z++ | also undoes automatic edits |

Formatting shortcuts toggle: pressing again removes the format. Without a selection they apply to the word under the cursor; outside a word they insert an empty pair. On a Mac, ++cmd++ works instead of ++ctrl++. Formatting and shortcuts apply only to `.md` files, not to `config.toml`.

#+
## Editor suggestions
{{livedemo 8}}
{{scene suggestions.md}}
##* Due dates
**1. 3.** insurance
> [!tip] Tip
> The editor suggests shortcodes too.
{{rss https://news.ycombinator.com/rss 3}}
{{/livedemo}}

````md
#        → columns, cards and headings: #+ #- #1.2 #60px #25% ## ##* ##. ##- ### … ######
{{       → shortcodes: {{rss URL 5}}, {{sys … auto}}, {{countdown +12}}, {{example …}} …
> [!     → callouts: tip, warning, danger, important, bug … folded (-) and open (+)
{        → attributes: .check .demo .warn .center .big .fill .mobile #anchor width= target= style= …
<        → HTML: <small> <sup> <kbd> <span style> <div markdown="1"> <details> …
@        → due date after - [ ] task: @+3 @-1 @+0 14:00 @2026-12-01
++ [? [^ → key ++ctrl+b++, hint [?](…), footnote [^1]
!!! ??? *[ [^ / //   → at the start of a line: admonition, folded block, abbreviation, footnote text, spacer, hidden note
](/      → names of your pages, ](/media/ images
- [      → task
```       → code block language, hl_lines / linenums, md live
````
- the list appears only after these starts, not on every word
- ++arrow-up++ ++arrow-down++ selects, ++enter++ or ++tab++ accepts, ++esc++ closes; without the list ++enter++ works as usual
- after accepting a shortcode its parameter (`URL`) is selected, just type over it
- works in the editor and when editing a `##*` card on the page, not on touch devices; to turn off: `[editor] suggest = false`

#
## [editor]
`enabled` · `true`
: web editor (`/edit/…`) and the save API. The password is set in `.env` (`H6082_EDITOR_PASSWORD`), not here.

`autosave_ms` · `800`
: autosave delay after the last keystroke

`max_size_kb` · `1024`
: max. size of a saved file

`suggest` · `true`
: markdown and shortcode suggestions while typing (editor and `##*` cards, not on touch devices); `false` switches all suggestions off

`[editor.suggestions]` · all `true`
: parts of the list: `columns` (`#` columns and headings), `shortcodes` (`{{`), `callouts` (`> [!`), `attributes` (`{`), `tasks` (`- [`), `due_dates` (`@` after a task), `html` (`<`), `inline` (`++` `[?` `[^` `==`), `line_starts` (`!!!` `???` `*[` `/` `//`), `links` (`](/`), `media` (`](/media/`), `code` (```` ``` ````)

`[editor.autocomplete]` · all `true`
: what the editor completes by itself (`.md` files only): `pairs` (closing brackets and quotes), `wrap` (wrapping a selection), `lists` (++enter++ continues lists, tasks, quotes and `: ` definitions), `fences` (closing a code block), `tables` (++enter++ at the end of a table row adds a row, under the header also `|---|`; an empty row ends the table), `notes` (`{{note}}` → `{{/note}}`), `html` (`<small>` → `</small>`), `admonitions` (indenting the content after `!!!` and `???`)

```toml
[editor.autocomplete]
tables = false
```

On a conflict the editor offers *load from file* or *overwrite*. The controls are described in the Editor card.

## Languages
The interface and built-in pages (settings, markdown, documentation) are in English and Czech. Pick the language in the dropdown in the top bar of the settings page, or in `[page] lang`. The choice is saved to `config.toml` and applies everywhere.

**Translations of your own tabs:** next to `name.md`, save `name.cs.md` (or `name.en.md`). The tab then shows the version for the selected language, and when a translation is missing it shows `name.md`. It appears in the bar only once. Deleting a tab deletes its translations too.

| file | when it is shown |
|---|---|
| `recipes.md` | default version |
| `recipes.cs.md` | with `lang = "cs"` |
| `recipes.en.md` | with `lang = "en"`, optional instead of the default version |

Preview another language without saving: `/<name>?lang=cs`.

## Top bar
```text
[header] | [tabs…] ……… [hidden] [language ▾] [theme ▾] ⚙ ●
```
- **header**: `[page] header`
- **tabs**: user `.md` from the left, ordered by `[tabs] order`
- **hidden**: shown only while viewing a hidden tab (dashed border)
- **language, theme**: dropdowns, only on the settings page
- **⚙**: the settings page (`/settings`, `[page] about_tab`): overview, files, settings
- **●**: live reload, green = connected

---
/
# Configuration
##. `Configuration`

---
#
## Config format
The `content/config.toml` file is in TOML format. Values with a unit are CSS values written as strings, e.g. `"12px"` or `"1.2em"`. Colors can be in any CSS format: `#rrggbb`, `rgb()`, `hsl()` or a name.
```toml
[layout]
gap = "12px"
[colors]
accent = "#a882ff"
```
A missing key has its default value.

## [page]
`title` · `"h6082"`
: browser title; with several tabs it shows as `<tab> · <title>`

`favicon` · `""`
: browser tab icon: `""` = built-in purple diamond, otherwise a single character or emoji (`"🚀"`)

`lang` · `"en"`
: language of the interface and built-in pages: `en` or `cs`. It can also be switched in the dropdown in the top bar of the settings page (or with the `{{lang}}` shortcode); the choice is written here.

`links_new_tab` · `true`
: external links (`http`/`https`) open in a new tab

`header` · `""`
: header on the left of the top bar, separated from the tabs by a line. Inline markdown, e.g. `"**home** · start page"`. Empty string = no header.

`live_reload` · `true`
: the page refreshes itself after a `.md` or the config is saved. The green dot in the top right means an active connection.

`about_tab` · `"settings"`
: the tab shown in the top right (default is the built-in settings page; the former `"h6082"` still works). It isn't placed in the left bar. Without user tabs it is at `/`. `""` = none.

## [history]
`enabled` · `false`
: change history of all `.md` files and `config.toml` (the *history* link in the editor, diff and restore, `{{history}}`). Off by default, switch it on if you want file versions. `{{history … demo}}` (made-up changes) works even when off, `{{history … auto}}` shows sample data until it is on.

`coalesce_min` · `5`
: edits within this many minutes of the last version are merged into one, so autosave doesn't create hundreds of versions

`max_versions` · `50`
: max. number of versions per file

`max_age_days` · `90`
: older versions are deleted. The 3 newest always stay.

A version is **the state of the file before the change**. Edits from the editor and from elsewhere (vim, git) are captured: the server checks files every 2 s. Before a restore, the current state is saved as a new version, so a restore can be undone too. Version content, diff and restore are behind the editor password. `{{history}}` on a page shows only times, names and line counts.

#
## [api]
`allowed_hosts` · `["127.0.0.1", "localhost"]`
: hostnames the server responds to (`Host`) and that may call `/api` (`Origin`). Applies to all pages. If you access it under another name, add it here.

## [checks]
`enabled` · `true`
: availability check for links with `{.check}` / `{check="…"}`

`interval_s` · `60`
: how often the status refreshes (results are held in the server 5 s shorter)

`timeout_s` · `4`
: timeout of a single check

`verify_tls` · `false`
: verify the certificate. `false` = self-signed passes too (homelab); the check sends no data.

ICMP ping doesn't work in the container because it runs without root privileges. Use `tcp://host:port` instead.

## [tabs]
`order` · `[]`
: order of user tabs from the left, by file name. The first one is the home page `/`. Files not in the list follow alphabetically.

`labels` · `{}`
: labels, e.g. `{ demo = "sample" }`. The default label is the file name. A label can also be set per language: `{ recipes = { en = "recipes", cs = "recepty" } }`.

`hidden` · `[]`
: tabs hidden from the bar, still reachable at `/<name>` and from the file list on the settings page. Also toggled with the eye icon in the editor. Built-in pages (markdown, documentation) are never in the bar, no need to hide them; the exception is examples, see `examples`.

`examples` · `true`
: the examples page (`/examples`) as the first tab on the left; move it elsewhere by listing `"examples"` in `order`. The home page `/` stays the first user tab. Also toggled with the “in the bar” checkbox next to the examples tab on the [markdown](/markdown) page (with the editor password); the choice is written here.

`show_single` · `false`
: show the bar even when there is only one user tab
```toml
[tabs]
order  = ["dev", "infra", "notes"]
labels = { demo = "sample", dev = { en = "dev", cs = "vývoj" } }
hidden = ["drafts"]
```

## [markdown]
`line_breaks` · `true`
: ++enter++ in text = new line, empty line = new paragraph. `false` restores classic markdown behavior (lines are joined).

A line with just `/` inserts an empty line, `//` two. Outside a card (under `#`, above `##`) it adds space between cards. A line starting with `// text` is a hidden note.

#
## [system]
`enabled` · `false`
: real values for `{{sys [parts…]}}` and the `/api/sys` endpoint. Off by default, because anyone who can see the page can see `/api/sys`. `{{sys demo}}` with made-up data works even when off.

`interval_s` · `5`
: refresh of the values on the page

`temps` · `[]`
: thermal zone types (`/sys/class/thermal/*/type`), e.g. `["x86_pkg_temp", "acpitz"]`. `[]` = automatic: `x86_pkg_temp` as CPU, otherwise the highest temperature.

`disks`
: a list of `{ label, path }`. `path` is a folder **in the container** that lies on the monitored disk.
```toml
disks = [
  { label = "/",       path = "/host/disk/root" },
  { label = "content", path = "/app/content" },
]
```
The container sees the root disk through the empty host folder `H6082_DISK_ROOT` from `.env`. Another disk = another empty folder in `volumes` (`:ro`). The container only learns the disk size and can't see the folder contents.

Values come from the host (the container shares `/proc` and `/sys` with the kernel). Network, processes and docker containers are left out on purpose: they would require `network_mode: host`, `pid: host` or the docker socket, which weakens isolation.

## [rss]
`enabled` · `true`
: `{{rss URL [count]}}` feeds

`refresh_min` · `15`
: time in cache. When the source fails, the last known state is shown.

`timeout_s` · `8`
: download timeout, max. feed size is 2 MB

`default_limit` · `10`
: number of items when not given in the shortcode

## [code]
`pygments_style` · `"monokai"`
: color scheme of code blocks for the **obsidian** theme, e.g. `monokai`, `dracula`, `one-dark`, `nord`, `gruvbox-dark`, `material`, `github-dark`, `solarized-dark`, `native`, `zenburn`. Other themes have their own scheme. Unknown name = `monokai` + a warning in the log.

`line_numbers` · `false`
: line numbers in all code blocks; with `false` only blocks with `linenums="1"` have them

`wrap` · `true`
: long code lines wrap; `false` = horizontal scrollbar

The background of code blocks is always `code_bg`, only token colors are taken from the scheme.

---
/
# Appearance
##. `Appearance`

---
#
## [layout]
`columns_fixed` · `0`
: `0` = number of columns based on window width, `N` = N regular columns per row

`column_min_width` · `"240px"`
: min. column width in automatic mode. `#+` / `#++` columns are 1.5× / 1.75× wider, `#-` / `#--` half / quarter width, `#1.2` a custom ratio; a column needs at least its number × this width, otherwise the row wraps. `#120px` has a fixed width. A `---` line starts a new row of columns (a lone `#` in it is a full-width band). The syntax is shown in the [markdown showcase](/markdown#columns).

`page_max_width` · `"1600px"`
: max. content width, `"none"` = full width

`padding` · `"14px"`
: page margin

`gap` · `"12px"`
: space between columns and below the tab bar

`row_gap` · `""`
: space between rows of columns (`---`); `""` = same as `gap`

`block_gap` · `"10px"`
: vertical space between cards in a column

`block_padding` · `"6px 10px 8px"`
: inner padding of a card (CSS padding: top, right/left, bottom)

`radius` · `"6px"`
: corner rounding of cards and tabs

`h3_indent` · `"2px"`
: indent of the `###` heading

`content_indent` · `"10px"`
: indent of content under `###`

Up to 640 px wide there is always a single column.

## [font]
`family` · JetBrains Mono
: CSS `font-family`. JetBrains Mono is bundled in the image. Any other font must be installed on the browser's system, e.g. `'"Fira Code", monospace'`.

`size` · `"13px"`
: base font size, everything else is derived from it

`line_height` · `"1.4"`
: line spacing

`block_title_transform` · `"none"`
: card titles: `none`, `uppercase`, `lowercase`, `capitalize`

#
## [style]
Content typography, each element has its own section: `[style.text]`, `[style.h2]` to `[style.h6]`, `bold`, `italic`, `strike`, `highlight`, `link`, `code`, `code_block`, `quote`, `list`, `task`, `callout`, `kbd`, `tip`, `table` and `bracket_round` / `square` / `curly` / `angle` for text in brackets.

| key | CSS |
|:--|:--|
| `color`, `bg` | text color, background |
| `size`, `weight`, `style` | size, weight, italics |
| `space_before`, `space_after` | space above and below |
| `padding`, `radius`, `border` | padding, rounding, border |

- `""` = built-in look; a color can be the name of a theme color (`muted`, `accent`, `h3`…), then it changes with the theme
- `em` is a multiple of the font size: `1em` = font height, so spacing grows with `[font] size`
- all keys with default values and comments are in the default `config.toml`
- changes take effect right after saving

## [themes.*]
A custom theme, or a tweak of a built-in one when you use its name. Keys are as in `[colors]`, plus:

`label`
: name in the switcher

`scheme` · `"dark"`
: `dark` / `light`. Sets the group in the switcher and the colors of browser elements (scrollbars, forms).

`pygments_style`
: code highlighting scheme

`pair`
: name of the counterpart in the other scheme (e.g. a light theme's dark version). The picker then shows them side by side on one row.

Missing colors are filled in from `obsidian`.
```toml
[themes.mine]
label  = "mine"
scheme = "light"
pygments_style = "friendly"
bg     = "#fafafa"
panel  = "#ffffff"
text   = "#202020"

[themes.nord]   # tweak of a built-in theme
accent = "#b48ead"
```

#
## Themes
Pick one in the dropdown in the top bar of the settings page. The choice writes the theme to `config.toml` as `[theme] default` (with the editor password), so it applies to all browsers. Other lines and comments in the config stay unchanged.

| dark | code | light | code |
|---|---|---|---|
| `obsidian` | `[code]` | `obsidian-light` | friendly |
| `nord` | nord | `nord-light` | default |
| `dracula` | dracula | `dracula-light` | xcode |
| `gruvbox-dark` | gruvbox-dark | `gruvbox-light` | gruvbox-light |
| `solarized-dark` | solarized-dark | `solarized-light` | solarized-light |
| `catppuccin-mocha` | one-dark | `catppuccin-latte` | default |
| `tokyo-night` | one-dark | `tokyo-night-day` | xcode |
| `lagoon` | material | `lagoon-light` | xcode |
| `meadow` | monokai | `meadow-light` | default |
| `berry` | dracula | `berry-light` | xcode |
| `azure` | github-dark | `azure-light` | default |
| `paper-dark` | github-dark | `paper` | default |
| `one-dark` | one-dark | `one-light` | xcode |
| `rose-pine` | dracula | `rose-pine-dawn` | xcode |
| `everforest` | gruvbox-dark | `everforest-light` | gruvbox-light |
| `ayu-mirage` | material | `ayu-light` | default |

Each row is the dark and the light version of the same look, as in the picker. `obsidian` = colors from `[colors]` (default). `auto` picks between `auto_dark` and `auto_light` based on the system setting and switches even while the page is open.

Preview without saving the choice: `?theme=<theme>`, e.g. [/documentation?theme=paper](/documentation?theme=paper).

## [theme]
`default` · `"auto"`
: active theme; `"auto"` follows the system (`auto_dark` / `auto_light`), otherwise a theme name, e.g. `"obsidian"`. Also set by the picker on the settings page.

`auto_dark` · `"obsidian"`
: theme for `auto` when the system is dark

`auto_light` · `"obsidian-light"`
: theme for `auto` when the system is light

#
## [colors] base
| key | default | used for |
|---|---|---|
| `bg` | `#1e1e1e` | page background |
| `panel` | `#262626` | cards, active tab |
| `border` | `#363636` | borders, tables, `---` |
| `text` | `#dcddde` | text |
| `muted` | `#999999` | bullets, quotes, inactive tabs |
| `accent` | `#a882ff` | active tab, checkboxes, selection |
| `h2` | `#a882ff` | card titles |
| `h3` | `#c6b6ff` | `###`, table headers, terms |
| `link` | `#8a9cff` | links |
| `link_hover` | `#b5c0ff` | link on hover |

## [colors] code and highlight
| key | default | used for |
|---|---|---|
| `code_bg` | `#2b2b2b` | code and key background |
| `code_fg` | `#e0a96d` | inline code |
| `mark_bg` | `#6b5a1e` | `==highlight==` |
| `quote_border` | `#555555` | quote line |

## [colors] callouts
| key | default | types |
|---|---|---|
| `callout_note` | `#448aff` | note, abstract, quote, example, unknown |
| `callout_tip` | `#00bfa5` | tip, hint, important, success |
| `callout_info` | `#00b8d4` | info, todo, question, faq |
| `callout_warning` | `#ff9100` | warning, caution, attention |
| `callout_danger` | `#ff5252` | danger, error, bug, failure |

> [!tip] Light theme
> Override `bg`, `panel`, `border`, `text`, `muted` and `code_bg`. Then adjust `h3`, `link` and `code_fg` so they have enough contrast.

---
/
# Endpoints
##. `Endpoints`

---
#
## Pages and files
`/`
: the first tab

`/<name>`
: the tab `pages/<name>.md` (or its translation, see Languages)

`/<name>?lang=en`
: preview of the tab in another language, nothing is saved

`/<name>?embed=1`
: the tab without the top bar (preview in the editor)

`/edit/<file>`
: web editor (`<name>.md`, `<name>.cs.md`, `system/<lang>/<name>.md` or `config.toml`)

`/themes.css`
: CSS of all themes (generated from the config)

`/media/<file>`
: your own images from `content/media/` (svg, png, jpg, webp, gif, avif, ico) with CSP `sandbox`

`/static/…`
: CSS, font, images

`/events`
: SSE stream for live reload

`/history/<file>`
: list of versions, diff and restore (with the editor password)

`/healthz`
: healthcheck (`ok`)

#
## Read API
`/api/file?name=…`
: read (GET) and save (PUT) a file for the editor

`/api/check`
: service status (POST, list of targets)

`/api/rss?url=…&limit=…`
: feed items (GET)

`/api/sys`
: system status for `{{sys}}` (GET)

`/api/history?file=…&limit=…`
: recent changes for `{{history}}`: only times, files and line counts (GET)

## Rules
If a password is set, `/edit/…`, `/api/file`, `/api/new` and `/api/rename` require login. For a `Host` other than those in `[api] allowed_hosts` the server responds with error 421.

A tab name may contain only `A-Z a-z 0-9 _ . -`. A file with any other name is ignored. The names `static`, `events`, `healthz`, `edit`, `api`, `history` and `media` are reserved, as are the built-in page names `settings`, `markdown`, `documentation` and `examples` and the former or Czech addresses `h6082`, `nastaveni` (redirect to `/settings`), `docs` and `dokumentace` (redirect to `/documentation`).

#
## Write API
`/api/file?name=…` DELETE
: deletes a user tab together with its translations (for a translation, only that file), i.e. moves it to `content/.trash/<name>.<time>.md`

`/api/new`
: creates a new `.md` (POST)

`/api/rename`
: renames a tab together with its translations and history (POST `{name, to}`); references in `[tabs] order`, `hidden`, `labels` and `[page] about_tab` in `config.toml` are updated automatically. A translation is renamed along with it.

`/api/theme`
: saves the theme to `[theme] default` (POST, with the editor password)

`/api/lang`
: saves the language to `[page] lang` (POST, with the editor password)

`/api/note`
: saves a `{{note}}` note (POST, with the editor password)

`/api/block`
: saves a `##*` card edited right on the page (POST `{file, i, orig, text}`, with the editor password)

`/api/tasks`
: ticks, adds and deletes a task (POST, with the editor password)

`/api/history/restore`, `/api/history/purge`
: restores a version and deletes history (POST, with the editor password)
