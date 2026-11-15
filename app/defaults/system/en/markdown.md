#
##.
{{examples}}

---
#
##. `Structure`

---
#
## Tabs
Every file `content/pages/*.md` is one tab in the top bar.

The tab name is the file name without `.md`. A translation is a file `name.cs.md` or `name.en.md` and is shown according to the selected language.

- user tabs are on the left, their order is set by `[tabs] order`
- hidden tabs (`[tabs] hidden`) are reachable via `/<name>`
- the first user tab is at `/`
- create a new file on the [settings](/settings) page
- a link to another tab is a plain link to `/<name>`:

```md
[documentation](/documentation)
```

## Columns
A `#` line starts a new column, `---` a new row of columns. This whole page is built that way.
{{example columns.md}}
| syntax | result |
|---|---|
| `#` | column |
| `#+` | column 1.5× wider |
| `#++` | column 1.75× wider |
| `#-` | narrow column, half width |
| `#--` | very narrow column, quarter width |
| `#1.2` · `#0,8` | custom width ratio (decimal point or comma) |
| `#120px` · `#12em` · `#30%` | fixed width, the other columns in the row share the rest; percentages include the gaps, so `#25%` `#25%` `#50%` fill the row exactly |
| `---` | new row of columns (the line right before `#`); a lone `#` in a row is a full-width band |
| ` ##. heading ` | column heading without a frame, see Plain card |

- the text after `#` only helps you find your way in the file, it is not shown on the page
- widths are relative: the numbers in a row set the ratio, `#++` next to `#-` is 3.5× wider; narrow columns suit quick links or service status
- a column needs at least its number × `[layout] column_min_width`; what does not fit wraps to the next row and stretches
- the gap between `---` rows is the same as between columns (`[layout] row_gap`); a `/` line between `---` and `#` adds more
- a `---` not followed by `#` stays a horizontal line in the card
- number of columns: window width, or `[layout] columns_fixed`
- `#` inside a code block is ignored

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
---
# Full-width band
## News
…
```

## Hidden notes
A line starting with `//` is not rendered on the page.
{{example hidden-notes}}
Handy for reminders in the file. Inside a code block and in the middle of a line, `//` is plain text.

```md
// a note just for me
```

#
## Cards
`## Title` creates a framed card, like every box on this page.
{{example cards.md}}
Everything up to the next `##` or `#` belongs to the card.
Content before the first `##` in a column forms a card without a title, and so does a bare `##` without text.
`## Title {.fill}` stretches the card to the height of the tallest column in the row, so neighbouring cards end at the same level (the Author card on the [settings](/settings) page).

```md
## Repos
- [GitHub](https://github.com)
```

## Plain card
`##.` instead of `##` draws a card without a frame and background, like the yellow row headings on this page.
{{example plain-card}}
Handy for naming a column, but it can have content too, e.g. text right on the page. A bare `##.` without text = content without a frame or heading.
`code` in any heading has no frame of its own, only its colour stays.

```md
# Structure
##. `Structure`

## Tabs
…
```

## Editable cards
`##*` instead of `##` marks a card you can edit right on the page, without opening the editor.
{{example editable-card}}
Handy for small ongoing things: lists, tables, short texts.

- on hover a ✎ appears at the top right, a click opens the card's markdown in place
- ++ctrl+enter++ saves, ++esc++ cancels; smart typing and editor shortcuts work
- only this card is saved, the rest of the file stays unchanged
- if the card was changed elsewhere in the meantime, saving is refused and nothing is overwritten
- the title and new cards are changed in the editor; works only for your tabs and with the editor password

```md
##* Shopping list
- milk
- bread
```

#
##+ Foldable cards
A click on the heading folds the card and it stays folded next time. Try it on this card.
{{example foldable}}
`##-` instead of `##` is a card folded from the start, `##+` unfolded but foldable. A click on the heading (or ++enter++ on it) toggles it. The browser remembers the state per page and card, nothing is written to the file. Combines with `{.fill}` or `{.mobile}`.

```md
##- Archive
- old links

##+ This week
- …
```

## Subheadings
`###` structures the content inside a card.
{{example subheadings}}
The heading and the content below it are slightly indented (`[layout] h3_indent`, `content_indent`).

```md
### Languages
- [Rust](https://doc.rust-lang.org/std/)
```

## Smaller headings
`####` to `######` are small muted headings for little captions.
{{example subheadings}}
They have no indentation. Look: `[style.h4]` to `[style.h6]`.

```md
#### level 4 caption
##### level 5 caption
```

## Lines and paragraphs
Every line in the file is a line on the page, an empty line starts a paragraph.
{{example lines}}
- ++enter++ = new line, empty line = new paragraph with a gap
- a line with only `/` inserts an empty line, `//` two, `///` three…
- `/` outside a card (right below `#`, or above `##`) makes a gap between cards, between `---` and `#` a gap between rows of columns
- classic markdown behaviour (lines are joined) is restored by `[markdown] line_breaks = false`

No empty line is needed before a list, table, quote, code block or heading, nor after a table; it is added automatically.

```md
First line
second line
/
after an empty line

New paragraph.
```

---
#
//
##. `Text`

---
#
## Font styles
Bold, italic and strikethrough.
{{example type}}
The underscore variants work too: `__bold__` and `_italic_`.
In the editor: ++ctrl+b++, ++ctrl+i++, ++ctrl+shift+x++.

```md
**bold** · *italic* · ***both*** · ~~strikethrough~~
```

## Highlight
`==text==` puts a highlighter-style background behind a span.
{{example type}}
Colour: `mark_bg` in the theme, look: `[style.highlight]`. In the editor: ++ctrl+shift+h++.

```md
Text with a ==highlighted part==.
```

## Inline code
Text between backticks is code right in the line.
{{example inline-code}}
`#!language` at the start turns on syntax highlighting.
A backtick inside code: ``` `` a`b `` ```. In the editor: ++ctrl+e++.

```md
`docker ps`
`#!python print("hi")`
```

## Keys
`++ctrl+b++` draws a keyboard shortcut.
{{example keys}}
Keys are joined with `+`. Known names (`ctrl`, `alt`, `shift`, `cmd`, `win`, `tab`, `esc`, `up`, `f1`–`f24`, `page-up`, …) become key labels.

```md
++ctrl+shift+t++ · ++f5++
```

## Hints
`[?](text)` is an icon with a hint that shows on hover.
{{example keys}}
On mobile it shows on tap. `\n` in the text breaks the line. Any character can replace ⓘ (`[★](?…)`).
Look: `[style.tip]`. `[?](https://…)` stays a plain link.

```md
[?](hint text)
[★](?hint text)
```

#
## Abbreviations
`*[TOML]: …` explains an abbreviation on hover.
{{example footnotes}}
The definition can be anywhere in the column and applies to the whole column.

```md
Configuration in TOML.
*[TOML]: Tom's Obvious Minimal Language
```

## Brackets
Brackets can be coloured in the config, e.g. for side remarks (in parentheses).

Each type (`round`, `square`, `curly`, `angle`) has its own section, e.g. `[style.bracket_round] color = "muted"`. The default look is unchanged.

```md
Text (in parentheses) and [square] and {curly}.
```

## Escaping
A backslash before a character turns its formatting off.
{{example escaping}}
Handy when you want to write `*`, `#`, `[` or a backtick as they are.

```md
\*asterisks\*  \# hash  \[brackets\]
```

## Inline HTML
HTML in the text works: superscript and subscript, underline, custom styles.
{{example html}}
- `style="…"` on `<span>` or `<div>` = custom CSS (colour, background, border)
- markdown inside an HTML block is processed only if the block has the attribute `markdown="1"`
- `<details><summary>` is a foldable block

```html
<small>small</small> x<sup>2</sup> H<sub>2</sub>O <u>underline</u>
<span style="background:#a882ff33;border-radius:6px;padding:1px 8px">label</span>
```

## Gear
`{{gear}}` puts the settings icon into the text.
{{example keys}}
It is the same gear as in the bar, just as an icon (not a link). Handy in instructions and welcome texts.

```md
under {{gear}} at the top right
```

#
## Alignment and size
A `{: … }` line right below a paragraph aligns or enlarges it.
{{example alignment}}
| class | result |
|:--|:--|
| `.center` / `.right` | centre / right alignment |
| `.big` / `.huge` | bigger / large font |
| `.small` | smaller font |
| `.muted` | muted colour |

Classes can be combined and work for headings and lists too. On a heading, `{: … }` can be at the end of the line or on the line below. Custom style: `{: style="…" }`, see Attributes.

```md
Centred signpost
{: .center .big }

signature on the right
{: .right .muted }
```

## Phone or computer only
`{.mobile}` and `{.desktop}` show a card or paragraph only on a phone, or only on a computer.
{{example devices}}
The breakpoint is 640 px, the same as for stacking columns. After a `##` heading it applies to the whole card, below a paragraph only to that paragraph.

```md
## Tip for the phone {.mobile}
…

A paragraph for the computer only.
{: .desktop }
```

## Attributes
`{…}` after an element adds a colour, class, anchor or another attribute.
{{example attributes}}
You can add `{#id}`, `{.class}`, `{key=value}` and `{: style="…" }` after an element. On a heading, write the attributes at the end of the line or on a separate line right below it.

```md
Paragraph.
{: style="color:#00bfa5" }
**text**{: style="color:#ff9100" }
[maps](https://www.openstreetmap.org){target=_blank}
```

## Footnotes
`[^1]` in the text refers to a note listed at the bottom.
{{example footnotes}}
Footnotes appear at the end of the last card in the column. The identifier can be a word too (`[^source]`).

```md
A claim with a footnote[^1].
[^1]: Footnote text.
```

---
#
//
##. `Links and images`

---
#
## Links
`[text](address)` is a link, optionally with a title or with the address set aside.
{{example links}}
External links open in a new tab (`[page] links_new_tab`). In the editor: ++ctrl+k++, or paste a URL over selected text.

```md
[text](https://example.com)
[text](https://example.com "tooltip")
[text](/documentation)
[text][ref]
[ref]: https://example.com
```

## Autolinks
A bare address in the text is a link by itself.
{{example links}}
It is shown without `https://` and the trailing slash. A link to `http://` gets a warning mark, except for addresses on the local network (`192.168.…`, `*.local`, `*.lan`, `localhost`).

```md
<https://example.com>
https://example.com/path
<user@example.com>
```

#
## Protected e-mail
`{{email name domain}}` shows an e-mail address that bots will not find in the file.
{{example links}}
Name and domain are written separately, so neither the md nor the HTML contains the address with an at sign. JavaScript in the browser builds the readable address and the `mailto:` link. Works anywhere in the text.

```md
{{email name example.com}}
```

## Images
`![description](/media/file.svg)` embeds an image, a banner or a small icon.
{{example images.md}}
- save your own images to `content/media/` and embed them via `/media/<file>` (`svg png jpg webp gif avif ico`)
- an image alone in a paragraph stretches to the card width
- a card without a title that contains only an image is drawn without a frame, as a banner (the header of the settings page)
- set a smaller size with the `{width=…}` attribute
- images from the web (`https://…`) work too, but the browser loads them from a foreign server

A script inside an SVG never runs, not even when the image is opened directly.

```md
![valley](/media/foto-den.svg)
![icon](/media/ikona.svg){width=20}
[![](/media/ikona.svg){width=14} text](https://…)
```

---
#
//
##. `Lists and tasks`

---
#
## Bullet lists
`-` at the start of a line is a list item.
{{example bullets}}
Indent by 2 spaces to nest, in the editor ++tab++. Bullets are drawn as `›` (`[style.list] marker`). `*` and `+` work too.
In the editor: ++ctrl+shift+8++.

```md
- item
  - nested
```

## Numbered lists
`1.` at the start of a line is a numbered item.
{{example numbered}}
++enter++ at the end of an item adds the next number. A list can start at any number. In the editor: ++ctrl+shift+7++.

```md
1. first
2. second
   1. nested
```

#
## Tasks
`- [ ]` is a task with a checkbox, `- [x]` a done task.
{{example tasks}}
In your tabs, tasks can be edited right on the page:
- a click on the checkbox ticks or unticks the task
- ✕ (on hover) deletes the task including its subtasks
- the **+ new task** field adds a task to the end of the list

The change is written to the md file at once. Here in the documentation the tasks are read-only. In the editor: ++ctrl+shift+9++.

```md
- [x] done
- [ ] in progress
  - [ ] subtask
```

## Definition list
A term and `: explanation` below it.
{{example definitions}}
The term is on one line, the explanation on the next after `: `. There can be several explanations.

```md
TTL
: how long a DNS record is valid
```

#
## Due dates
`@date` at the end of a task shows a due-date label.
{{example due-dates}}
| syntax | due |
|:--|:--|
| `@2027-03-31` | fixed date |
| `@2026-11-20 14:00` | date and time |
| `@+3` · `@-2` | in 3 days · 2 days ago, counted from today (for templates and examples that should not age) |
| `@+0 14:00` | today at 14:00 |

Within a week the label is relative ("in 2 days", "yesterday"), further out a date. Past due it is red, within 3 days orange, on a done task grey. The browser computes it from today's date; the file keeps what you wrote, so the task can still be ticked and edited.

```md
- [ ] submit the annual report @2027-03-31
- [ ] meeting @2026-11-20 14:00
- [ ] renew the certificate @+2
```

---
#
//
##. `Card content`

---
#
## Tables
Cells are separated by `|`, below the header is a `|---|` row.
{{example table.md}}
The separator row sets the alignment: `:--` left, `--:` right, `:-:` centre. Cells may contain inline formatting.

```md
| service | port | status |
|:--|--:|:-:|
| home | 8088 | ✓ |
```

## Code blocks
Code between ```` ``` ```` is a separate block, coloured by language.
{{example code-block}}
- hover over the block: a copy button is at the top right
- language: `bash`, `python`, `yaml`, `toml`, `json`, `rust`, `nix`, `diff`, …
- `hl_lines="2 4-6"` highlights lines, `linenums="1"` numbers them
- colour scheme and line numbers globally: `[code]`

````md
```python hl_lines="2"
def hello(name):
    return f"hello {name}"
```
````

## Quotes
`>` at the start of a line is a quote, `>>` a nested one.
{{example quotes}}
++enter++ in the editor continues the quote, on an empty line it ends it.

```md
> A short quote or remark.
>> nested quote
```

#
## Callouts
A quote with a type like `[!tip]` is a coloured box with a title.
{{example callouts}}
Types: `note` · `tip` · `info` · `warning` · `danger`. Aliases from Obsidian and GitHub work too (`important`, `caution`, `question`, `bug`, `success`, …). Without a title the type is used as the title, a callout without content is just a coloured line.

```md
> [!tip] Title
> content
```

## Foldable callouts
`-` or `+` after the type makes the callout foldable.
{{example foldable-callouts}}
`-` = folded, `+` = unfolded but foldable.

```md
> [!info]- Folded
> content
```

## Admonition
`!!!` is a callout in MkDocs syntax.
{{example mkdocs}}
The content is indented by 4 spaces. The result is the same as a callout.

```md
!!! warning "Title"
    content indented by 4 spaces
```

#
## Details
`???` is a foldable block in MkDocs syntax.
{{example mkdocs}}
`???` = folded, `???+` = unfolded. The content is indented by 4 spaces.

```md
??? note "Folded"
    content
```

## Note
`{{note}}` … `{{/note}}` is a field you type into right on the page.
{{example note}}
- the text between the markers is plain text, markdown is not rendered in it
- in your tabs it saves itself ~0.8 s after the last change, the field grows with the text
- if the note was changed elsewhere in the meantime, saving is refused and nothing is overwritten
- writing requires the editor password, here in the documentation it is read-only

````md
{{note}}
milk, bread
call the plumber
{{/note}}
````

## Divider
`---` between empty lines draws a horizontal line.
{{example divider}}
An empty line must precede `---`, otherwise the previous line turns into a heading.

```md
above the line

---

below the line
```

---
#
//
##. `Live widgets`

---
#
## Service status
`{.check}` after a link shows with a coloured dot whether the service responds.
{{example status}}
| dot | status |
|:--|:--|
| 🟢 | OK |
| 🟠 | 4xx: running, but needs a login etc. |
| 🔴 | 5xx, timeout or unreachable |

- `{.check}` checks the link address over HTTP(S)
- `{check="…"}` is a custom target: `https://…` or `tcp://host:port`
- hover shows the status code, latency or error
- refreshed every `[checks] interval_s`
- made-up status for examples: [sample data](/documentation#sample-data)

Checks run from the server in the container. Services on the host: `host.docker.internal:<port>`. The server only checks targets written in md files.

```md
[GitHub](https://github.com){.check}
[NAS](http://nas.lan){check="tcp://192.168.1.50:22"}
```

#
## Server
`{{sys}}` shows the server's CPU, memory and disk usage.
{{example server}}
- parts: `cpu` `mem` `swap` `load` `temp` `uptime` `disk`, without parameters all are shown
- values refresh every `[system] interval_s` seconds
- the bar is orange from 70 %, red from 90 %

> [!info] Turning it on
> Set `[system] enabled = true` in `config.toml`. Off by default, because `/api/sys` is visible to anyone who can see the page. Made-up values for examples: [sample data](/documentation#sample-data).

```md
{{sys}}
{{sys cpu mem disk}}
```

## RSS
`{{rss URL}}` lists the latest articles from a feed.
{{example rss}}
- the whole line = one feed, the number = item count (default `[rss] default_limit`)
- RSS 2.0, RSS 1.0 and Atom
- 💬 = link to the comments, if the feed has them
- the server caches the feed for `[rss] refresh_min` minutes and shows the last known state if the source is down
- made-up titles for examples: [sample data](/documentation#sample-data)

```md
{{rss https://news.ycombinator.com/rss 5}}
```

#
## Change history
`{{history}}` lists the latest file edits.
{{example history}}
- latest changes: time, file, added and removed lines
- a click opens the diff with an option to restore the version (with the editor password)
- versions are created automatically by edits from the editor and from elsewhere, edits within 5 minutes are merged

The history shows the names of your files and when you edited them. Made-up changes for examples: [sample data](/documentation#sample-data).

```md
{{history}}
{{history 20}}
{{history demo.md 5}}
```

## Countdown
`{{countdown date}}` shows how long until a date, or how long since it.
{{example countdown}}
| syntax | shows |
|:--|:--|
| `{{countdown 2027-01-01}}` | "in 39 days", "tomorrow", "today", "3 days ago" |
| `{{countdown 2027-01-20 9:00}}` | with a time also "in 5 h" |
| `{{countdown 2026-11-12 days}}` | just the number of days ("3 days") |
| `{{countdown +12}}` | 12 days from today |

The browser computes it from its clock and refreshes it every minute, hover shows the full date. Works anywhere in the text.

```md
New Year {{countdown 2027-01-01}}.
Holiday {{countdown +12}}.
```

---
#
//
##. `Shortcodes`

---
#
## Shortcodes
A line containing **only** a shortcode is replaced by generated content, e.g. the Server, Change history and RSS cards above.

- `{{files}}`: list of files with *view* and *edit* buttons. `user` = only yours, `system` = documentation, configuration and markdown.
- `{{newfile}}`: form for a new `.md` file
- `{{theme}}`: theme tiles, a click saves `[theme] default`
- `{{lang}}`: language switch, saves `[page] lang`
- `{{email name domain}}`: protected e-mail
- `{{countdown date}}`: countdown to or since a date
- `{{gear}}`: settings gear in the text

`{{email}}`, `{{countdown}}` and `{{gear}}` also work mid-line. Shortcodes are not executed inside a code block.

```md
{{files}}
{{newfile}}
{{rss URL [count]}}
{{sys [parts…]}}
{{history [file] [count]}}
{{note}} … {{/note}}
{{theme}}
{{lang}}
{{email name domain}}
{{countdown date [time] [days]}}
{{gear}}
```
#-
