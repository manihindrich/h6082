#__
/

#+ Struktura
## `Struktura`

## Záložky
Každý soubor `content/pages/*.md` je jedna záložka v horní liště.
Odkaz na jinou záložku: [dokumentace](/docs)

```md
[dokumentace](/docs)
```
Název záložky je jméno souboru bez `.md`. Překlad je soubor `jmeno.cs.md` nebo `jmeno.en.md` a zobrazí se podle zvoleného jazyka.

- uživatelské záložky jsou vlevo, pořadí určuje `[tabs] order`
- skryté (`[tabs] hidden`) jsou dostupné přes `/<jméno>`
- první uživatelská záložka je na `/`
- nový soubor vytvoříš na stránce [h6082](/h6082)

## Sloupce
Ukázka: celá tahle stránka. Každý sloupec začíná řádkem `#`.

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
#__ Pás přes celou šířku
## Novinky
…
```
| zápis | výsledek |
|---|---|
| `#` | sloupec |
| `#+` | sloupec 1,5× širší |
| `#++` | sloupec 2× širší |
| `#-` | úzký sloupec, poloviční šířka |
| `#--` | velmi úzký sloupec, čtvrtinová šířka |
| `#__` | pás přes celou šířku pod předchozími sloupci |
| `` ## `nadpis` `` | nadpis sloupce bez rámečku (blok jen s titulkem, viz Nadpis sloupce) |

- text za `#` je jen pro orientaci v souboru, na stránce se nezobrazí
- šířky jsou poměrové: `#++` vedle `#-` je čtyřikrát širší; úzké sloupce se hodí na rychlé odkazy nebo stav služeb
- sloupce, které se nevejdou, se zalomí na další řádek a roztáhnou se
- počet sloupců: šířka okna, nebo `[layout] columns_fixed`
- `#` uvnitř bloku kódu se ignoruje

## Bloky
Ukázka: každý orámovaný rámeček na této stránce.

```md
## Repos
- [GitHub](https://github.com)
```
`## Titulek` vytvoří orámovaný blok. Všechno až do dalšího `##` nebo `#` patří do něj.
Obsah před prvním `##` ve sloupci tvoří blok bez titulku.
`## Titulek {.fill}` roztáhne blok do výšky nejvyššího sloupce v řádku, takže sousední bloky končí na stejné úrovni (blok Autor na stránce [h6082](/h6082)).

## Nadpis sloupce
Ukázka: žluté nadpisy `Struktura`, `Text`, `Bloky`… nad sloupci této stránky.

```md
# Struktura
## `Struktura`

## Záložky
…
```
Blok, který má jen titulek a nic pod ním, se vykreslí jako nadpis bez rámečku a pozadí. Hodí se k pojmenování sloupce.
`kód` v jakémkoli nadpisu nemá vlastní rámeček, zůstane jen jeho barva.

## Upravitelné bloky
Ukázka: v záložce [demo-student](/demo-student) mají ✎ bloky Tento týden, Zkouškové, Bakalářská práce a Pojmový aparát.

```md
##* Nákupní seznam
- mléko
- chleba
```
`##*` místo `##` označí blok, který jde upravit přímo na stránce, bez otevírání editoru. Hodí se na průběžné drobnosti: seznamy, tabulky, krátké texty.

- po najetí myší je vpravo nahoře ✎, klik otevře markdown bloku na místě
- ++ctrl+enter++ uloží, ++esc++ zruší; funguje chytré psaní i zkratky z editoru
- uloží se jen tento blok, zbytek souboru zůstane beze změny
- když se blok mezitím změní jinde, uložení se odmítne a nic se nepřepíše
- titulek a nové bloky se mění v editoru; platí jen pro tvoje záložky a s heslem editoru

## Podnadpisy
### Jazyky
- [Rust](https://doc.rust-lang.org/std/)
- [Python](https://docs.python.org/3/)

### Nástroje
- [Docker](https://docs.docker.com)

```md
### Jazyky
- [Rust](https://doc.rust-lang.org/std/)
```
Člení obsah uvnitř bloku. Nadpis i obsah pod ním jsou lehce odsazené (`[layout] h3_indent`, `content_indent`).

## Menší nadpisy
#### popisek 4. úrovně
##### popisek 5. úrovně
###### popisek 6. úrovně

```md
#### popisek 4. úrovně
##### popisek 5. úrovně
```
Malé tlumené nadpisy bez odsazení, hodí se na drobné popisky. Vzhled: `[style.h4]` až `[style.h6]`.

## Řádky a odstavce
První řádek
druhý řádek
/
po prázdném řádku

Nový odstavec.

```md
První řádek
druhý řádek
/
po prázdném řádku

Nový odstavec.
```
- ++enter++ = nový řádek, prázdný řádek = nový odstavec s mezerou
- řádek jen s `/` vloží prázdný řádek, `//` dva, `///` tři…
- `/` mimo blok (hned pod `#`, nebo nad `##`) udělá mezeru mezi bloky
- klasické markdown chování (řádky se slévají) vrátí `[markdown] line_breaks = false`

Před seznamem, tabulkou, citací nebo blokem kódu nemusí být prázdný řádek, doplní se sám.

## Skryté poznámky
Tenhle blok obsahuje poznámku, kterou nevidíš.
// tohle se na stránce nezobrazí

```md
// poznámka jen pro mě
```
Řádek začínající `//` se nevykreslí. Hodí se na připomínky v souboru. Uvnitř bloku kódu a uprostřed řádku `//` platí jako obyčejný text.

# Text
## `Text`

## Řez písma
**tučně** · *kurzíva* · ***tučná kurzíva*** · ~~přeškrtnuto~~

```md
**tučně** · *kurzíva* · ***obojí*** · ~~přeškrtnuto~~
```
Fungují i varianty s podtržítkem: `__tučně__` a `_kurzíva_`.
V editoru: ++ctrl+b++, ++ctrl+i++, ++ctrl+shift+x++.

## Zvýraznění
Text se ==zvýrazněným úsekem==.

```md
Text se ==zvýrazněným úsekem==.
```
Barva: `mark_bg` v motivu, vzhled: `[style.highlight]`. V editoru: ++ctrl+shift+h++.

## Inline kód
Příkaz `docker ps` nebo `#!python print("hi")`

```md
`docker ps`
`#!python print("hi")`
```
`#!jazyk` na začátku zapne zvýraznění syntaxe.
Backtick uvnitř kódu: ``` `` a`b `` ```. V editoru: ++ctrl+e++.

## Klávesy
++ctrl+shift+t++ · ++alt+tab++ · ++cmd+space++ · ++f5++

```md
++ctrl+shift+t++ · ++f5++
```
Klávesy se spojují znakem `+`. Známé názvy (`ctrl`, `alt`, `shift`, `cmd`, `win`, `tab`, `esc`, `up`, `f1`–`f24`, `page-up`, …) se převedou na popisky.

## Nápověda
Ikona s nápovědou [?](Zobrazí se po najetí myší nebo po klepnutí.) a s vlastní ikonou [★](?Místo ⓘ libovolný znak.)

```md
[?](text nápovědy)
[★](?text nápovědy)
```
Nápověda se ukáže po najetí myší, na mobilu po klepnutí. `\n` v textu zalomí řádek.
Vzhled: `[style.tip]`. `[?](https://…)` zůstane obyčejným odkazem.

## Zkratky
Konfigurace v TOML, styl v CSS.

```md
Konfigurace v TOML.
*[TOML]: Tom's Obvious Minimal Language
```
Najeď myší na zkratku. Definice může být kdekoli ve sloupci a platí pro celý sloupec.

*[TOML]: Tom's Obvious Minimal Language
*[CSS]: Cascading Style Sheets

## Závorky
Text (v závorce) a [hranatá] i {složená}.

```md
Text (v závorce) a [hranatá] i {složená}.
```
Každý typ závorek jde v configu obarvit, např. `[style.bracket_round] color = "muted"` pro vedlejší poznámky. Výchozí vzhled je beze změny.

## Zarovnání a velikost
Rozcestník na střed
{: .center .big }

podpis vpravo
{: .right .muted }

```md
Rozcestník na střed
{: .center .big }

podpis vpravo
{: .right .muted }
```
Řádek `{: … }` hned pod odstavcem mu přidá třídy:

| třída | výsledek |
|:--|:--|
| `.center` / `.right` | zarovnání na střed / doprava |
| `.big` / `.huge` | větší / velké písmo |
| `.small` | menší písmo |
| `.muted` | tlumená barva |

Třídy jdou kombinovat a fungují i u nadpisů a seznamů. Vlastní styl: `{: style="…" }`, viz Atributy.

## Inline HTML
<small>malý text</small> · x<sup>2</sup> · H<sub>2</sub>O · <u>podtržení</u>

```html
<small>malý</small> x<sup>2</sup> H<sub>2</sub>O <u>podtržení</u>
```
Markdown uvnitř HTML bloku se zpracuje, jen když má blok atribut `markdown="1"`.

## Escapování
\*hvězdičky\*, \# křížek, \[závorky\], \`backtick\`

```md
\*hvězdičky\*  \# křížek  \[závorky\]
```
Zpětné lomítko před znakem vypne jeho formátování.

## Poznámky pod čarou
Tvrzení s poznámkou[^1] a další[^dlouha].

```md
Tvrzení s poznámkou[^1].
[^1]: Text poznámky.
```
Poznámky se zobrazí na konci posledního bloku ve sloupci.

[^1]: Text poznámky.
[^dlouha]: Identifikátor může být i slovo.

# Odkazy a seznamy
## `Odkazy a seznamy`

## Odkazy
[klasický odkaz](https://example.com) · [s tooltipem](https://example.com "titulek při najetí") · [jiná záložka](/docs) · [s referencí][ref]

[ref]: https://example.com

```md
[text](https://example.com)
[text](https://example.com "tooltip")
[text](/docs)
[text][ref]
[ref]: https://example.com
```
Externí odkazy se otevírají v nové záložce (`[page] links_new_tab`). V editoru: ++ctrl+k++, nebo vlož URL přes označený text.

## Auto-odkazy
<https://example.com> · https://example.com/path · <user@example.com>

```md
<https://example.com>
https://example.com/path
<user@example.com>
```
Holá adresa se zobrazí bez `https://` a koncového lomítka. Odkaz na `http://` dostane varovnou značku, kromě adres v místní síti (`192.168.…`, `*.local`, `*.lan`, `localhost`).

## Chráněný e-mail
Napiš mi: {{email jmeno example.com}}

```md
{{email jmeno example.com}}
```
Jméno a doména se píšou odděleně, takže v md ani v HTML není adresa se zavináčem. Čitelnou adresu a odkaz `mailto:` složí až JavaScript v prohlížeči. Funguje kdekoli v textu.

## Obrázky
![h6082](/media/demo-hero.cs.svg)

![logo](/static/img/logo.svg){width=20} ikona před textem · [![](/static/img/logo.svg){width=14} odkaz s ikonou](https://example.com)

```md
![h6082](/media/demo-hero.cs.svg)
![logo](/media/ikona.svg){width=20}
[![](/media/ikona.svg){width=14} text](https://…)
```
- vlastní obrázky ulož do `content/media/` a vlož přes `/media/<soubor>` (`svg png jpg webp gif avif ico`)
- obrázek sám v odstavci se roztáhne na šířku bloku
- blok bez nadpisu, ve kterém je jen obrázek, se vykreslí bez rámečku jako banner (hlavička stránky h6082)
- menší velikost nastavíš atributem `{width=…}`
- obrázky z webu (`https://…`) fungují taky, ale prohlížeč je stahuje z cizího serveru

Skript uvnitř SVG se nespustí ani při přímém otevření obrázku.

## Odrážky
- položka
- položka
  - vnořená
    - další úroveň

```md
- položka
  - vnořená
```
Vnoření stačí odsadit o 2 mezery, v editoru ++tab++. Odrážky se kreslí jako `›` (`[style.list] marker`). Fungují i `*` a `+`.
V editoru: ++ctrl+shift+8++.

## Číslované seznamy
1. první
2. druhý
   1. vnořený
3. třetí

```md
1. první
2. druhý
   1. vnořený
```
++enter++ na konci položky přidá další číslo. Seznam může začít libovolným číslem. V editoru: ++ctrl+shift+7++.

## Úkoly
- [x] hotovo
- [ ] rozpracováno
  - [x] podúkol
  - [ ] podúkol

```md
- [x] hotovo
- [ ] rozpracováno
  - [ ] podúkol
```
V tvých záložkách jdou úkoly upravovat přímo na stránce:
- klik na políčko úkol zaškrtne nebo odškrtne
- ✕ (po najetí myší) smaže úkol i s podúkoly
- pole **+ nový úkol** přidá úkol na konec seznamu

Změna se hned zapíše do md souboru. Tady v dokumentaci jsou úkoly jen pro čtení. V editoru: ++ctrl+shift+9++.

## Definiční seznam
TTL
: doba platnosti DNS záznamu

MTU
: max. velikost paketu
: typicky 1500 B

```md
TTL
: doba platnosti DNS záznamu
```
Pojem na jednom řádku, vysvětlení na dalším za `: `. Vysvětlení může být víc.

# Bloky
## `Bloky`

## Tabulky
| služba | port | stav |
|:--|--:|:-:|
| home | 8088 | ✓ |
| grafana | 3000 | ~~off~~ |

```md
| služba | port | stav |
|:--|--:|:-:|
| home | 8088 | ✓ |
```
Zarovnání určuje oddělovací řádek: `:--` vlevo, `--:` vpravo, `:-:` na střed. V buňkách funguje inline formátování.

## Bloky kódu
```python hl_lines="2"
def hello(name):
    return f"ahoj {name}"
```

````md
```python hl_lines="2"
def hello(name):
    return f"ahoj {name}"
```
````
- najeď myší na blok: vpravo nahoře je tlačítko pro zkopírování
- jazyk: `bash`, `python`, `yaml`, `toml`, `json`, `rust`, `nix`, `diff`, …
- `hl_lines="2 4-6"` zvýrazní řádky, `linenums="1"` je očísluje
- barevné schéma a čísla řádků globálně: `[code]`

## Citace
> Krátká citace nebo poznámka.
>> vnořená citace

```md
> Krátká citace nebo poznámka.
>> vnořená citace
```
++enter++ v editoru pokračuje v citaci, na prázdném řádku ji ukončí.

## Callouty
> [!note]
> Bez titulku se jako titulek použije typ.

> [!tip] Tip
> Obsah může obsahovat **markdown**, `kód` i [odkazy](https://example.com).

> [!warning] Varování

> [!danger] Nebezpečí

```md
> [!tip] Titulek
> obsah
```
Typy: `note` · `tip` · `info` · `warning` · `danger`. Fungují i aliasy z Obsidianu a GitHubu (`important`, `caution`, `question`, `bug`, `success`, …). Callout bez obsahu je jen barevný řádek.

## Sbalitelné callouty
> [!info]- Sbalený (klikni)
> Skrytý obsah.

> [!tip]+ Rozbalený
> Lze ho sbalit.

```md
> [!info]- Sbalený
> obsah
```
`-` za typem = sbalený, `+` = rozbalený, ale sbalitelný.

## Admonition
!!! warning "Titulek"
    Alternativní zápis calloutu.

```md
!!! warning "Titulek"
    obsah odsazený 4 mezerami
```
Totéž co callout, jen v syntaxi z MkDocs.

## Details
??? note "Sbalený blok"
    Obsah se zobrazí po kliknutí.

???+ tip "Otevřený blok"
    `???+` = výchozí stav rozbalený.

```md
??? note "Sbalený"
    obsah
```

## Poznámka
{{note}}
Upravitelná poznámka. Pole roste dolů podle délky textu.
Text se ukládá zpátky do md souboru.
{{/note}}

````md
{{note}}
mléko, chleba
zavolat instalatérovi
{{/note}}
````
- text mezi `{{note}}` a `{{/note}}` je obyčejný text, markdown se v něm nevykresluje
- v tvých záložkách se do ní píše přímo na stránce a ukládá se sama ~0,8 s po poslední změně
- když se poznámka mezitím změní jinde, uložení se odmítne a nic se nepřepíše
- zápis vyžaduje heslo editoru, tady v dokumentaci je jen pro čtení

## Oddělovač
nad čarou

---

pod čarou

```md
nad čarou

---

pod čarou
```
Před `---` musí být prázdný řádek, jinak se z předchozího řádku stane nadpis.

## Atributy
Odstavec s vlastní barvou.
{: style="color:#00bfa5" }

**tučně oranžově**{: style="color:#ff9100" }

```md
Odstavec.
{: style="color:#00bfa5" }
**text**{: style="color:#ff9100" }
```
Za prvek jde přidat `{#id}`, `{.třída}`, `{klíč=hodnota}` i `{: style="…" }`.

#__
//
## `Živé prvky`

# Sledování

## Stav služeb
- [GitHub](https://github.com){.check}
- [Hacker News](https://news.ycombinator.com){.check}
- [neexistující](https://nonexistent.invalid){.check}

```md
[GitHub](https://github.com){.check}
[NAS](http://nas.lan){check="tcp://192.168.1.50:22"}
```
Barevná tečka ukazuje, jestli služba odpovídá: 🟢 v pořádku · 🟠 4xx (běží, ale chce přihlášení apod.) · 🔴 5xx, timeout nebo nedostupné.

- `{.check}` kontroluje adresu odkazu přes HTTP(S)
- `{check="…"}` je vlastní cíl: `https://…` nebo `tcp://host:port`
- najetí myší ukáže kód, odezvu nebo chybu
- obnovuje se každých `[checks] interval_s`

Kontroly běží ze serveru v kontejneru. Služby na hostiteli: `host.docker.internal:<port>`. Server kontroluje jen cíle napsané v md souborech.

## Server
{{sys demo}}

```md
{{sys}}
{{sys cpu mem disk}}
{{sys demo}}
```
- části: `cpu` `mem` `swap` `load` `temp` `uptime` `disk`, bez parametrů se zobrazí všechny
- hodnoty se obnovují každých `[system] interval_s` sekund
- pruh je oranžový od 70 %, červený od 90 %

> [!info] Demo režim
> Ukázka výše má **vymyšlené hodnoty** (`demo`), generuje je prohlížeč a server se na nic neptá.
> Skutečné hodnoty: v `config.toml` nastav `[system] enabled = true` a z bloku odeber `demo`. Výchozí stav je vypnuto, protože `/api/sys` vidí každý, kdo vidí stránku.

# Feedy a historie

## RSS
{{rss https://news.ycombinator.com/rss 5}}

```md
{{rss https://news.ycombinator.com/rss 5}}
```
- celý řádek = jeden feed, číslo = počet položek (výchozí `[rss] default_limit`)
- RSS 2.0, RSS 1.0 i Atom
- 💬 = odkaz na komentáře, pokud je feed má
- server drží feed v cache `[rss] refresh_min` minut a při výpadku zdroje ukáže poslední známý stav

## Historie změn
{{history 5 demo}}

```md
{{history}}
{{history 20}}
{{history demo-family.cs.md 5}}
```
- poslední změny: čas, soubor, přidané a odebrané řádky
- klik vede na diff s možností obnovit verzi (s heslem editoru)
- verze vznikají samy při úpravách z editoru i odjinud, úpravy do 5 minut se slučují

> [!info] Demo režim
> Ukázka výše má **vymyšlené změny** (`demo`). Skutečná historie by ukázala názvy tvých souborů a časy úprav. Stačí z bloku odebrat `demo`.

#+ Editor a ukázky

## Našeptávání v editoru
{{livedemo 8}}
{{scene napoveda.md}}
##* Termíny
**1. 3.** pojištění
> [!tip] Tip
> Editor napoví i shortcody.
{{rss https://news.ycombinator.com/rss 3}}
{{/livedemo}}

```md
#        → sloupce a bloky: #+ #- #__ ## ##* …
{{       → shortcody: {{rss URL 5}}, {{note}} …
> [!     → callouty: tip, warning, danger … i sbalené
{.       → třídy: .check .center .big .fill …
](/      → názvy tvých stránek
- [      → úkol
```
- nabídka se ukáže jen po těchto začátcích, ne u každého slova
- ++arrow-up++ ++arrow-down++ vybírá, ++enter++ nebo ++tab++ potvrdí, ++esc++ zavře; bez nabídky ++enter++ funguje jako obvykle
- u shortcodu se po potvrzení označí parametr (`URL`), stačí ho přepsat
- funguje v editoru i při úpravě bloku `##*` na stránce, ne na dotykových zařízeních; vypnutí: `[editor] suggest = false`

## Živá ukázka
{{livedemo 12}}
#
## Odkazy
- [Mapy](https://mapy.cz)
#
## Dnes
- [ ] nakoupit
{{/livedemo}}

```md
{{livedemo 12}}
#
## Odkazy
- [Mapy](https://mapy.cz)
#
## Dnes
- [ ] nakoupit
{{/livedemo}}
```
- okno editoru postupně „píše“ markdown mezi značkami a náhled pod ním se po každém řádku překreslí
- číslo = délka jednoho průchodu v sekundách (výchozí 30), pak 4 s pauza a znovu od začátku
- ❚❚ v liště okna animaci zastaví; mimo obrazovku stojí sama, při omezeném pohybu v systému se ukáže rovnou hotový stav
- obsah je jen ukázka: úkoly nejdou odškrtnout a nepočítají se mezi úkoly stránky

# Přehled shortcodů

## Shortcody
Ukázka: bloky Server, Historie změn a RSS vlevo.

```md
{{files}}
{{newfile}}
{{rss URL [počet]}}
{{sys [části…] [demo]}}
{{history [soubor] [počet] [demo]}}
{{note}} … {{/note}}
{{livedemo [sekundy]}} … {{/livedemo}}
{{theme}}
{{lang}}
{{email jméno doména}}
```
Řádek obsahující **jen** shortcode se nahradí vygenerovaným obsahem.

- `{{files}}`: seznam souborů s tlačítky *zobrazit* a *upravit*. `user` = jen tvoje, `system` = dokumentace, konfigurace a markdown.
- `{{newfile}}`: formulář pro nový `.md` soubor
- `{{livedemo [sekundy]}} … {{/livedemo}}`: animované okno editoru s živým náhledem, viz [Živá ukázka](#ziva-ukazka)
- `{{theme}}`: dlaždice motivů, klik uloží `[theme] default`
- `{{lang}}`: přepínač jazyka, uloží `[page] lang`
- `{{email jméno doména}}`: chráněný e-mail, jako jediný funguje i uprostřed řádku

Uvnitř bloku kódu se shortcode nevykoná.
