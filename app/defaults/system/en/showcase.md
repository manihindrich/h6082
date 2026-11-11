# Structure

## Tabs
Every file `content/pages/*.md` is one tab in the top bar. The tab name = the file name without `.md`. A translation of a tab is a file `name.cs.md` or `name.en.md`; it is shown according to the language.
- user tabs are on the left, their order is set by `[tabs] order`
- `h6082` is on the right (`[page] about_tab`)
- hidden tabs (`[tabs] hidden`) are reachable via `/<name>`
- the first user tab is at `/`
- a link to another tab: `[config](/docs)` → [config](/docs)
- create and edit new files on the [h6082](/h6082) page

## Columns #
A line `# Name` starts a new column. A column is invisible, it just stacks blocks. The name helps you find your way in the file.
```md
# Dev
## Repos
…
# Infra
## Servers
…
```
- columns go from left to right in file order
- text before the first `#` belongs to the first column
- columns per row: window width, or `columns_fixed`
- `#` inside a code block is ignored

## Blocks ##
`## Title` creates a framed block. Everything up to the next `##` or `#` belongs to the block.
```md
## Repos
- [GitHub](https://github.com)
```
Content before the first `##` in a column forms a block without a title. Title letter case: `block_title_transform`.

## Subheadings ###
Structure the content inside a block. They are slightly indented and their content is indented a bit more (`h3_indent`, `content_indent`).
### Languages
- [Rust](https://doc.rust-lang.org/std/)
- [Python](https://docs.python.org/3/)
### Tools
- [Docker](https://docs.docker.com)
```md
### Languages
- [Rust](https://…)
```

## Headings #### to ######
Small muted headings without indentation, handy for little captions.
#### level 4 caption
##### level 5 caption
```md
#### level 4 caption
```

## Paragraphs and line breaks
Consecutive lines are joined into one paragraph.
An empty line starts a new paragraph.

A line ending with two spaces  
breaks. `<br>` does the same.<br>Like this.
```md
first line··
broken line
```
`··` stands for two spaces.

No empty line is needed before a list, table, quote or code block, it is added automatically.

# Text

## Font styles
**bold** · *italic* · ***bold italic*** · ~~strikethrough~~
```md
**bold** · *italic* · ***both*** · ~~strikethrough~~
```
The underscore variants work too: `__bold__` and `_italic_`.

## Highlight
Text with a ==highlighted part==. The colour is set by `mark_bg`.
```md
Text with a ==highlighted part==.
```

## Inline code
The command `docker ps` or the path `/etc/hosts`.
Inline code with syntax highlighting: `#!python print("hi")`
```md
`docker ps`
`#!python print("hi")`
```
A backtick inside code: ``` `` a`b `` ```

## Keys
++ctrl+shift+t++ · ++alt+tab++ · ++cmd+space++ · ++f5++ · ++enter++
```md
++ctrl+shift+t++  ++f5++  ++enter++
```
Known names (`ctrl`, `alt`, `shift`, `cmd`, `win`, `tab`, `esc`, `up`, `down`, `f1`–`f24`, `page-up`, …) become key labels. Keys are joined with `+`.

## Abbreviations
Configuration in TOML, styles in CSS. Hover over an abbreviation.
```md
Configuration in TOML.
*[TOML]: Tom's Obvious Minimal Language
```
The definition can be anywhere in the column and applies to the whole column.

*[TOML]: Tom's Obvious Minimal Language
*[CSS]: Cascading Style Sheets

## Inline HTML
<small>small text</small> · x<sup>2</sup> · H<sub>2</sub>O · <span style="color:#ff9100">colour</span> · <u>underline</u>
```html
<small>small</small> x<sup>2</sup> H<sub>2</sub>O
<span style="color:#ff9100">colour</span>
```
Markdown inside an HTML block is processed only if the block has the attribute `markdown="1"`.

## Escaping
A backslash before a character turns its formatting off: \*asterisks\*, \# hash, \[brackets\], \`backtick\`.
```md
\*asterisks\*  \# hash  \[brackets\]
```

## Footnotes
A claim with a footnote[^1] and another one[^long].
```md
A claim with a footnote[^1].
[^1]: Footnote text.
```
Footnotes appear at the end of the last block of the column.

[^1]: Footnote text.
[^long]: The identifier can be a word, too.

# Links and lists

## Links
- [plain link](https://example.com)
- [with a tooltip](https://example.com "title on hover")
- [relative, another tab](/docs)
- [reference link][ref]

[ref]: https://example.com
```md
[text](https://example.com)
[text](https://example.com "tooltip")
[text](/docs)
[text][ref]
[ref]: https://example.com
```
External links open in a new tab (`links_new_tab`).

## Autolinks
- <https://example.com>
- bare URL: https://example.com/path
- e-mail: <user@example.com>
```md
<https://example.com>
https://example.com/path
<user@example.com>
```

## Protected e-mail
Write to me: {{email name example.com}}
```md
{{email name example.com}}
```
Name and domain are written separately, so neither the md nor the HTML contains the address with an at sign. JavaScript in the browser builds the readable address and the `mailto:` link. Works anywhere in the text, even mid-line.

## Images
![h6082](/media/demo-hero.svg)

![logo](/static/img/logo.svg){width=20} icon before text · [![](/static/img/logo.svg){width=14} link with an icon](https://example.com)
```md
![h6082](/media/demo-hero.svg)
![logo](/media/icon.svg){width=20}
[![](/media/icon.svg){width=14} text](https://…)
```
- **own images**: save them to `content/media/` and embed via `/media/<file>`. Allowed: `svg png jpg webp gif avif ico`.
- an image alone in a paragraph stretches to the block width and gets rounded corners
- set a smaller size with the `{width=…}` attribute
- images from the web (`https://…`) work too, but the browser then loads them from a foreign server

Images are sent with a strict CSP (`sandbox`), so a script inside an SVG never runs, not even when opened directly.

## Bullet lists
- item
- item
    - nested (4 spaces)
        - next level
```md
- item
    - nested
```
Bullets are drawn as `›`. `*` and `+` work too.

## Numbered lists
1. first
2. second
    1. nested
3. third

5. starts at five
6. sixth
```md
1. first
    1. nested
5. starts at five
```

## Tasks
- [x] done
- [ ] in progress
    - [x] subtask
    - [ ] subtask
```md
- [x] done
- [ ] in progress
```
In user tabs, tasks can be edited right on the page:
- a click on the checkbox toggles the task
- ✕ (appears on hover) deletes the task including its subtasks
- the **+ new task** field below the list adds a task to the end of the list (++enter++)

The change is written to the md file at once. Here in the documentation the tasks are read-only.

## Definition list
TTL
: how long a DNS record is valid

MTU
: max. packet size
: typically 1500 B
```md
TTL
: how long a record is valid
```

# Blocks

## Tables
| service | port | status |
|:--|--:|:-:|
| home | 8088 | ✓ |
| grafana | 3000 | ~~off~~ |
```md
| service | port | status |
|:--|--:|:-:|
| home | 8088 | ✓ |
```
The separator row sets the column alignment: `:--` left, `--:` right, `:-:` centre. Cells may contain inline formatting.

## Code blocks
```python hl_lines="2"
def hello(name):
    return f"hello {name}"
```
````md
```python hl_lines="2"
def hello(name): ...
```
````
- language: `bash`, `python`, `yaml`, `toml`, `json`, `rust`, `nix`, `diff`, …
- `hl_lines="2 4-6"` highlights lines
- `linenums="1"` line numbers in one block
- colour scheme and line numbers globally: section `[code]`

## Quotes
> A short quote or remark.
>> nested quote
```md
> quote
>> nested
```

## Callouts
> [!note]
> Without a title, the type is used as the title.

> [!tip] Tip
> The content can contain **markdown**, `code` and [links](https://example.com).

> [!info] Info

> [!warning] Warning

> [!danger] Danger
```md
> [!tip] Title
> content
```
Colours: `note` · `tip` · `info` · `warning` · `danger`. Aliases from Obsidian and GitHub work too (`important`, `caution`, `question`, `bug`, `success`, …). A callout without content is just a coloured line.

## Collapsible callouts
> [!info]- Collapsed (click)
> Hidden content.

> [!tip]+ Expanded
> Can be collapsed.
```md
> [!info]- Collapsed
> [!tip]+ Expanded
```

## Admonition
!!! warning "Title"
    Alternative callout syntax. The content is indented by 4 spaces.
```md
!!! warning "Title"
    content
```

## Details
??? note "Collapsed block"
    The content shows after a click.

???+ tip "Open block"
    `???+` = expanded by default.
```md
??? note "Collapsed"
    content
```

## Note
{{note}}
An editable note. The field grows downwards with the text.
The text is saved back into the md file.
{{/note}}
````md
## Shopping
{{note}}
milk, bread
call the plumber
{{/note}}
````
- the text between `{{note}}` and `{{/note}}` is plain text, markdown is not rendered in it
- in user tabs you can type right on the page. It saves itself ~0.8 s after the last change, the status is at the bottom right.
- the page does not reload while you type. Changes from elsewhere load once you leave the field.
- if the note was changed elsewhere in the meantime, saving is refused and nothing is overwritten
- writing requires the editor password
- here in the documentation the note is read-only

## Divider
above the line

---

below the line
```md
text

---

text
```
An empty line must precede `---`. Otherwise the previous line turns into a heading.

## Attributes
A paragraph with its own colour.
{: style="color:#00bfa5" }

**bold orange**{: style="color:#ff9100" }
```md
Paragraph.
{: style="color:#00bfa5" }
**text**{: style="color:#ff9100" }
![](/img.svg){width=16}
```
You can add `{#id}`, `{.class}`, `{key=value}` and `{: style="…" }` after an element.

# Live widgets

## Service status
A coloured dot before the link shows whether the service responds.
- [GitHub](https://github.com){.check}
- [Hacker News](https://news.ycombinator.com){.check}
- [non-existent](https://nonexistent.invalid){.check}
- [h6082 via TCP](/h6082){check="tcp://127.0.0.1:8080"}
```md
[GitHub](https://github.com){.check}
[NAS](http://nas.lan){check="tcp://192.168.1.50:22"}
```
- `{.check}`: HTTP(S) check of the link address
- `{check="…"}`: own target, `https://…` or `tcp://host:port`
- 🟢 response < 400 · 🟠 4xx (running, but needs a login etc.) · 🔴 5xx, timeout or unreachable
- hover shows the status code, latency or error
- refreshed every `[checks] interval_s`

Checks run from the server in the container. Services on the host: `host.docker.internal:<port>`. The server only checks targets written in md files.

## Server
{{sys demo}}
```md
{{sys}}
{{sys cpu mem disk}}
{{sys demo}}
```
> [!info] Demo mode
> The example above shows **made-up values** (`demo`), no real server data here. The values are generated in the browser and the server is not asked at all. Works even with `[system] enabled = false`.
>
> **Switching to real values:** 1) set `[system] enabled = true` in `config.toml`, 2) remove `demo` from the block, e.g. `{{sys cpu mem disk}}`.
- parts: `cpu` `mem` `swap` `load` `temp` `uptime` `disk`, without parameters all are shown
- `demo` shows made-up data in the browser without asking the server. Handy for examples and public pages.
- real values need `[system] enabled = true`. Off by default, because `/api/sys` is visible to anyone who can see the page.
- values refresh every `[system] interval_s` seconds, not on a hidden browser tab
- it is the host: the container reads `/proc` and `/sys`, shared with the host
- disks according to `[system] disks`. The container only sees empty directories mounted from the host, no data.
- bar: orange from 70 %, red from 90 %

Processes and docker containers are left out on purpose. They would need a weaker container isolation (`pid: host`, docker socket).

## Change history
{{history 5 demo}}
```md
{{history}}
{{history 20}}
{{history demo.md 5}}
{{history 5 demo}}
```
> [!info] Demo mode
> The example above shows **made-up changes** (`demo`): invented files and times, no request to the server. The real history would show the names of your files and when you edit them.
>
> **Switching to the real history:** remove `demo` from the block, e.g. `{{history 5}}`. `[history] enabled = true` is the default.
- latest changes: time, file, added and removed lines
- a click opens the diff with an option to restore the version (with the editor password)
- versions are created automatically by edits from the editor and from elsewhere. Edits within 5 minutes are merged.
- all versions of a file are in the editor under the **history** link

## RSS
{{rss https://news.ycombinator.com/rss 8}}
```md
{{rss https://news.ycombinator.com/rss 8}}
```
- the whole line = one feed, the number = item count (default `[rss] default_limit`)
- RSS 2.0, RSS 1.0 and Atom
- 💬 = link to the comments, if the feed has them (HN does)
- the server caches the feed for `[rss] refresh_min` minutes. If the source is down, the last known state is shown.
- the page renders at once, the feed loads afterwards

## Shortcodes
A line containing **only** a shortcode is replaced by generated content.
```md
{{files}}
{{files user}}
{{newfile}}
{{rss URL [count]}}
{{sys [parts…] [demo]}}
{{history [file] [count] [demo]}}
{{note}} … {{/note}}
{{lang}}
{{email name domain}}
```
- `{{files}}`: list of `.md` files and `config.toml` with editor links. The `system` variant shows only system files, `user` only yours (with a ✕ delete button).
- `{{newfile}}`: form to create a new `.md`
- `{{rss …}}`: feed block (see RSS)
- `{{sys …}}`: server stats (see Server), `demo` = made-up data
- `{{note}}` … `{{/note}}`: editable note (see Note)
- `{{history …}}`: latest file changes, `demo` = made-up data
- `{{lang}}`: language switch, saves `[page] lang` to the config
- `{{email name domain}}`: protected e-mail, the only one that also works mid-line

Shortcodes are not executed inside a code block or in the middle of a line.
