# Operation

## Files
```text
docker-compose.yml
Dockerfile
.env            (local, do not commit)
.env.example
app/
  server.py
  static/
  defaults/          shipped with the image: built-in pages, demo, images, default config
content/             your data only — an update never touches it
  config.toml        your configuration (copied from the defaults on the first start)
  pages/*.md         your tabs (+ translations *.cs.md)
  system/<lang>/     your customised built-in pages (optional)
  media/             your images
```
- `docker-compose.yml`: the container and its hardening
- `.env`: local settings and the editor password, template `.env.example`. It is in `.gitignore`.
- `config.toml`: configuration (this tab)
- `app/defaults/`: what comes with the application — built-in pages h6082, markdown and config in each language, the demo tab, its images and the default `config.toml`
- `pages/*.md`: your tabs, optionally with translations `name.cs.md` and `name.en.md` (see Languages)
- `system/<lang>/`: your own copies of built-in pages, created by saving them in the editor
- `server.py`: generator, HTTP server, API (editor, checks, RSS)
- `.trash/`: deleted files, created by the first delete
- `.history/`: file versions, created by the first change
- `static/`: CSS, font, application icons
- `media/`: own images for tabs (`/media/<file>`); files of the same name in `app/defaults/media/` are used as a fallback

The `content/` folder is mounted writable into the container so the web editor can save into it. The container runs as the UID:GID from `.env`, so the files stay yours. Changes in `app/` need a rebuild.

## Running
```bash
# build + start
docker compose up -d --build
# log
docker compose logs -f h6082
# restart / stop
docker compose restart h6082
docker compose down
```
The container has `restart: unless-stopped`, so it starts again after a Docker restart.

## Port and .env
Local settings live in `.env`:
```bash
H6082_UID=1000          # id -u
H6082_GID=1000          # id -g
H6082_BIND=127.0.0.1    # this machine only
H6082_PORT=8088
H6082_EDITOR_USER=h6082
H6082_EDITOR_PASSWORD=… # openssl rand -base64 24
H6082_ALLOWED_HOSTS=    # extra hostnames, e.g. a domain behind a reverse proxy
H6082_READONLY=         # 1 = public read-only page (see Read-only mode)
H6082_DISK_ROOT=/var/empty
```
After changing `.env` run `docker compose up -d`. Exposing the page to a network is covered by the Security block on the [h6082](/h6082) page.

`extra_hosts: host.docker.internal:host-gateway` lets you check services running directly on the host. The service must however listen on the docker bridge too, not only on `127.0.0.1`.

## Updates
An update replaces only the application (the image). **Your data in `content/` and `.env` are never touched**:

| part | after an update |
|---|---|
| your tabs, notes, tasks | unchanged |
| `content/config.toml` | unchanged; new options use their defaults until you set them |
| built-in pages (h6082, markdown, config) | new version from the image |
| your customised built-in page | yours stays; ↺ on the h6082 page returns the new default |
| demo tab | copied only on the very first start (marker `content/.seeded`), never again |

First start with an empty `content/`: the default `config.toml` and the demo tab are copied there. A deleted demo therefore never comes back.

A deployment adds its domain with the `H6082_ALLOWED_HOSTS` environment variable (comma separated) instead of editing `[api] allowed_hosts` in your config.

Update: `git pull && docker compose up -d --build`. On a server this is done by the deploy workflow (repository `h6082-deploy`).

## Live changes
An open page refreshes itself after a save, typically within 0.5 s (`live_reload`). The server watches the modification time of files in `content/` and notifies the browser via SSE (`/events`). The browser swaps the content without flicker and keeps the scroll position.

Green dot at the top right = the connection is active. It reconnects by itself after a container restart. Behind a reverse proxy, buffering must be disabled for `/events`.

Without live reload, the modification time is checked on every request:
- `pages/*.md` and `system/*/*.md` → the tab is re-rendered (a new image re-renders everything)
- `config.toml` → all tabs are re-rendered
- a new or deleted `.md` → the tab bar changes

A TOML syntax error keeps the last valid config and logs a warning. Unknown keys are ignored and logged too.

## Endpoints
`/`
: the first tab

`/<name>`
: tab `pages/<name>.md` (or its translation, see Languages)

`/<name>?lang=cs`
: preview of a tab in another language, nothing is saved

`/<name>?embed=1`
: tab without the top bar (editor preview)

`/edit/<file>`
: web editor (`<name>.md`, `<name>.cs.md`, `system/<lang>/<name>.md` or `config.toml`)

`/api/file?name=…`
: read (GET) and save (PUT) a file for the editor

`/api/file?name=…` DELETE
: delete a user tab with its translations (for a translation only that file), i.e. move it to `content/.trash/<name>.<time>.md`

`/api/new`
: create a new `.md` (POST)

`/api/check`
: service status (POST, list of targets)

`/api/rss?url=…&limit=…`
: feed items (GET)

`/themes.css`
: CSS of all themes (generated from the config)

`/api/sys`
: server stats for `{{sys}}` (GET)

`/media/<file>`
: own images from `content/media/` (svg, png, jpg, webp, gif, avif, ico) with CSP `sandbox`

`/static/…`
: CSS, font, images

`/events`
: SSE stream for live reload

`/history/<file>`
: list of versions, diff and restore (with the editor password)

`/api/theme`
: save the theme to `[theme] default` (POST, with the editor password)

`/api/lang`
: save the language to `[page] lang` (POST, with the editor password)

`/api/note`
: save a `{{note}}` (POST, with the editor password)

`/api/tasks`
: toggle, add and delete a task (POST, with the editor password)

`/api/history?file=…&limit=…`
: latest changes for `{{history}}`: only times, files and line counts (GET)

`/api/history/restore`, `/api/history/purge`
: restore a version and delete the history (POST, with the editor password)

`/healthz`
: healthcheck (`ok`)

If a password is set, `/edit/…`, `/api/file` and `/api/new` require a login. For a `Host` that is not in `[api] allowed_hosts` the server answers with error 421.

A tab name may only contain `A-Z a-z 0-9 _ . -`. Files with other names are ignored. The names `static`, `events`, `healthz`, `edit`, `api`, `history` and `media` are reserved, and so are the names of the built-in pages `h6082`, `showcase` and `docs`.

## Security
An overview is in the Security block on the [h6082](/h6082) page. Technical details:

- **Editor password** (`H6082_EDITOR_PASSWORD` in `.env`): HTTP Basic for `/edit/…`, `/api/file` and `/api/new`. Compared in constant time; after a wrong attempt the server answers with a 1 s delay.
- **CSP**: only the application's scripts run (a random nonce per response). `<script>`, `onclick=` and `javascript:` from md never run.
- **Frames**: `frame-ancestors 'self'` and `X-Frame-Options: SAMEORIGIN` protect against clickjacking.
- **Headers**: `nosniff`, `Referrer-Policy: same-origin`, `Cross-Origin-Resource-Policy` and `Cross-Origin-Opener-Policy: same-origin`.
- **Host**: every page answers only to a `Host` from `[api] allowed_hosts`, otherwise 421 (protection against DNS rebinding).
- **Limits**: 30 s connection timeout, max. 32 `/events` connections, `Content-Length` check, max. file size `max_size_kb`.
- **Container**: read-only file system (writes only to `content/` and `/tmp`), `cap_drop: ALL`, `no-new-privileges`, 256 MB RAM and 64 process limit.
- **Build**: package versions are pinned, fonts are verified via SHA-256 (`ADD --checksum`). `.dockerignore` lets only `app/` into the build.
- **Writes**: the editor may write only to `content/config.toml`, `content/pages/*.md` and `content/system/<lang>/*.md`
- **Request origin**: the API accepts only an `Origin` from `[api] allowed_hosts`
- the API requires the `X-H6082` header. A foreign website cannot send it from the browser without CORS, so other pages cannot change files.
- writes are atomic via a temp file and a rename, a file is never left half-written
- concurrency check: the editor never overwrites a change made elsewhere
- size limit `max_size_kb`
- system files (`h6082`, `showcase`, `docs`, `config.toml`) cannot be deleted, only your copy of a built-in page can be reset; deleting is just a move to `content/.trash/`
- `/api/check` and `/api/rss` work only with targets and feeds written in md files, so the server cannot be abused to scan a network
- RSS is parsed with `defusedxml` (protection against XML bombs and external entities). Only `http(s)` links get into the page, inserted as text, not as HTML.
- checks and RSS follow redirects only to `http(s)` and at most 3 times

## Cleanup
```bash
# stop + delete the image
docker compose down --rmi local
# old layers after rebuilds
docker image prune -f
```

# Page

## Config format
The file `content/config.toml` is in TOML format. Values with a unit are CSS values and are written as strings, e.g. `"12px"` or `"1.2em"`. Colours can be in any CSS format: `#rrggbb`, `rgb()`, `hsl()` or a name.
```toml
[layout]
gap = "12px"
[colors]
accent = "#a882ff"
```
A missing key has its default value.

## Top bar
```text
[header] | [tabs…] ……… [hidden] [h6082] ●
```
- **header**: `[page] header`
- **tabs**: user `.md` files from the left, ordered by `[tabs] order`
- **hidden**: shown only while viewing a hidden tab (dashed frame)
- **h6082**: `[page] about_tab`, info, file list and editor
- **●**: live reload, green = connected

## [page]
`title` · `"h6082"`
: browser title; with several tabs shown as `<tab> · <title>`

`favicon` · `"◆"`
: a character or emoji as the browser tab icon

`lang` · `"en"`
: language of the UI and the built-in pages: `en` or `cs`. Also switched by the Language block on the h6082 page (`{{lang}}`), which writes the choice here.

`links_new_tab` · `true`
: external links (`http`/`https`) open in a new tab

`header` · `""`
: header on the left of the top bar, separated from the tabs by a line. Inline markdown, e.g. `"**home** · start page"`. Empty string = no header.

`live_reload` · `true`
: the page refreshes itself after an `.md` or config save. A green dot at the top right means an active connection.

`about_tab` · `"h6082"`
: the tab shown at the top right (the built-in h6082 page by default). It is not put into the left bar. Without user tabs it is at `/`. `""` = none.

## [tabs]
`order` · `[]`
: order of the user tabs from the left by file name. The first one is the home page `/`. Files not in the list follow alphabetically.

`labels` · `{}`
: labels, e.g. `{ docs = "config" }`. The default label is the file name. A label can also be given per language: `{ demo = { en = "demo tab", cs = "demo záložka" } }`.

`hidden` · `[]`
: tabs hidden from the bar, still reachable via `/<name>` and from the file list on h6082. The built-in pages (markdown, config) are never in the bar, no need to hide them.

`show_single` · `false`
: show the bar even if there is only one user tab
```toml
[tabs]
order  = ["dev", "infra", "notes"]
labels = { showcase = "markdown" }
hidden = ["drafts"]
```

## Languages
The UI and the built-in pages (h6082, markdown, config) are available in English and Czech. The language is chosen in the **Language** block on the h6082 page, or in `[page] lang`.

**Translations of your own tabs:** next to `name.md` save `name.cs.md` (or `name.en.md`). The tab then shows the version for the selected language; if a translation is missing, it shows `name.md`. The tab appears only once in the bar. Deleting a tab deletes its translations too.

| file | shown when |
|---|---|
| `demo.md` | default version |
| `demo.cs.md` | with `lang = "cs"` |
| `demo.en.md` | with `lang = "en"` (optional) |

Preview of another language without saving: `/<name>?lang=cs`.

## [editor]
`enabled` · `true`
: web editor (`/edit/…`) and the saving API. The password is set in `.env` (`H6082_EDITOR_PASSWORD`), not here.

`autosave_ms` · `800`
: autosave delay after the last key press

`max_size_kb` · `1024`
: max. size of a saved file

Controls: ++ctrl+s++ saves at once, ++tab++ inserts 4 spaces. Live preview on the right. On a conflict the editor offers *reload from file* or *overwrite*.

## [api]
`allowed_hosts` · `["127.0.0.1", "localhost"]`
: hostname the server answers to (`Host`) and from which `/api` may be called (`Origin`). Applies to all pages. Add another name here when accessing the page through it.

## [checks]
`enabled` · `true`
: availability check for links with `{.check}` / `{check="…"}`

`interval_s` · `60`
: how often the status refreshes (the server keeps results 5 s shorter)

`timeout_s` · `4`
: timeout of a single check

`verify_tls` · `false`
: verify certificates. `false` = self-signed ones pass too (homelab); the check sends no data.

ICMP ping is not possible in the container, as it runs without root privileges. Use `tcp://host:port` instead.

## [history]
`enabled` · `true`
: change history of all `.md` files and `config.toml`. `{{history … demo}}` (made-up changes) works even when disabled.

`coalesce_min` · `5`
: edits within this many minutes of the last version are merged into one, so autosave does not create hundreds of versions

`max_versions` · `50`
: max. number of versions per file

`max_age_days` · `90`
: older versions are deleted. The 3 newest always stay.

A version is **the state of the file before a change**. Edits from the editor and from elsewhere (vim, git) are caught: the server checks the files every 2 s. Before a restore, the current state is saved as a new version, so a restore can be undone too. Version contents, diff and restore are behind the editor password. The `{{history}}` block shows only times, names and line counts.

## Read-only mode
`H6082_READONLY=1` turns the application into a public, read-only page — e.g. a demo on the internet:

- nothing can be saved: the editor, new files, deleting, notes, tasks, theme, language and history return `403`, and their controls are hidden
- content comes only from the image (`app/defaults/`): no volume, nothing to fill or overwrite
- live reload (`/events`), server stats (`/api/sys`) and the change history are off
- a visitor's theme and language are kept only in their own browser (cookie); the server stores nothing
- service status and RSS keep working, only for targets written in the image's md files

Run it with a read-only file system and no volume (see `h6082-deploy-demo`); even a bug in the application then has nowhere to write, and a restart is always clean.

## Demo mode
The `{{sys}}` and `{{history}}` blocks have a `demo` switch. With it they show **made-up data**, generated in the browser without asking the server. Handy for examples, documentation and public pages.

| block | demo | real data |
|---|---|---|
| server | `{{sys demo}}` | `{{sys}}` + `[system] enabled = true` |
| history | `{{history 5 demo}}` | `{{history 5}}` |

The examples in **demo** and **markdown** use demo mode, so they reveal neither server data nor the names of your files.

## [system]
`enabled` · `false`
: real values for `{{sys [parts…]}}` and the `/api/sys` endpoint. Off by default, because `/api/sys` is visible to anyone who can see the page. `{{sys demo}}` with made-up data works even when disabled.

`interval_s` · `5`
: refresh of the values in the page

`temps` · `[]`
: thermal zone types (`/sys/class/thermal/*/type`), e.g. `["x86_pkg_temp", "acpitz"]`. `[]` = automatic: `x86_pkg_temp` as CPU, otherwise the highest temperature.

`disks`
: list of `{ label, path }`. `path` is a directory **inside the container** that lies on the monitored disk.
```toml
disks = [
  { label = "/",       path = "/host/disk/root" },
  { label = "content", path = "/app/content" },
]
```
The container sees the root disk through the empty host directory `H6082_DISK_ROOT` from `.env`. Another disk = another empty directory in `volumes` (`:ro`). The container only learns the disk size and cannot see the directory contents.

The values come from the host (`/proc`, `/sys` are shared with the kernel). Network, processes and docker containers are left out on purpose: they would need `network_mode: host`, `pid: host` or the docker socket, which weakens the isolation.

## [rss]
`enabled` · `true`
: `{{rss URL [count]}}` blocks

`refresh_min` · `15`
: cache time. If the source fails, the last known state is shown.

`timeout_s` · `8`
: download timeout, the max. feed size is 2 MB

`default_limit` · `10`
: number of items when the shortcode does not say

## [code]
`pygments_style` · `"monokai"`
: colour scheme of code blocks for the **obsidian** theme, e.g. `monokai`, `dracula`, `one-dark`, `nord`, `gruvbox-dark`, `material`, `github-dark`, `solarized-dark`, `native`, `zenburn`. The other themes have their own scheme. An unknown name = `monokai` + a warning in the log.

`line_numbers` · `false`
: line numbers in all code blocks

`wrap` · `true`
: long code lines wrap; `false` = horizontal scrollbar

The background of code blocks is always `code_bg`, only the token colours come from the scheme.

# Look

## [layout]
`columns_fixed` · `0`
: `0` = number of columns by window width, `N` = always N columns

`column_min_width` · `"240px"`
: min. column width in automatic mode

`page_max_width` · `"1600px"`
: max. content width, `"none"` = full width

`padding` · `"14px"`
: page margin

`gap` · `"12px"`
: space between columns and below the tab bar

`block_gap` · `"10px"`
: vertical space between blocks in a column

`block_padding` · `"6px 10px 8px"`
: inner padding of a block (CSS padding: top, right/left, bottom)

`radius` · `"6px"`
: corner radius of blocks and tabs

`h3_indent` · `"2px"`
: indentation of `###` headings

`content_indent` · `"10px"`
: indentation of the content under `###`

Up to 640 px width there is always one column.

## [font]
`family` · JetBrains Mono
: CSS `font-family`. JetBrains Mono is bundled in the image. Any other font must be installed on the browser's system, e.g. `'"Fira Code", monospace'`.

`size` · `"13px"`
: base font size, everything else is derived from it

`line_height` · `"1.4"`
: line height

`block_title_transform` · `"none"`
: block titles: `none`, `uppercase`, `lowercase`, `capitalize`

# Colours

## Themes
The picker is in the Theme block on the h6082 page. A click on a tile writes the theme to `config.toml` as `[theme] default` (with the editor password), so it applies to every browser. All other lines and comments in the config stay unchanged.

| theme | type | code |
|---|---|---|
| `obsidian` | dark | `[code]` |
| `nord` | dark | nord |
| `dracula` | dark | dracula |
| `gruvbox-dark` | dark | gruvbox-dark |
| `solarized-dark` | dark | solarized-dark |
| `catppuccin-mocha` | dark | one-dark |
| `tokyo-night` | dark | one-dark |
| `obsidian-light` | light | friendly |
| `gruvbox-light` | light | gruvbox-light |
| `solarized-light` | light | solarized-light |
| `catppuccin-latte` | light | default |
| `paper` | light | default |
| `auto` | follows the OS | — |

`obsidian` = colours from `[colors]` (default). `auto` picks between `auto_dark` and `auto_light` according to the OS setting and switches live.

Preview without saving: `?theme=<theme>`, e.g. [/docs?theme=paper](/docs?theme=paper).

## [theme]
`default` · `"obsidian"`
: the active theme (can also be `"auto"`). Also set by the picker on the h6082 page.

`auto_dark` · `"obsidian"`
: theme for `auto` with a dark OS

`auto_light` · `"obsidian-light"`
: theme for `auto` with a light OS

## [themes.*]
A custom theme, or a tweak of a built-in one when you use its name. Keys as in `[colors]` plus:

`label`
: name in the picker

`scheme` · `"dark"`
: `dark` / `light`. Decides the group in the picker and the colours of browser controls (scrollbars, forms).

`pygments_style`
: code highlighting scheme

Missing colours are taken from `obsidian`.
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

## [colors] basics
| key | default | used for |
|---|---|---|
| `bg` | `#1e1e1e` | page background |
| `panel` | `#262626` | blocks, active tab |
| `border` | `#363636` | borders, tables, `---` |
| `text` | `#dcddde` | text |
| `muted` | `#999999` | bullets, quotes, inactive tabs |
| `accent` | `#a882ff` | active tab, checkboxes, selection |
| `h2` | `#a882ff` | block titles |
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
> Override `bg`, `panel`, `border`, `text`, `muted` and `code_bg`. Then adjust `h3`, `link` and `code_fg` so they keep enough contrast.
