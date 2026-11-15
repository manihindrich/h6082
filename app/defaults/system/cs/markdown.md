#
##.
{{examples}}

---
#
##. `Struktura`

---
#
## Záložky
Každý soubor `content/pages/*.md` je jedna záložka v horní liště.

Název záložky je jméno souboru bez `.md`. Překlad je soubor `jmeno.cs.md` nebo `jmeno.en.md` a zobrazí se podle zvoleného jazyka.

- uživatelské záložky jsou vlevo, pořadí určuje `[tabs] order`
- skryté (`[tabs] hidden`) jsou dostupné přes `/<jméno>`
- první uživatelská záložka je na `/`
- nový soubor vytvoříš na stránce [nastavení](/settings)
- odkaz na jinou záložku je obyčejný odkaz na `/<jméno>`:

```md
[dokumentace](/documentation)
```

## Sloupce
Řádek `#` začne nový sloupec, `---` nový řádek sloupců. Takhle je poskládaná i celá tahle stránka.
{{example sloupce.md}}
| zápis | výsledek |
|---|---|
| `#` | sloupec |
| `#+` | sloupec 1,5× širší |
| `#++` | sloupec 1,75× širší |
| `#-` | úzký sloupec, poloviční šířka |
| `#--` | velmi úzký sloupec, čtvrtinová šířka |
| `#1.2` · `#0,8` | vlastní poměr šířky (desetinná tečka i čárka) |
| `#120px` · `#12em` · `#30%` | pevná šířka, ostatní sloupce řádku si rozdělí zbytek; procenta počítají i s mezerami, takže `#25%` `#25%` `#50%` přesně vyplní řádek |
| `---` | nový řádek sloupců (řádek těsně před `#`); samotný `#` v řádku je pás přes celou šířku |
| ` ##. nadpis ` | nadpis sloupce bez rámečku, viz Karta bez rámečku |

- text za `#` je jen pro orientaci v souboru, na stránce se nezobrazí
- šířky jsou poměrové: čísla v řádku určují poměr, `#++` vedle `#-` je 3,5× širší; úzké sloupce se hodí na rychlé odkazy nebo stav služeb
- sloupec potřebuje aspoň svoje číslo × `[layout] column_min_width`; co se nevejde, zalomí se na další řádek a roztáhne se
- mezi řádky `---` je stejná mezera jako mezi sloupci (`[layout] row_gap`); řádek `/` mezi `---` a `#` přidá další
- `---`, za kterým nenásleduje `#`, zůstane vodorovnou čarou v kartě
- počet sloupců: šířka okna, nebo `[layout] columns_fixed`
- `#` uvnitř bloku kódu se ignoruje

```md
# Dev
## Repos
…
#+ Široký sloupec
## Servery
…
#- Úzký sloupec
## Rychlé odkazy
…
---
# Pás přes celou šířku
## Novinky
…
```

## Skryté poznámky
Řádek začínající `//` se na stránce nevykreslí.
{{example skryte}}
Hodí se na připomínky v souboru. Uvnitř bloku kódu a uprostřed řádku `//` platí jako obyčejný text.

```md
// poznámka jen pro mě
```

#
## Karty
`## Titulek` vytvoří orámovanou kartu, jako je každý rámeček na této stránce.
{{example karty.md}}
Všechno až do dalšího `##` nebo `#` patří do karty.
Obsah před prvním `##` ve sloupci tvoří kartu bez titulku, stejně jako samotné `##` bez textu.
`## Titulek {.fill}` roztáhne kartu do výšky nejvyššího sloupce v řádku, takže sousední karty končí na stejné úrovni (karta Autor na stránce [nastavení](/settings)).

```md
## Repos
- [GitHub](https://github.com)
```

## Karta bez rámečku
`##.` místo `##` vykreslí kartu bez rámečku a pozadí, třeba žluté nadpisy řádků na této stránce.
{{example bez-ramecku}}
Hodí se k pojmenování sloupce, ale může mít i obsah, třeba text přímo na stránce. Samotné `##.` bez textu = obsah bez rámečku i nadpisu.
`kód` v jakémkoli nadpisu nemá vlastní rámeček, zůstane jen jeho barva.

```md
# Struktura
##. `Struktura`

## Záložky
…
```

## Upravitelné karty
`##*` místo `##` označí kartu, která jde upravit přímo na stránce, bez otevírání editoru.
{{example upravitelna-karta}}
Hodí se na průběžné drobnosti: seznamy, tabulky, krátké texty.

- po najetí myší je vpravo nahoře ✎, klik otevře markdown karty na místě
- ++ctrl+enter++ uloží, ++esc++ zruší; funguje chytré psaní i zkratky z editoru
- uloží se jen tato karta, zbytek souboru zůstane beze změny
- když se karta mezitím změní jinde, uložení se odmítne a nic se nepřepíše
- titulek a nové karty se mění v editoru; platí jen pro tvoje záložky a s heslem editoru

```md
##* Nákupní seznam
- mléko
- chleba
```

#
##+ Sbalitelné karty
Klik na nadpis kartu sbalí a příště zůstane sbalená. Zkus to na téhle kartě.
{{example sbalitelne}}
`##-` místo `##` je karta sbalená od začátku, `##+` rozbalená, ale jde sbalit. Klik na nadpis (nebo ++enter++ na něm) ji přepne. Prohlížeč si stav pamatuje pro každou stránku a kartu, do souboru se nic nezapisuje. Jde kombinovat s `{.fill}` nebo `{.mobile}`.

```md
##- Archiv
- staré odkazy

##+ Tento týden
- …
```

## Podnadpisy
`###` člení obsah uvnitř karty.
{{example podnadpisy}}
Nadpis i obsah pod ním jsou lehce odsazené (`[layout] h3_indent`, `content_indent`).

```md
### Jazyky
- [Rust](https://doc.rust-lang.org/std/)
```

## Menší nadpisy
`####` až `######` jsou malé tlumené nadpisy na drobné popisky.
{{example podnadpisy}}
Jsou bez odsazení. Vzhled: `[style.h4]` až `[style.h6]`.

```md
#### popisek 4. úrovně
##### popisek 5. úrovně
```

## Řádky a odstavce
Každý řádek v souboru je řádek na stránce, prázdný řádek začne odstavec.
{{example radky}}
- ++enter++ = nový řádek, prázdný řádek = nový odstavec s mezerou
- řádek jen s `/` vloží prázdný řádek, `//` dva, `///` tři…
- `/` mimo kartu (hned pod `#`, nebo nad `##`) udělá mezeru mezi kartami, mezi `---` a `#` mezeru mezi řádky sloupců
- klasické markdown chování (řádky se slévají) vrátí `[markdown] line_breaks = false`

Před seznamem, tabulkou, citací, blokem kódu nebo nadpisem nemusí být prázdný řádek a za tabulkou taky ne, doplní se sám.

```md
První řádek
druhý řádek
/
po prázdném řádku

Nový odstavec.
```

---
#
//
##. `Text`

---
#
## Řez písma
Tučné písmo, kurzíva a přeškrtnutí.
{{example pismo}}
Fungují i varianty s podtržítkem: `__tučně__` a `_kurzíva_`.
V editoru: ++ctrl+b++, ++ctrl+i++, ++ctrl+shift+x++.

```md
**tučně** · *kurzíva* · ***obojí*** · ~~přeškrtnuto~~
```

## Zvýraznění
`==text==` podbarví úsek jako zvýrazňovač.
{{example pismo}}
Barva: `mark_bg` v motivu, vzhled: `[style.highlight]`. V editoru: ++ctrl+shift+h++.

```md
Text se ==zvýrazněným úsekem==.
```

## Inline kód
Text mezi backticky je kód přímo v řádku.
{{example inline-kod}}
`#!jazyk` na začátku zapne zvýraznění syntaxe.
Backtick uvnitř kódu: ``` `` a`b `` ```. V editoru: ++ctrl+e++.

```md
`docker ps`
`#!python print("hi")`
```

## Klávesy
`++ctrl+b++` nakreslí klávesovou zkratku.
{{example klavesy}}
Klávesy se spojují znakem `+`. Známé názvy (`ctrl`, `alt`, `shift`, `cmd`, `win`, `tab`, `esc`, `up`, `f1`–`f24`, `page-up`, …) se převedou na popisky.

```md
++ctrl+shift+t++ · ++f5++
```

## Nápověda
`[?](text)` je ikona s nápovědou, která se ukáže po najetí myší.
{{example klavesy}}
Na mobilu se ukáže po klepnutí. `\n` v textu zalomí řádek. Místo ⓘ může být libovolný znak (`[★](?…)`).
Vzhled: `[style.tip]`. `[?](https://…)` zůstane obyčejným odkazem.

```md
[?](text nápovědy)
[★](?text nápovědy)
```

#
## Zkratky
`*[TOML]: …` vysvětlí zkratku po najetí myší.
{{example pod-carou}}
Definice může být kdekoli ve sloupci a platí pro celý sloupec.

```md
Konfigurace v TOML.
*[TOML]: Tom's Obvious Minimal Language
```

## Závorky
Závorky jde v configu obarvit, třeba vedlejší poznámky (v závorce).

Každý typ (`round`, `square`, `curly`, `angle`) má vlastní sekci, např. `[style.bracket_round] color = "muted"`. Výchozí vzhled je beze změny.

```md
Text (v závorce) a [hranatá] i {složená}.
```

## Escapování
Zpětné lomítko před znakem vypne jeho formátování.
{{example escapovani}}
Hodí se, když chceš napsat `*`, `#`, `[` nebo backtick tak, jak jsou.

```md
\*hvězdičky\*  \# křížek  \[závorky\]
```

## Inline HTML
HTML v textu funguje: horní a dolní index, podtržení, vlastní styly.
{{example html}}
- `style="…"` na `<span>` nebo `<div>` = vlastní CSS (barva, pozadí, rámeček)
- markdown uvnitř HTML bloku se zpracuje, jen když má blok atribut `markdown="1"`
- `<details><summary>` je sbalitelný blok

```html
<small>malý</small> x<sup>2</sup> H<sub>2</sub>O <u>podtržení</u>
<span style="background:#a882ff33;border-radius:6px;padding:1px 8px">štítek</span>
```

## Ozubené kolečko
`{{gear}}` vloží do textu ikonu nastavení.
{{example klavesy}}
Je to stejné ozubené kolečko jako v liště, jen jako ikona (není to odkaz). Hodí se do návodů a uvítacích textů.

```md
pod {{gear}} vpravo nahoře
```

#
## Zarovnání a velikost
Řádek `{: … }` hned pod odstavcem ho zarovná nebo zvětší.
{{example zarovnani}}
| třída | výsledek |
|:--|:--|
| `.center` / `.right` | zarovnání na střed / doprava |
| `.big` / `.huge` | větší / velké písmo |
| `.small` | menší písmo |
| `.muted` | tlumená barva |

Třídy jdou kombinovat a fungují i u nadpisů a seznamů. U nadpisu může být `{: … }` na konci řádku i na řádku pod ním. Vlastní styl: `{: style="…" }`, viz Atributy.

```md
Rozcestník na střed
{: .center .big }

podpis vpravo
{: .right .muted }
```

## Jen telefon nebo počítač
`{.mobile}` a `{.desktop}` ukážou kartu nebo odstavec jen na telefonu, nebo jen na počítači.
{{example zarizeni}}
Hranice je 640 px, stejná jako skládání sloupců pod sebe. Za nadpisem `##` platí pro celou kartu, pod odstavcem jen pro něj.

```md
## Tip pro telefon {.mobile}
…

Odstavec jen pro počítač.
{: .desktop }
```

## Atributy
`{…}` za prvkem mu přidá barvu, třídu, kotvu nebo jiný atribut.
{{example atributy}}
Za prvek jde přidat `{#id}`, `{.třída}`, `{klíč=hodnota}` i `{: style="…" }`. U nadpisu jde atributy napsat na konec řádku i na samostatný řádek hned pod něj.

```md
Odstavec.
{: style="color:#00bfa5" }
**text**{: style="color:#ff9100" }
[mapy](https://mapy.cz){target=_blank}
```

## Poznámky pod čarou
`[^1]` v textu odkáže na poznámku, která se vypíše dole.
{{example pod-carou}}
Poznámky se zobrazí na konci poslední karty ve sloupci. Identifikátor může být i slovo (`[^zdroj]`).

```md
Tvrzení s poznámkou[^1].
[^1]: Text poznámky.
```

---
#
//
##. `Odkazy a obrázky`

---
#
## Odkazy
`[text](adresa)` je odkaz, volitelně s titulkem nebo s adresou bokem.
{{example odkazy}}
Externí odkazy se otevírají v nové záložce (`[page] links_new_tab`). V editoru: ++ctrl+k++, nebo vlož URL přes označený text.

```md
[text](https://example.com)
[text](https://example.com "tooltip")
[text](/documentation)
[text][ref]
[ref]: https://example.com
```

## Auto-odkazy
Holá adresa v textu je sama odkazem.
{{example odkazy}}
Zobrazí se bez `https://` a koncového lomítka. Odkaz na `http://` dostane varovnou značku, kromě adres v místní síti (`192.168.…`, `*.local`, `*.lan`, `localhost`).

```md
<https://example.com>
https://example.com/path
<user@example.com>
```

#
## Chráněný e-mail
`{{email jméno doména}}` ukáže e-mail, který roboti v souboru nenajdou.
{{example odkazy}}
Jméno a doména se píšou odděleně, takže v md ani v HTML není adresa se zavináčem. Čitelnou adresu a odkaz `mailto:` složí až JavaScript v prohlížeči. Funguje kdekoli v textu.

```md
{{email jmeno example.com}}
```

## Obrázky
`![popis](/media/soubor.svg)` vloží obrázek, banner nebo malou ikonu.
{{example obrazky.md}}
- vlastní obrázky ulož do `content/media/` a vlož přes `/media/<soubor>` (`svg png jpg webp gif avif ico`)
- obrázek sám v odstavci se roztáhne na šířku karty
- karta bez nadpisu, ve které je jen obrázek, se vykreslí bez rámečku jako banner (hlavička stránky nastavení)
- menší velikost nastavíš atributem `{width=…}`
- obrázky z webu (`https://…`) fungují taky, ale prohlížeč je stahuje z cizího serveru

Skript uvnitř SVG se nespustí ani při přímém otevření obrázku.

```md
![údolí](/media/foto-den.svg)
![ikona](/media/ikona.svg){width=20}
[![](/media/ikona.svg){width=14} text](https://…)
```

---
#
//
##. `Seznamy a úkoly`

---
#
## Odrážky
`-` na začátku řádku je položka seznamu.
{{example odrazky}}
Vnoření stačí odsadit o 2 mezery, v editoru ++tab++. Odrážky se kreslí jako `›` (`[style.list] marker`). Fungují i `*` a `+`.
V editoru: ++ctrl+shift+8++.

```md
- položka
  - vnořená
```

## Číslované seznamy
`1.` na začátku řádku je číslovaná položka.
{{example cislovane}}
++enter++ na konci položky přidá další číslo. Seznam může začít libovolným číslem. V editoru: ++ctrl+shift+7++.

```md
1. první
2. druhý
   1. vnořený
```

#
## Úkoly
`- [ ]` je úkol se zaškrtávacím políčkem, `- [x]` hotový úkol.
{{example ukoly}}
V tvých záložkách jdou úkoly upravovat přímo na stránce:
- klik na políčko úkol zaškrtne nebo odškrtne
- ✕ (po najetí myší) smaže úkol i s podúkoly
- pole **+ nový úkol** přidá úkol na konec seznamu

Změna se hned zapíše do md souboru. Tady v dokumentaci jsou úkoly jen pro čtení. V editoru: ++ctrl+shift+9++.

```md
- [x] hotovo
- [ ] rozpracováno
  - [ ] podúkol
```

## Definiční seznam
Pojem a pod ním `: vysvětlení`.
{{example definice}}
Pojem je na jednom řádku, vysvětlení na dalším za `: `. Vysvětlení může být víc.

```md
TTL
: doba platnosti DNS záznamu
```

#
## Termíny úkolů
`@datum` na konci úkolu ukáže štítek s termínem.
{{example terminy}}
| zápis | termín |
|:--|:--|
| `@2027-03-31` | pevné datum |
| `@2026-11-20 14:00` | datum a čas |
| `@+3` · `@-2` | za 3 dny · před 2 dny od dneška (šablony a ukázky, které nemají stárnout) |
| `@+0 14:00` | dnes ve 14:00 |

Do týdne je štítek relativní („za 2 dny“, „včera“), dál datum. Po termínu je červený, do 3 dnů oranžový, u hotového úkolu šedý. Počítá prohlížeč podle dnešního data; v souboru zůstává zápis, takže úkol jde dál odškrtnout i upravit.

```md
- [ ] podat daňové přiznání @2027-03-31
- [ ] porada @2026-11-20 14:00
- [ ] obnovit certifikát @+2
```

---
#
//
##. `Obsah karet`

---
#
## Tabulky
Buňky odděluje `|`, pod hlavičkou je řádek `|---|`.
{{example tabulka.md}}
Zarovnání určuje oddělovací řádek: `:--` vlevo, `--:` vpravo, `:-:` na střed. V buňkách funguje inline formátování.

```md
| služba | port | stav |
|:--|--:|:-:|
| home | 8088 | ✓ |
```

## Bloky kódu
Kód mezi ```` ``` ```` je samostatný blok, obarvený podle jazyka.
{{example blok-kodu}}
- najeď myší na blok: vpravo nahoře je tlačítko pro zkopírování
- jazyk: `bash`, `python`, `yaml`, `toml`, `json`, `rust`, `nix`, `diff`, …
- `hl_lines="2 4-6"` zvýrazní řádky, `linenums="1"` je očísluje
- barevné schéma a čísla řádků globálně: `[code]`

````md
```python hl_lines="2"
def hello(name):
    return f"ahoj {name}"
```
````

## Citace
`>` na začátku řádku je citace, `>>` vnořená.
{{example citace}}
++enter++ v editoru pokračuje v citaci, na prázdném řádku ji ukončí.

```md
> Krátká citace nebo poznámka.
>> vnořená citace
```

#
## Callouty
Citace s typem `[!tip]` je barevný rámeček s titulkem.
{{example callouty}}
Typy: `note` · `tip` · `info` · `warning` · `danger`. Fungují i aliasy z Obsidianu a GitHubu (`important`, `caution`, `question`, `bug`, `success`, …). Bez titulku se jako titulek použije typ, callout bez obsahu je jen barevný řádek.

```md
> [!tip] Titulek
> obsah
```

## Sbalitelné callouty
`-` nebo `+` za typem udělá z calloutu sbalitelný blok.
{{example sbalitelne-callouty}}
`-` = sbalený, `+` = rozbalený, ale sbalitelný.

```md
> [!info]- Sbalený
> obsah
```

## Admonition
`!!!` je callout v syntaxi z MkDocs.
{{example mkdocs}}
Obsah je odsazený 4 mezerami. Výsledek je stejný jako u calloutu.

```md
!!! warning "Titulek"
    obsah odsazený 4 mezerami
```

#
## Details
`???` je sbalitelný blok v syntaxi z MkDocs.
{{example mkdocs}}
`???` = sbalený, `???+` = rozbalený. Obsah je odsazený 4 mezerami.

```md
??? note "Sbalený"
    obsah
```

## Poznámka
`{{note}}` … `{{/note}}` je pole, do kterého se píše přímo na stránce.
{{example poznamka}}
- text mezi značkami je obyčejný text, markdown se v něm nevykresluje
- v tvých záložkách se ukládá sama ~0,8 s po poslední změně, pole roste podle délky textu
- když se poznámka mezitím změní jinde, uložení se odmítne a nic se nepřepíše
- zápis vyžaduje heslo editoru, tady v dokumentaci je jen pro čtení

````md
{{note}}
mléko, chleba
zavolat instalatérovi
{{/note}}
````

## Oddělovač
`---` mezi prázdnými řádky nakreslí vodorovnou čáru.
{{example oddelovac}}
Před `---` musí být prázdný řádek, jinak se z předchozího řádku stane nadpis.

```md
nad čarou

---

pod čarou
```

---
#
//
##. `Živé prvky`

---
#
## Stav služeb
`{.check}` za odkazem ukáže barevnou tečkou, jestli služba odpovídá.
{{example stav-sluzeb}}
| tečka | stav |
|:--|:--|
| 🟢 | v pořádku |
| 🟠 | 4xx: běží, ale chce přihlášení apod. |
| 🔴 | 5xx, timeout nebo nedostupné |

- `{.check}` kontroluje adresu odkazu přes HTTP(S)
- `{check="…"}` je vlastní cíl: `https://…` nebo `tcp://host:port`
- najetí myší ukáže kód, odezvu nebo chybu
- obnovuje se každých `[checks] interval_s`
- vymyšlený stav pro ukázky: [ukázková data](/documentation#ukazkova-data)

Kontroly běží ze serveru v kontejneru. Služby na hostiteli: `host.docker.internal:<port>`. Server kontroluje jen cíle napsané v md souborech.

```md
[GitHub](https://github.com){.check}
[NAS](http://nas.lan){check="tcp://192.168.1.50:22"}
```

#
## Server
`{{sys}}` ukáže vytížení procesoru, paměti a disků serveru.
{{example server}}
- části, bez parametrů se zobrazí všechny:

| část | ukáže |
|:--|:--|
| `cpu` | vytížení procesoru |
| `cpuinfo` | jádra × model procesoru |
| `mem` · `swap` | využití paměti a swapu |
| `load` | průměrná zátěž za 1 · 5 · 15 min, pruh = poslední minuta ÷ jádra |
| `procs` | procesy celkem a běžící |
| `io` | čtení ↓ a zápis ↑ disků za sekundu |
| `temp` | teploty (`[system] temps`) |
| `disk` | zaplnění disků (`[system] disks`) |
| `uptime` | doba od spuštění |

- swap a teploty se ukážou jen tam, kde je server má; síťový provoz chybí záměrně, kontejner vidí jen ten svůj
- hodnoty se obnovují každých `[system] interval_s` sekund
- pruh je oranžový od 70 %, červený od 90 %

> [!info] Zapnutí
> V `config.toml` nastav `[system] enabled = true`. Výchozí stav je vypnuto, protože `/api/sys` vidí každý, kdo vidí stránku. Vymyšlené hodnoty pro ukázky: [ukázková data](/documentation#ukazkova-data).

```md
{{sys}}
{{sys cpu mem disk}}
```

## RSS
`{{rss URL}}` vypíše poslední články z feedu.
{{example rss}}
- celý řádek = jeden feed, číslo = počet položek (výchozí `[rss] default_limit`)
- RSS 2.0, RSS 1.0 i Atom
- 💬 = odkaz na komentáře, pokud je feed má
- server drží feed v cache `[rss] refresh_min` minut a při výpadku zdroje ukáže poslední známý stav
- vymyšlené titulky pro ukázky: [ukázková data](/documentation#ukazkova-data)

```md
{{rss https://news.ycombinator.com/rss 5}}
```

#
## Historie změn
`{{history}}` vypíše poslední úpravy souborů.
{{example historie}}
- poslední změny: čas, soubor, přidané a odebrané řádky
- klik vede na diff s možností obnovit verzi (s heslem editoru)
- verze vznikají samy při úpravách z editoru i odjinud, úpravy do 5 minut se slučují

Historie ukáže názvy tvých souborů a časy úprav. Vymyšlené změny pro ukázky: [ukázková data](/documentation#ukazkova-data).

```md
{{history}}
{{history 20}}
{{history demo.cs.md 5}}
```

## Odpočet
`{{countdown datum}}` ukáže, kolik zbývá do data nebo kolik od něj uběhlo.
{{example odpocet}}
| zápis | ukáže |
|:--|:--|
| `{{countdown 2027-01-01}}` | „za 39 dní“, „zítra“, „dnes“, „před 3 dny“ |
| `{{countdown 2027-01-20 9:00}}` | s časem i „za 5 h“ |
| `{{countdown 2026-11-12 dny}}` | jen počet dní („3 dny“) |
| `{{countdown +12}}` | 12 dní od dneška |

Počítá prohlížeč podle svých hodin a obnovuje se každou minutu, najetí myší ukáže celé datum. Funguje kdekoli v textu.

```md
Do Nového roku {{countdown 2027-01-01}}.
Dovolená {{countdown +12}}.
```

---
#
//
##. `Shortcody`

---
#
## Shortcody
Řádek obsahující **jen** shortcode se nahradí vygenerovaným obsahem, třeba karty Server, Historie změn a RSS výše.

- `{{files}}`: seznam souborů s tlačítky *zobrazit* a *upravit*. `user` = jen tvoje, `system` = dokumentace, konfigurace a markdown.
- `{{newfile}}`: formulář pro nový `.md` soubor
- `{{theme}}`: dlaždice motivů, klik uloží `[theme] default`
- `{{lang}}`: přepínač jazyka, uloží `[page] lang`
- `{{email jméno doména}}`: chráněný e-mail
- `{{countdown datum}}`: odpočet do data nebo od něj
- `{{gear}}`: ozubené kolečko nastavení v textu

`{{email}}`, `{{countdown}}` a `{{gear}}` fungují i uprostřed řádku. Uvnitř bloku kódu se shortcode nevykoná.

```md
{{files}}
{{newfile}}
{{rss URL [počet]}}
{{sys [části…]}}
{{history [soubor] [počet]}}
{{note}} … {{/note}}
{{theme}}
{{lang}}
{{email jméno doména}}
{{countdown datum [čas] [dny]}}
{{gear}}
```
#-