# Start

![h6082](/media/demo-hero.cs.svg)

**Dobrý den 👋** Tohle je ukázková záložka. Všechno tady je obyčejný markdown v souboru `content/pages/demo.cs.md` (anglická verze je `demo.md`), klidně ho přepiš nebo smaž.

## ☀️ Dnes
- [x] ranní káva
- [ ] projít notifikace a PR
- [ ] 30 minut čtení
    - [ ] článek z RSS vedle
- [ ] zálohovat fotky

## 📝 Poznámka
{{note}}
Sem se dá psát přímo na stránce.
Pole roste dolů a ukládá se samo do md souboru.
{{/note}}

## ⌨️ Zkratky prohlížeče
- ++ctrl+l++ adresní řádek
- ++ctrl+shift+t++ obnovit zavřený tab
- ++ctrl+shift+v++ vložit bez formátu
- ++ctrl+f5++ obnovit bez cache

# Svět

## 🌐 Stav služeb
- [GitHub](https://github.com){.check} · kód, issues, pull requesty
- [Codeberg](https://codeberg.org){.check} · open-source hosting gitu
- [Wikipedie](https://www.wikipedia.org){.check} · encyklopedie
- [OpenStreetMap](https://www.openstreetmap.org){.check} · otevřené mapy
- [Mozilla](https://www.mozilla.org){.check} · Firefox a MDN
- [Cloudflare](https://www.cloudflare.com){.check} · CDN a DNS 1.1.1.1

<small>Tečka se obnovuje každou minutu, najetím myší uvidíš kód a odezvu.</small>

## 📰 Ars Technica
{{rss https://feeds.arstechnica.com/arstechnica/index 5}}

## 🖍️ xkcd
{{rss https://xkcd.com/atom.xml 3}}

# Tvorba

## 🛠️ Vývoj
### Dokumentace
- [MDN](https://developer.mozilla.org) · HTML, CSS, JavaScript
- [Python](https://docs.python.org/3/) · standardní knihovna
- [Rust](https://doc.rust-lang.org/book/) · The Book
### Nástroje
- [regex101](https://regex101.com) · ladění regulárních výrazů
- [explainshell](https://explainshell.com) · co dělá shellový příkaz
- [crontab.guru](https://crontab.guru) · srozumitelný cron
- [Can I use](https://caniuse.com) · podpora webových funkcí

## 🎨 Design a inspirace
- [Coolors](https://coolors.co) · generátor palet
- [Google Fonts](https://fonts.google.com) · písma zdarma
- [Unsplash](https://unsplash.com) · fotky bez licenčních starostí

## 📦 Snippet
```bash
# rychlý webserver z aktuální složky
python3 -m http.server 8000
# co zabírá nejvíc místa
du -sh * | sort -h | tail
```

## 📊 Projekt
| úkol | stav |
|---|:-:|
| návrh | ✓ |
| prototyp | ✓ |
| testy | ⏳ |
| vydání | — |

# Přehled

## 🖥️ Server
{{sys cpu mem load temp disk uptime demo}}

<small>**Demo režim**: vymyšlené hodnoty. Pro skutečné nastav v configu `[system] enabled = true` a z bloku odeber `demo`.</small>

## 🕓 Poslední změny
{{history 5 demo}}

<small>**Demo režim**: vymyšlené změny. Pro skutečné odeber z bloku `demo`.</small>

## 💡 Jak na to
> [!tip] Upravit záložku
> Na stránce **h6082** vpravo nahoře klikni na `demo.cs.md`. Otevře se editor s živým náhledem.

> [!info] Vlastní obrázky
> Ulož je do `content/media/` a vlož přes `![popis](/media/soubor.png)`.

??? note "Co všechno tu je?"
    Obrázek, úkoly a poznámka upravitelné na stránce, stav webů, RSS, stav serveru, historie změn, tabulka, kód a callouty. Všechny prvky popisuje záložka **markdown** na stránce h6082.

## ✉️ Kontakt
Napiš na {{email demo example.com}}. Adresa je chráněná před roboty.
