// Demo: Klára, freelance graphic designer and photographer. Visual identities and product
// photos for small businesses. Clients and numbers are made up.

#__ About this board
## 🎨 Demo use case: a freelance graphic designer
![studio Klára: identity, photography, print](/media/demo-design.svg)

**Klára** designs visual identities for small businesses and photographs their products. She works alone, has four jobs in progress and doesn't want to open a different app for each one. The board is her **studio on a single page**:

- **in the morning** she checks *In progress* and moves the jobs along with ✎. The table is a `##*` block in the file, so she doesn't need the editor.
- **on a call with a client** she shares her screen with the brief, moodboard and palette, everything is in one place
- **while typesetting** she copies the brand's HEX codes and CSS variables with one click, and the CMYK values for the printer are right next to them
- **at the end of the month** she ticks off in *Invoices* what has been paid and sees what is overdue
- **for fun** she browses inspiration from design magazines in RSS

#+ Jobs
## `Jobs`

##* 📋 In progress
| client | job | deadline | status |
|:--|:--|:--|:--|
| Pražírna Zrno | visual identity, label 250 g / 1 kg | 28 Nov | ==concepts== |
| Bistro Vltavská | menu and interior photos for the website | 5 Dec | shooting |
| Jóga Letná | unified Instagram, templates | 15 Dec | brief |
| Spolek Karlín | annual report, A4 print | 20 Jan | waiting for texts |

## ☕ Pražírna Zrno: identity
**Brief:** a small roastery of speciality coffee from smaller farms. It should feel *honest and warm, not snobbish*. Target group aged 25–45, sold in cafés and an online shop.
Contact: Jan Beneš {{email jan zrno.example}}

### Moodboard
![bean pattern](/media/demo-design-beans.svg){width=132} ![packaging concept](/media/demo-design-bag.svg){width=132} ![palette](/media/demo-design-palette.svg){width=132} ![typeface](/media/demo-design-type.svg){width=132}

### Palette
| | colour | HEX | CMYK<sup>*</sup> | use |
|:-:|:--|:--|:--|:--|
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#2b1d16;vertical-align:-3px;border:1px solid #8885"></span> | espresso | `#2b1d16` | 0 · 33 · 49 · 83 | logo, text |
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#e9d8b9;vertical-align:-3px;border:1px solid #8885"></span> | crema | `#e9d8b9` | 0 · 7 · 21 · 9 | backgrounds |
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#c8553d;vertical-align:-3px;border:1px solid #8885"></span> | terracotta | `#c8553d` | 0 · 58 · 70 · 22 | accent, prices |
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#6b7d4f;vertical-align:-3px;border:1px solid #8885"></span> | olive | `#6b7d4f` | 14 · 0 · 37 · 51 | origin, labels |
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#f6f1e7;vertical-align:-3px;border:1px solid #8885"></span> | paper | `#f6f1e7` | 0 · 2 · 6 · 4 | website background |

<small>* approximate conversion, final values according to the printer's proof</small>

```css
:root {
  --zrno-espresso: #2b1d16;
  --zrno-crema:    #e9d8b9;
  --zrno-terakota: #c8553d;
  --zrno-oliva:    #6b7d4f;
  --zrno-papir:    #f6f1e7;
}
```

### Typography
- [Fraunces](https://fonts.google.com/specimen/Fraunces) · headings, variable, OFL
- [Inter](https://rsms.me/inter/) · body text, price list, label

Tagline for the label:
**Coffee from farms we know by name.**{: style="font-family:Georgia,serif;font-size:1.25em;color:#c8553d" }

### Tasks
- [x] competitor research, 12 roasteries
- [ ] three logo directions (wordmark, bean symbol, monogram)
- [ ] label 250 g, 1 kg + origin variants
- [ ] Instagram templates (post 4:5, story)
- [ ] concept presentation **28 Nov**

### Client feedback
{{note}}
- direction B (bean in a circle) the most, but without the gradient
- push the terracotta more towards brown, so it doesn't look like a "pizzeria"
- origin bigger on the label, it is the main selling point
{{/note}}

*[OFL]: SIL Open Font License, a free typeface even for commercial use
*[CMYK]: print colours: cyan, magenta, yellow, black

# Studio
## `Studio`

## 🧰 Tools
- [Figma](https://www.figma.com) · designs, client presentations
- [Adobe Creative Cloud](https://creativecloud.adobe.com) · Illustrator, InDesign
- [Lightroom](https://lightroom.adobe.com) · product photos
- [Coolors](https://coolors.co) · tuning palettes
- [WebAIM Contrast](https://webaim.org/resources/contrastchecker/) · text contrast [?](At least 4.5 : 1 for normal text, 3 : 1 for large headings, a WCAG AA requirement)
- [Squoosh](https://squoosh.app) · image compression for the web

## ⌨️ Figma
| shortcut | action |
|:--|:--|
| ++shift+a++ | auto layout |
| ++ctrl+alt+k++ | create component |
| ++ctrl+alt+g++ | wrap selection in a frame |
| ++ctrl+d++ | duplicate |
| ++shift+h++ / ++shift+v++ | flip horizontally / vertically |

## 🖨️ Print-ready files
| output | colours | resolution | format |
|:--|:--|:--|:--|
| print | CMYK, FOGRA39 | 300 dpi, 3 mm bleed | PDF/X-4 |
| web | sRGB | 2× for retina | WebP, SVG |
| Instagram | sRGB | 1080 × 1350 (4:5) | JPG |

> [!warning]- Black in print
> Text always only 100 % K, otherwise it blurs when the plates are registered. Large black areas as rich black C60 M40 Y40 K100.

##* 🧾 Invoices
| number | client | amount | due | status |
|:--|:--|--:|:--|:-:|
| 2026-041 | Bistro Vltavská | 18 500 Kč | 20 Nov | ⏳ |
| 2026-040 | Spolek Karlín, deposit | 12 000 Kč | 6 Nov | ✓ |
| 2026-039 | Jóga Letná | 6 800 Kč | ~~1 Nov~~ | ⚠️ reminder |

- [Fakturoid](https://www.fakturoid.cz) · issuing invoices
- [Moje daně](https://www.mojedane.cz) (Czech tax portal) · flat-rate tax [?](In the flat-rate regime, one monthly payment covers income tax, health and social insurance, due by the 20th of the month)

*[OFL]: SIL Open Font License, a free typeface even for commercial use
*[CMYK]: print colours: cyan, magenta, yellow, black
*[FOGRA39]: standard for offset printing on coated paper
*[WCAG]: Web Content Accessibility Guidelines

# Inspiration
## `Inspiration`

## 🔗 Sources
- [Fonts In Use](https://fontsinuse.com) · typefaces in real projects
- [Are.na](https://www.are.na) · reference collections
- [Behance](https://www.behance.net) · portfolios
- [Unsplash](https://unsplash.com) · photos for concepts

## 📰 Creative Boom
{{rss https://www.creativeboom.com/feed/ 3}}

## 📰 Smashing Magazine
{{rss https://www.smashingmagazine.com/feed/ 3}}

## 📰 Abduzeedo
{{rss https://abduzeedo.com/rss.xml 3}}
