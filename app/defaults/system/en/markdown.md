#__
/

# Structure
## `Structure`

## Tabs
Every file `content/pages/*.md` is one tab in the top bar.
Link to another tab: [documentation](/docs)

```md
[documentation](/docs)
```
The tab name is the file name without `.md`. A translation is a file `name.cs.md` or `name.en.md` and is shown according to the selected language.

- user tabs are on the left, their order is set by `[tabs] order`
- hidden tabs (`[tabs] hidden`) are reachable via `/<name>`
- the first user tab is at `/`
- create a new file on the [h6082](/h6082) page

## Columns
Example: this whole page. Every column starts with a `#` line.

```md
# Dev
## Repos
…
#+ Wide column
## Servers
…
#- Narrow column
## Quick links
…
#__ Full-width band
## News
…
```
| syntax | result |
|---|---|
| `#` | column |
| `#+` | column 1.5× wider |
| `#++` | column 2× wider |
| `#-` | narrow column, half width |
| `#--` | very narrow column, quarter width |
| `#__` | full-width band below the previous columns |
| `` ## `heading` `` | column heading without a frame (a block with only a title, see Column heading) |

- the text after `#` only helps you find your way in the file, it is not shown on the page
- widths are relative: `#++` next to `#-` is four times wider; narrow columns suit quick links or service status
- columns that do not fit wrap to the next row and stretch
- number of columns: window width, or `[layout] columns_fixed`
- `#` inside a code block is ignored

## Blocks
Example: every framed box on this page.

```md
## Repos
- [GitHub](https://github.com)
```
`## Title` creates a framed block. Everything up to the next `##` or `#` belongs to it.
Content before the first `##` in a column forms a block without a title.
`## Title {.fill}` stretches the block to the height of the tallest column in the row, so neighbouring blocks end at the same level (the Author and app block on the [h6082](/h6082) page).

## Column heading
Example: the yellow headings `Structure`, `Text`, `Blocks`… above the columns of this page.

```md
# Structure
## `Structure`

## Tabs
…
```
A block that has only a title and nothing below it is drawn as a heading without a frame and background. Handy for naming a column.
`code` in any heading has no frame of its own, only its colour stays.

## Editable blocks
Example: in the [demo-student](/demo-student) tab, the blocks This week, Exam period, Bachelor's thesis and Glossary of concepts have ✎.

```md
##* Shopping list
- milk
- bread
```
`##*` instead of `##` marks a block that can be edited right on the page, without opening the editor. Handy for small ongoing things: lists, tables, short texts.

- on hover a ✎ appears at the top right, a click opens the block's markdown in place
- ++ctrl+enter++ saves, ++esc++ cancels; smart typing and editor shortcuts work
- only this block is saved, the rest of the file stays unchanged
- if the block was changed elsewhere in the meantime, saving is refused and nothing is overwritten
- the title and new blocks are changed in the editor; works only for your tabs and with the editor password

## Subheadings
### Languages
- [Rust](https://doc.rust-lang.org/std/)
- [Python](https://docs.python.org/3/)

### Tools
- [Docker](https://docs.docker.com)

```md
### Languages
- [Rust](https://doc.rust-lang.org/std/)
```
Structure the content inside a block. The heading and the content below it are slightly indented (`[layout] h3_indent`, `content_indent`).

## Smaller headings
#### level 4 caption
##### level 5 caption
###### level 6 caption

```md
#### level 4 caption
##### level 5 caption
```
Small muted headings without indentation, handy for little captions. Look: `[style.h4]` to `[style.h6]`.

## Lines and paragraphs
First line
second line
/
after an empty line

New paragraph.

```md
First line
second line
/
after an empty line

New paragraph.
```
- ++enter++ = new line, empty line = new paragraph with a gap
- a line with only `/` inserts an empty line, `//` two, `///` three…
- `/` outside a block (right below `#`, or above `##`) makes a gap between blocks
- classic markdown behaviour (lines are joined) is restored by `[markdown] line_breaks = false`

No empty line is needed before a list, table, quote or code block, it is added automatically.

## Hidden comments
This block contains a comment you cannot see.
// this is not shown on the page

```md
// a note just for me
```
A line starting with `//` is not rendered. Handy for reminders in the file. Inside a code block and in the middle of a line, `//` is plain text.

# Text
## `Text`

## Font styles
**bold** · *italic* · ***bold italic*** · ~~strikethrough~~

```md
**bold** · *italic* · ***both*** · ~~strikethrough~~
```
The underscore variants work too: `__bold__` and `_italic_`.
In the editor: ++ctrl+b++, ++ctrl+i++, ++ctrl+shift+x++.

## Highlight
Text with a ==highlighted part==.

```md
Text with a ==highlighted part==.
```
Colour: `mark_bg` in the theme, look: `[style.highlight]`. In the editor: ++ctrl+shift+h++.

## Inline code
The command `docker ps` or `#!python print("hi")`

```md
`docker ps`
`#!python print("hi")`
```
`#!language` at the start turns on syntax highlighting.
A backtick inside code: ``` `` a`b `` ```. In the editor: ++ctrl+e++.

## Keys
++ctrl+shift+t++ · ++alt+tab++ · ++cmd+space++ · ++f5++

```md
++ctrl+shift+t++ · ++f5++
```
Keys are joined with `+`. Known names (`ctrl`, `alt`, `shift`, `cmd`, `win`, `tab`, `esc`, `up`, `f1`–`f24`, `page-up`, …) become key labels.

## Hints
An icon with a hint [?](Shows on hover or on tap.) and with a custom icon [★](?Any character instead of ⓘ.)

```md
[?](hint text)
[★](?hint text)
```
The hint shows on hover, on mobile on tap. `\n` in the text breaks the line.
Look: `[style.tip]`. `[?](https://…)` stays a plain link.

## Abbreviations
Configuration in TOML, styles in CSS.

```md
Configuration in TOML.
*[TOML]: Tom's Obvious Minimal Language
```
Hover over an abbreviation. The definition can be anywhere in the column and applies to the whole column.

*[TOML]: Tom's Obvious Minimal Language
*[CSS]: Cascading Style Sheets

## Brackets
Text (in parentheses) and [square] and {curly}.

```md
Text (in parentheses) and [square] and {curly}.
```
Each bracket type can be coloured in the config, e.g. `[style.bracket_round] color = "muted"` for side remarks. The default look is unchanged.

## Alignment and size
Centred signpost
{: .center .big }

signature on the right
{: .right .muted }

```md
Centred signpost
{: .center .big }

signature on the right
{: .right .muted }
```
A `{: … }` line right below a paragraph adds classes to it:

| class | result |
|:--|:--|
| `.center` / `.right` | centre / right alignment |
| `.big` / `.huge` | bigger / large font |
| `.small` | smaller font |
| `.muted` | muted colour |

Classes can be combined and work for headings and lists too. Custom style: `{: style="…" }`, see Attributes.

## Inline HTML
<small>small text</small> · x<sup>2</sup> · H<sub>2</sub>O · <u>underline</u>

```html
<small>small</small> x<sup>2</sup> H<sub>2</sub>O <u>underline</u>
```
Markdown inside an HTML block is processed only if the block has the attribute `markdown="1"`.

## Escaping
\*asterisks\*, \# hash, \[brackets\], \`backtick\`

```md
\*asterisks\*  \# hash  \[brackets\]
```
A backslash before a character turns its formatting off.

## Footnotes
A claim with a footnote[^1] and another one[^long].

```md
A claim with a footnote[^1].
[^1]: Footnote text.
```
Footnotes appear at the end of the last block in the column.

[^1]: Footnote text.
[^long]: The identifier can be a word, too.

# Links and lists
## `Links and lists`

## Links
[plain link](https://example.com) · [with a tooltip](https://example.com "title on hover") · [another tab](/docs) · [with a reference][ref]

[ref]: https://example.com

```md
[text](https://example.com)
[text](https://example.com "tooltip")
[text](/docs)
[text][ref]
[ref]: https://example.com
```
External links open in a new tab (`[page] links_new_tab`). In the editor: ++ctrl+k++, or paste a URL over selected text.

## Autolinks
<https://example.com> · https://example.com/path · <user@example.com>

```md
<https://example.com>
https://example.com/path
<user@example.com>
```
A bare address is shown without `https://` and the trailing slash. A link to `http://` gets a warning mark, except for addresses on the local network (`192.168.…`, `*.local`, `*.lan`, `localhost`).

## Protected e-mail
Write to me: {{email name example.com}}

```md
{{email name example.com}}
```
Name and domain are written separately, so neither the md nor the HTML contains the address with an at sign. JavaScript in the browser builds the readable address and the `mailto:` link. Works anywhere in the text.

## Images
![h6082](/media/demo-hero.svg)

![logo](/static/img/logo.svg){width=20} icon before text · [![](/static/img/logo.svg){width=14} link with an icon](https://example.com)

```md
![h6082](/media/demo-hero.svg)
![logo](/media/icon.svg){width=20}
[![](/media/icon.svg){width=14} text](https://…)
```
- save your own images to `content/media/` and embed them via `/media/<file>` (`svg png jpg webp gif avif ico`)
- an image alone in a paragraph stretches to the block width
- a block without a title that contains only an image is drawn without a frame, as a banner (the header of the h6082 page)
- set a smaller size with the `{width=…}` attribute
- images from the web (`https://…`) work too, but the browser loads them from a foreign server

A script inside an SVG never runs, not even when the image is opened directly.

## Bullet lists
- item
- item
  - nested
    - next level

```md
- item
  - nested
```
Indent by 2 spaces to nest, in the editor ++tab++. Bullets are drawn as `›` (`[style.list] marker`). `*` and `+` work too.
In the editor: ++ctrl+shift+8++.

## Numbered lists
1. first
2. second
   1. nested
3. third

```md
1. first
2. second
   1. nested
```
++enter++ at the end of an item adds the next number. A list can start at any number. In the editor: ++ctrl+shift+7++.

## Tasks
- [x] done
- [ ] in progress
  - [x] subtask
  - [ ] subtask

```md
- [x] done
- [ ] in progress
  - [ ] subtask
```
In your tabs, tasks can be edited right on the page:
- a click on the checkbox ticks or unticks the task
- ✕ (on hover) deletes the task including its subtasks
- the **+ new task** field adds a task to the end of the list

The change is written to the md file at once. Here in the documentation the tasks are read-only. In the editor: ++ctrl+shift+9++.

## Definition list
TTL
: how long a DNS record is valid

MTU
: max. packet size
: typically 1500 B

```md
TTL
: how long a DNS record is valid
```
The term on one line, the explanation on the next after `: `. There can be several explanations.

# Blocks
## `Blocks`

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
The separator row sets the alignment: `:--` left, `--:` right, `:-:` centre. Cells may contain inline formatting.

## Code blocks
```python hl_lines="2"
def hello(name):
    return f"hello {name}"
```

````md
```python hl_lines="2"
def hello(name):
    return f"hello {name}"
```
````
- hover over the block: a copy button is at the top right
- language: `bash`, `python`, `yaml`, `toml`, `json`, `rust`, `nix`, `diff`, …
- `hl_lines="2 4-6"` highlights lines, `linenums="1"` numbers them
- colour scheme and line numbers globally: `[code]`

## Quotes
> A short quote or remark.
>> nested quote

```md
> A short quote or remark.
>> nested quote
```
++enter++ in the editor continues the quote, on an empty line it ends it.

## Callouts
> [!note]
> Without a title, the type is used as the title.

> [!tip] Tip
> The content can contain **markdown**, `code` and [links](https://example.com).

> [!warning] Warning

> [!danger] Danger

```md
> [!tip] Title
> content
```
Types: `note` · `tip` · `info` · `warning` · `danger`. Aliases from Obsidian and GitHub work too (`important`, `caution`, `question`, `bug`, `success`, …). A callout without content is just a coloured line.

## Collapsible callouts
> [!info]- Collapsed (click)
> Hidden content.

> [!tip]+ Expanded
> Can be collapsed.

```md
> [!info]- Collapsed
> content
```
`-` after the type = collapsed, `+` = expanded but collapsible.

## Admonition
!!! warning "Title"
    Alternative callout syntax.

```md
!!! warning "Title"
    content indented by 4 spaces
```
The same as a callout, just in MkDocs syntax.

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
{{note}}
milk, bread
call the plumber
{{/note}}
````
- the text between `{{note}}` and `{{/note}}` is plain text, markdown is not rendered in it
- in your tabs you type right on the page and it saves itself ~0.8 s after the last change
- if the note was changed elsewhere in the meantime, saving is refused and nothing is overwritten
- writing requires the editor password, here in the documentation it is read-only

## Divider
above the line

---

below the line

```md
above the line

---

below the line
```
An empty line must precede `---`, otherwise the previous line turns into a heading.

## Attributes
A paragraph with its own colour.
{: style="color:#00bfa5" }

**bold orange**{: style="color:#ff9100" }

```md
Paragraph.
{: style="color:#00bfa5" }
**text**{: style="color:#ff9100" }
```
You can add `{#id}`, `{.class}`, `{key=value}` and `{: style="…" }` after an element.

#__
## `Live widgets`

# Monitoring
## `Monitoring`

## Service status
- [GitHub](https://github.com){.check}
- [Hacker News](https://news.ycombinator.com){.check}
- [non-existent](https://nonexistent.invalid){.check}

```md
[GitHub](https://github.com){.check}
[NAS](http://nas.lan){check="tcp://192.168.1.50:22"}
```
A coloured dot shows whether the service responds: 🟢 OK · 🟠 4xx (running, but needs a login etc.) · 🔴 5xx, timeout or unreachable.

- `{.check}` checks the link address over HTTP(S)
- `{check="…"}` is a custom target: `https://…` or `tcp://host:port`
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
- parts: `cpu` `mem` `swap` `load` `temp` `uptime` `disk`, without parameters all are shown
- values refresh every `[system] interval_s` seconds
- the bar is orange from 70 %, red from 90 %

> [!info] Demo mode
> The example above shows **made-up values** (`demo`), generated by the browser; the server is not asked at all.
> Real values: set `[system] enabled = true` in `config.toml` and remove `demo` from the block. Off by default, because `/api/sys` is visible to anyone who can see the page.

# Feeds and history
## `Feeds and history`

## RSS
{{rss https://news.ycombinator.com/rss 5}}

```md
{{rss https://news.ycombinator.com/rss 5}}
```
- the whole line = one feed, the number = item count (default `[rss] default_limit`)
- RSS 2.0, RSS 1.0 and Atom
- 💬 = link to the comments, if the feed has them
- the server caches the feed for `[rss] refresh_min` minutes and shows the last known state if the source is down

## Change history
{{history 5 demo}}

```md
{{history}}
{{history 20}}
{{history demo-family.md 5}}
```
- latest changes: time, file, added and removed lines
- a click opens the diff with an option to restore the version (with the editor password)
- versions are created automatically by edits from the editor and from elsewhere, edits within 5 minutes are merged

> [!info] Demo mode
> The example above shows **made-up changes** (`demo`). The real history would show the names of your files and when you edited them. Just remove `demo` from the block.

#+ Editor and demos
## `Editor and demos`

## Editor suggestions
{{livedemo 8}}
{{scene hints.md}}
##* Dates
**1 Mar** insurance
> [!tip] Tip
> The editor suggests shortcodes too.
{{rss https://news.ycombinator.com/rss 3}}
{{/livedemo}}

```md
#        → columns and blocks: #+ #- #__ ## ##* …
{{       → shortcodes: {{rss URL 5}}, {{note}} …
> [!     → callouts: tip, warning, danger … folded too
{.       → classes: .check .center .big .fill …
](/      → names of your pages
- [      → a task
```
- the list appears only after these openings, not on every word
- ++arrow-up++ ++arrow-down++ choose, ++enter++ or ++tab++ confirm, ++esc++ closes; without the list ++enter++ works as usual
- for a shortcode the parameter (`URL`) gets selected after confirming, just type over it
- works in the editor and when editing a `##*` block on the page, not on touch devices; turn off: `[editor] suggest = false`

## Live demo
{{livedemo 12}}
#
## Links
- [Maps](https://www.openstreetmap.org)
#
## Today
- [ ] shopping
{{/livedemo}}

```md
{{livedemo 12}}
#
## Links
- [Maps](https://www.openstreetmap.org)
#
## Today
- [ ] shopping
{{/livedemo}}
```
- an editor window "types" the markdown between the markers and the preview below redraws after each line
- the number = length of one run in seconds (default 30), then a 4 s pause and again from the start
- ❚❚ in the window bar stops the animation; off-screen it waits by itself, with reduced motion turned on in the system the finished state shows right away
- the content is only a demo: its tasks can't be ticked and don't count among the page's tasks

# Shortcode overview
## `Shortcode overview`

## Shortcodes
Example: the Server, Change history and RSS blocks on the left.

```md
{{files}}
{{newfile}}
{{rss URL [count]}}
{{sys [parts…] [demo]}}
{{history [file] [count] [demo]}}
{{note}} … {{/note}}
{{livedemo [seconds]}} … {{/livedemo}}
{{theme}}
{{lang}}
{{email name domain}}
```
A line containing **only** a shortcode is replaced by generated content.

- `{{files}}`: list of files with *view* and *edit* buttons. `user` = only yours, `system` = documentation, configuration and markdown.
- `{{newfile}}`: form for a new `.md` file
- `{{livedemo [seconds]}} … {{/livedemo}}`: an animated editor window with a live preview, see [Live demo](#live-demo)
- `{{theme}}`: theme tiles, a click saves `[theme] default`
- `{{lang}}`: language switch, saves `[page] lang`
- `{{email name domain}}`: protected e-mail, the only one that also works mid-line

Shortcodes are not executed inside a code block.
