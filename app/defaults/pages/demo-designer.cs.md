// Demo: Klára, grafická designérka a fotografka na volné noze. Vizuální identity a produktové
// fotky pro malé firmy. Klienti i čísla jsou smyšlené.

#__ O nástěnce
## 🎨 Demo usecase: grafická designérka na volné noze
![studio Klára: identita, fotografie, tisk](/media/demo-design.cs.svg)

**Klára** navrhuje vizuální identity pro malé podniky a fotí jejich produkty. Pracuje sama, má čtyři rozjeté zakázky a nechce kvůli každé otevírat jinou aplikaci. Nástěnka je její **studio na jedné stránce**:

- **ráno** zkontroluje *Rozpracováno* a posune stav zakázek přes ✎. Tabulka je v souboru jako `##*`, takže nemusí do editoru.
- **na callu s klientem** sdílí obrazovku s briefem, moodboardem a paletou, všechno je pohromadě
- **při sazbě** zkopíruje HEX kódy a CSS proměnné značky jedním klikem, CMYK hodnoty pro tiskárnu má hned vedle
- **na konci měsíce** si v *Fakturách* odškrtne, co přišlo, a vidí, co je po splatnosti
- **pro radost** projde inspiraci z designových magazínů v RSS

#+ Zakázky
## `Zakázky`

##* 📋 Rozpracováno
| klient | zakázka | termín | stav |
|:--|:--|:--|:--|
| Pražírna Zrno | vizuální identita, etiketa 250 g / 1 kg | 28. 11. | ==návrhy== |
| Bistro Vltavská | fotky menu a interiéru pro web | 5. 12. | focení |
| Jóga Letná | sjednocení Instagramu, šablony | 15. 12. | brief |
| Spolek Karlín | výroční zpráva, tisk A4 | 20. 1. | čeká na texty |

## ☕ Pražírna Zrno: identita
**Brief:** malá pražírna výběrové kávy z menších farem. Má působit *poctivě a teple, ne snobsky*. Cílová skupina 25–45 let, prodej v kavárnách a e-shopu.
Kontakt: Jan Beneš {{email jan zrno.example}}

### Moodboard
![vzor zrn](/media/demo-design-beans.svg){width=132} ![návrh obalu](/media/demo-design-bag.svg){width=132} ![paleta](/media/demo-design-palette.svg){width=132} ![písmo](/media/demo-design-type.svg){width=132}

### Paleta
| | barva | HEX | CMYK<sup>*</sup> | použití |
|:-:|:--|:--|:--|:--|
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#2b1d16;vertical-align:-3px;border:1px solid #8885"></span> | espresso | `#2b1d16` | 0 · 33 · 49 · 83 | logo, text |
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#e9d8b9;vertical-align:-3px;border:1px solid #8885"></span> | crema | `#e9d8b9` | 0 · 7 · 21 · 9 | podklady |
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#c8553d;vertical-align:-3px;border:1px solid #8885"></span> | terakota | `#c8553d` | 0 · 58 · 70 · 22 | akcent, ceny |
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#6b7d4f;vertical-align:-3px;border:1px solid #8885"></span> | oliva | `#6b7d4f` | 14 · 0 · 37 · 51 | origin, štítky |
| <span style="display:inline-block;width:1.1em;height:1.1em;border-radius:3px;background:#f6f1e7;vertical-align:-3px;border:1px solid #8885"></span> | papír | `#f6f1e7` | 0 · 2 · 6 · 4 | pozadí webu |

<small>* orientační převod, finální hodnoty podle nátisku v tiskárně</small>

```css
:root {
  --zrno-espresso: #2b1d16;
  --zrno-crema:    #e9d8b9;
  --zrno-terakota: #c8553d;
  --zrno-oliva:    #6b7d4f;
  --zrno-papir:    #f6f1e7;
}
```

### Typografie
- [Fraunces](https://fonts.google.com/specimen/Fraunces) · nadpisy, variabilní, OFL
- [Inter](https://rsms.me/inter/) · texty, ceník, etiketa

Claim na etiketu:
**Káva z farem, které známe jménem.**{: style="font-family:Georgia,serif;font-size:1.25em;color:#c8553d" }

### Úkoly
- [x] rešerše konkurence, 12 pražíren
- [ ] tři směry loga (wordmark, symbol zrna, monogram)
- [ ] etiketa 250 g, 1 kg + varianty origin
- [ ] šablony pro Instagram (post 4:5, story)
- [ ] prezentace návrhů **28. 11.**

### Zpětná vazba od klienta
{{note}}
- směr B (zrno v kruhu) nejvíc, ale bez gradientu
- terakotu víc do hněda, ať to není „pizzerie“
- origin na etiketě větší, je to hlavní prodejní argument
{{/note}}

*[OFL]: SIL Open Font License, písmo zdarma i pro komerční použití
*[CMYK]: tiskové barvy: azurová, purpurová, žlutá, černá

# Studio
## `Studio`

## 🧰 Nástroje
- [Figma](https://www.figma.com) · návrhy, prezentace klientům
- [Adobe Creative Cloud](https://creativecloud.adobe.com) · Illustrator, InDesign
- [Lightroom](https://lightroom.adobe.com) · fotky produktů
- [Coolors](https://coolors.co) · ladění palet
- [WebAIM Contrast](https://webaim.org/resources/contrastchecker/) · kontrast textu [?](Pro běžný text aspoň 4,5 : 1, pro velké nadpisy 3 : 1, požadavek WCAG AA)
- [Squoosh](https://squoosh.app) · komprese obrázků pro web

## ⌨️ Figma
| zkratka | akce |
|:--|:--|
| ++shift+a++ | auto layout |
| ++ctrl+alt+k++ | vytvořit komponentu |
| ++ctrl+alt+g++ | zabalit výběr do framu |
| ++ctrl+d++ | duplikovat |
| ++shift+h++ / ++shift+v++ | převrátit vodorovně / svisle |

## 🖨️ Podklady
| výstup | barvy | rozlišení | formát |
|:--|:--|:--|:--|
| tisk | CMYK, FOGRA39 | 300 dpi, spadávka 3 mm | PDF/X-4 |
| web | sRGB | 2× pro retina | WebP, SVG |
| Instagram | sRGB | 1080 × 1350 (4:5) | JPG |

> [!warning]- Černá v tisku
> Text vždy jen 100 % K, jinak se při soutisku rozmaže. Velké černé plochy jako bohatá černá C60 M40 Y40 K100.

##* 🧾 Faktury
| číslo | klient | částka | splatnost | stav |
|:--|:--|--:|:--|:-:|
| 2026-041 | Bistro Vltavská | 18 500 Kč | 20. 11. | ⏳ |
| 2026-040 | Spolek Karlín, záloha | 12 000 Kč | 6. 11. | ✓ |
| 2026-039 | Jóga Letná | 6 800 Kč | ~~1. 11.~~ | ⚠️ upomínka |

- [Fakturoid](https://www.fakturoid.cz) · vystavování faktur
- [Moje daně](https://www.mojedane.cz) · paušální daň [?](V paušálním režimu jedna měsíční platba za daň, zdravotní a sociální pojištění, splatná do 20. dne v měsíci)

*[OFL]: SIL Open Font License, písmo zdarma i pro komerční použití
*[CMYK]: tiskové barvy: azurová, purpurová, žlutá, černá
*[FOGRA39]: standard pro ofsetový tisk na natíraný papír
*[WCAG]: Web Content Accessibility Guidelines

# Inspirace
## `Inspirace`

## 🔗 Zdroje
- [Fonts In Use](https://fontsinuse.com) · písma v reálných projektech
- [Are.na](https://www.are.na) · sbírky referencí
- [Behance](https://www.behance.net) · portfolia
- [Unsplash](https://unsplash.com) · fotky pro koncepty

## 📰 Creative Boom
{{rss https://www.creativeboom.com/feed/ 3}}

## 📰 Smashing Magazine
{{rss https://www.smashingmagazine.com/feed/ 3}}

## 📰 Abduzeedo
{{rss https://abduzeedo.com/rss.xml 3}}
