
---
#-
## 📱 Phone tip {.mobile}
Open the examples on a computer too: you will see the editor and the result side by side and understand better how markdown turns into a page.

The page itself is optimized for phones, so afterwards feel free to use it on mobile only.

##+ Examples
Examples of the markdown this homepage is written in

- [text formatting](#scene:formatting.md)
- [working with columns](#scene:columns.md)
- [cards and headings](#scene:cards.md)
- [lists](#scene:lists.md)
- [tasks](#scene:tasks.md)
- [table](#scene:table.md)
- [code block](#scene:code.md)
- [quotes and callouts](#scene:callouts.md)
- [note on the page](#scene:note.md)
- [images](#scene:images.md)
- [live widgets](#scene:live-widgets.md)
- [text appearance, HTML and CSS](#scene:appearance.md)
- [lines, notes, abbreviations](#scene:text.md)

##+ Demo tab
You might want to see what a homepage could actually look like. Everything can be adapted to whatever you need, but a rough sketch of the most basic features is in the [demo tab](/demo).

##- Want to know more?
The complete documentation with examples is always in [markdown.md](/markdown).

More useful information about the app is in the [documentation](/documentation). The gateway to everything is [settings](/settings), hidden in the top right corner under {{gear}}.

##- Hide this tab
You can hide the [Examples](/examples) tab with the switch in the header of the [markdown documentation](/markdown).

You can remove other tabs by opening them for editing in [settings](/settings) ({{gear}}) and choosing delete in the editor header.

#++
##
{{livedemo 0.75}}

{{scene formatting.md}}
{{part type}}
#
##. `✍️ Formatting`
---
#
##
**bold** · *italic* · ***both***
~~strikethrough~~ · ==highlighted==
{{part keys}}
#
##
keys ++ctrl+b++
tooltip [?](shows on mouse hover)
custom icon [★](?any character can replace ⓘ)
settings under {{gear}} in the top right
{{hover 1}}
{{hover 2}}
{{part links}}
#
##
link https://code.nolog.cz/hindrich/h6082
nice link [h6082](https://code.nolog.cz/hindrich/h6082)
with a title [h6082](https://code.nolog.cz/hindrich/h6082 "title in quotes, shown on mouse hover")
another tab [documentation](/documentation)
with a reference [h6082][repo], the address is separately below
e-mail {{email name example.com}}

[repo]: https://code.nolog.cz/hindrich/h6082

{{scene columns.md}}
# Column
## Card in the 1st column
---
/
{{after ## Card in the 1st column}}
`---` makes a line break. This column is alone here, so its content spans the full width.
{{end}}

#
## \#
default column width (`#`) is `1/x`
`x`=number of columns
#+
## #`+`
you can add a `+` or `-` mark to the column
`#+` equals `1.5x` the default column
#-
## #`-`
`#-` is the opposite, `0.5x`
---
#
## \#
`1x` again for comparison
#++
## #`++`
2x `+` for `1.75x`
#--
## #`--`
`0.25x`
---
/
# 
## custom relative width
You can also set the column width with a number after `#`
---
#1.2
## #`1.2`
i.e. 1.2x
#1.8
## #`1.8`
i.e. 1.8x
---
#1.11
## #`1.11`
i.e. 1.11x
#0.35
## #`0.35`
i.e. 0.35x
#3
## #`3`
i.e. 3x
{{after You can also set the column width with a number after `#`}}
Whole numbers and decimals with a dot or comma both work.
{{end}}

---
/
#
## fixed width
A column can also have a fixed width in `px`, `em`, `rem` or `%`, e.g. `#120px`. The other columns in the row share the remaining space.
---
#120px
## 120px
`120px` fixed
#500px
## 500px
`500px` fixed
#200px
## 200px
`200px` fixed
{{after `120px` fixed}}
#
## rest
computed width
{{end}}
---
#100px
## 100px
`100px` fixed
#10em
## 10em
`10em` fixed
#10rem
## 10rem
`10rem` fixed
#10%
## 10%
`10%` fixed
#
## rest
computed width

{{scene cards.md}}
{{part cards}}
#
##. 🧱 Cards and headings
## Card
Every `##` starts a new card with a frame; everything up to the next `##` or `#` belongs to it.
{{part subheadings}}
### Subheading
`###` structures the content inside a card.
#### small caption
`####` is a muted caption,
##### even smaller
###### and the smallest
{{part cards-column}}
#
## Second column
Another `#` = another column next to it.
/
## Space above a card
A `/` line between cards or columns adds a blank line, `//` two.
##
Card without a heading: a bare `##` is enough.
{{part plain-card}}
{{after Every `##`}}
`##.` instead of `##` is a card without a frame, e.g. a column heading (at the top).
{{wait 1.5}}
{{part fill}}
{{swap ## Second column "## Stretched card {.fill}"}}
{{after Another `#` = another column next to it.}}
`{.fill}` after the heading stretches the card to the height of the tallest column.
{{part foldable}}
{{end}}
##+ Foldable card
`##+` instead of `##`: clicking the heading folds the card, `##-` starts folded. The browser remembers it.
{{fold 1}}
{{wait 1}}
{{fold 1}}

{{scene lists.md}}
{{part bullets}}
#
##. `📋 Lists`
---
#
##
A bullet is `-`, nesting = 2 extra spaces (tab).
- bullet
- another
  - nested
    - and even deeper
{{part numbered}}
#
##
Numbered list: `1.`, nesting is again 2 spaces.
1. first
2. second
   1. nested
3. third
{{wait 1.5}}
{{swap 1. first "5. you can start at five"}}
{{after Numbered list}}
A list can start at any number, the rest are counted on.
{{part definitions}}
{{end}}
#
##
A term and below it `: explanation`.

TTL
: lifetime of a DNS record

MX
: mail server of a domain

{{scene tasks.md}}
{{part tasks}}
#
##. `✅ Tasks`
---
#
##
`- [ ]` is a task, `- [x]` a done task.
- [ ] check backups
- [ ] update the router
  - [ ] download firmware
- [x] order toner
#
##
Click the box and the task is ticked right in the file. The **+ new task** field adds another one.
{{tick 1}}
{{tick 3}}
{{add 1 check the UPS}}
{{part due-dates}}
#
##
Due date at the end of a task: a date `@2026-12-01`, or in how many days `@+3`, `@-1` (yesterday), even with a time `@+0 14:00`.
- [ ] meeting @+0 14:00
- [ ] renew certificate @+2
- [ ] return book to the library @-3
- [ ] renew domain @+40
- [x] file tax return @-10
##
Overdue in red, within 3 days in orange, done in grey.
{{wait 1}}
{{tick 7}}

{{scene table.md}}
#
##. `📊 Table`
##
Cells are separated by `|`, below the header goes a `|---|` row.
| service | port | status |
|---|---|---|
| web | 443 | ✓ |
| ssh | 22 | ✓ |
| backups | — | 3:00 |
{{wait 1.5}}
{{swap |---|---|---| "|:--|:-:|--:|"}}
{{after Cells are separated}}
A colon aligns the column: `:--` left, `:-:` center, `--:` right.
{{swap | backups "| backups | — | ~~3:00~~ **4:00** |"}}
{{end}}

**Bold** and ~~strikethrough~~ work in cells too.

{{scene code.md}}
{{part inline-code}}
#
## 💻 Inline code
one-line `code` 
highlighted `#!python print("hello")`
backtick inside: ``` `` a`b `` ```
{{part code-block}}
#
## 💻 Code block
```python
def greet(name):
-    return "Hello"
+    return f"Hello {name}!"  # with a name
print(greet("world"), 42)
```
{{end}}
with syntax highlighting by language
{{wait 2}}
{{swap ```python "```diff"}}
{{copy 1}}
{{wait 1.5}}
{{swap ```diff '```python hl_lines="3" linenums="1"'}}
{{after with syntax highlighting by language}}
`hl_lines="3"` highlights line 3, `linenums="1"` numbers the lines.

{{scene callouts.md}}
{{part quotes}}
#
##. `💬 Quotes and callouts`
##
> A plain quote starts with `>`.
>> `>>` is a nested quote.

{{part callouts}}
##
> [!tip] Tip
> A callout is a quote with a type `[!…]` and a title.

> [!warning] Careful
> Types: `note` `tip` `info` `warning` `danger`.
{{wait 1}}
{{swap > [!tip] Tip "> [!danger] Danger"}}
{{end}}

{{part foldable-callouts}}
##
> [!info]- Folded callout
> `-` after the type folds it, a click opens it.

> [!tip]+ Unfolded callout
> `+` = open, but it can be folded.
> **Markdown**, `code` and [links](/markdown) work inside.
{{open 1}}
{{wait 1}}
{{part callout-types}}
#
##. `🎨 More options`
##
> [!note]
> Without a title, the type is used as the title.

> [!success] Without content, a callout is just a coloured line.

##
Names from Obsidian and GitHub work too, they take the colour of the base type:

> [!question] question = info

> [!bug] bug = danger

> [!example] example = note

{{part mkdocs}}
##
MkDocs syntax works as well:
!!! warning "Admonition"
    content indented by 4 spaces

??? note "Folded block"
    `???+` opens it right away.

{{open 3}}
{{wait 1}}

{{scene note.md}}
{{part note}}
#
##. `📝 Note`
##
Between `{{note}}` and `{{/note}}` there is a field you type into right on the page.
{{note}}
shopping: milk, bread
{{/note}}

##
It saves itself into the md file. Markdown is not rendered in it, it is plain text.
{{note 1 call the plumber}}
{{note 1 **this stays with asterisks**}}

{{part editable-card}}
#
##. `✎ Editable card`
##* This week
**Mon** tennis
**Wed** choir

##
`##*` instead of `##` adds ✎ to the card. You edit it right on the page, without the editor, and only this card is saved.
{{edit 1 **Fri** cinema}}
{{edit 1 **Sun** trip\n**Mon** back to work}}

{{scene images.md}}
#
![Valley by day](/media/foto-den.svg)
---
#
##. `🖼️ Images`
##
A card with only an image (at the top) is a banner without a frame.
##
An image alone in a paragraph stretches to the card width:
![Grass blade over the valley](/media/foto-detail.svg "title in quotes, shown on mouse hover")
##
Icon in text ![](/media/ikona.svg){width=20} is shrunk with `{width=20}`.
Works in a list too:
- ![](/media/ikona.svg){width=18} Ben Nevis
- ![](/media/ikona.svg){width=18} Dolomites
#
##. `🧩 More options`
##
Image as a link: `[![](…) text](URL)`
[![](/media/ikona.svg){width=20} mountain map](https://www.openstreetmap.org)
##
Icons in a table:
| | trip | km |
|:-:|:--|--:|
| ![](/media/ikona.svg){width=18} | Ben Nevis | 12 |
| ![](/media/ikona.svg){width=18} | Lake District | 25 |
##
Width in percent and centered:

![Grass blade over the valley](/media/foto-detail.svg){width=55%}
{: .center }
##
Save your own images to `content/media/` (`svg png jpg webp gif avif`) and insert them with `![description](/media/file.svg)`. The description in `[…]` is read by screen readers.
{{wait 1.5}}
{{swap ![Valley by day] "![Valley at night](/media/foto-noc.svg)"}}
{{wait 1}}
{{swap Icon in text "Icon in text ![](/media/ikona.svg){width=32} is enlarged with `{width=32}`."}}

{{scene live-widgets.md}}
{{part status}}
#
##. `🟢 Live widgets`
---
# 
## Service status
`{.check}` after a link: 🟢 running, 🟠 responds with an error, 🔴 down.
- [Web](https://example.com){.check}
- [API](https://example.com){.check .warn}
- [Backup](https://example.com){.check .down}
{{part server}}
## Server
`{{sys}}`: the server's CPU, memory and disk.
{{sys cpu mem disk}}
{{part rss}}
#
## RSS
`{{rss URL 3}}`: the latest 3 articles from a feed.
{{rss https://news.ycombinator.com/rss 3}}
{{part history}}
## Changes
`{{history 3}}`: the latest file edits, a click shows the diff.
{{history 3}}
{{part countdown}}
## Countdown
`{{countdown 2026-12-24}}` anywhere in text, or in how many days: holiday {{countdown +12}}.
After the date it counts back, `days` shows just the number: h6082 has been running {{countdown 2026-11-12 days}}.
{{wait 3}}

{{scene appearance.md}}
{{part alignment}}
#
##. `🎯 Text appearance`
---
#
## ↔️ Alignment
Signpost
{: .center }

signature on the right
{: .right .muted }

A `{: … }` line right below a paragraph adds classes to it.
#
## 🔠 Size
small `.small`
{: .small }

normal text

bigger `.big`
{: .big }

huge `.huge`
{: .huge }
{{wait 1}}
{{swap {: .center } "{: .center .huge }"}}
{{swap {: .right .muted } "{: .muted }"}}
{{part attributes}}
{{end}}
---
#
## 🎨 Colours
Custom paragraph colour via `style`:
{: style="color:#00bfa5" }

Just part of the text: **orange**{: style="color:#ff9100" } and normal again.
#
## 🏷️ Attributes
### Subheading on the right {: .right }
Link in a new window: [map](https://www.openstreetmap.org){target=_blank}

Anchor `{#contact}` after a heading: a link `[…](#contact)` jumps to it.
{{part html}}
---
#
## 🧩 HTML in text
x<sup>2</sup> · H<sub>2</sub>O · <u>underline</u> · <small>small text</small>

<details><summary>HTML details</summary>hidden content</details>
#
## 💅 Custom CSS
<span style="background:#a882ff33;border-radius:6px;padding:1px 8px">label</span> <span style="background:#ff910033;border-radius:6px;padding:1px 8px">⚠ careful</span>

<span style="font-size:1.6em;letter-spacing:.2em">BIG</span>

<div style="border:1px dashed #00bfa5;border-radius:10px;padding:6px 10px" markdown="1">
A frame from `<div>`, with **markdown** inside thanks to `markdown="1"`.
</div>
{{open 1}}
{{part devices}}
---
#
## 🖥️ Computer only {.desktop}
A card with `{.desktop}` after the heading is only visible on a larger screen.
## 📱 Phone only {.mobile}
This card only shows on a phone.
#
## 📏 Breakpoint
Below a paragraph, `{: .mobile }` or `{: .desktop }` applies only to it. The breakpoint is 640 px.

{{scene text.md}}
{{part lines}}
#
##. `📝 Text and lines`
---
#
## Lines
First line
second line (just press Enter)
/
after a `/` line 
///
you can use more slashes in a row for a bigger gap, here `///`

A new paragraph after a blank line.
{{part hidden-notes}}
## Hidden notes
A text line starting with `//` is not shown:
{{paste}}
// call Peter about the keys
{{/paste}}
{{part escaping}}
## Escaping
\*asterisks\*, \# hash, \[brackets\], \`backtick\`
A backslash turns off formatting for a character.
{{part footnotes}}
#
## Notes and abbreviations
A claim with a footnote[^1] and the abbreviation HTML.
`[^1]` links to the note at the bottom, `*[HTML]: …` explains the abbreviation on mouse hover.
{{paste}}
*[HTML]: HyperText Markup Language
[^1]: Footnote text.
{{/paste}}
{{part divider}}
## Divider
Above the line.

---

Below the line: `---` with a blank line above it.
{{/livedemo}}
