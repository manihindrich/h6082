# Struktura

## Záložky
Každý soubor `content/pages/*.md` je jedna záložka v horní liště. Název záložky = jméno souboru bez `.md`. Překlad záložky je soubor `jmeno.cs.md` nebo `jmeno.en.md` a zobrazí se podle jazyka.
- uživatelské záložky jsou vlevo, pořadí určuje `[tabs] order`
- `h6082` je vpravo (`[page] about_tab`)
- skryté (`[tabs] hidden`) jsou dostupné přes `/<jméno>`
- první uživatelská záložka je na `/`
- odkaz na jinou záložku: `[config](/docs)` → [config](/docs)
- nový soubor vytvoříš a upravíš na stránce [h6082](/h6082)

## Sloupce #
Řádek `# Název` založí nový sloupec. Sloupec není vidět, jen řadí bloky pod sebe. Název slouží pro orientaci v souboru.
```md
# Dev
## Repos
…
# Infra
## Servery
…
```
- sloupce jdou zleva doprava v pořadí v souboru
- text před prvním `#` patří do prvního sloupce
- počet sloupců na řádek: šířka okna, nebo `columns_fixed`
- `#` uvnitř bloku kódu se ignoruje

## Bloky ##
`## Titulek` vytvoří orámovaný blok. Všechno až do dalšího `##` nebo `#` patří do bloku.
```md
## Repos
- [GitHub](https://github.com)
```
Obsah před prvním `##` ve sloupci tvoří blok bez titulku. Velikost písmen titulku: `block_title_transform`.

## Podnadpisy ###
Člení obsah uvnitř bloku. Jsou lehce odsazené a jejich obsah je odsazený ještě o kus víc (`h3_indent`, `content_indent`).
### Jazyky
- [Rust](https://doc.rust-lang.org/std/)
- [Python](https://docs.python.org/3/)
### Nástroje
- [Docker](https://docs.docker.com)
```md
### Jazyky
- [Rust](https://…)
```

## Nadpisy #### až ######
Malé tlumené nadpisy bez odsazení, hodí se na drobné popisky.
#### popisek 4. úrovně
##### popisek 5. úrovně
```md
#### popisek 4. úrovně
```

## Odstavce a zalomení
Řádky jdoucí po sobě se spojí do jednoho odstavce.
Prázdný řádek začne nový odstavec.

Řádek ukončený dvěma mezerami  
se zalomí. Totéž udělá `<br>`.<br>Takhle.
```md
první řádek··
zalomený řádek
```
`··` označuje dvě mezery.

Před seznamem, tabulkou, citací nebo blokem kódu nemusí být prázdný řádek, doplní se automaticky.

# Text

## Řez písma
**tučně** · *kurzíva* · ***tučná kurzíva*** · ~~přeškrtnuto~~
```md
**tučně** · *kurzíva* · ***obojí*** · ~~přeškrtnuto~~
```
Fungují i varianty s podtržítkem: `__tučně__` a `_kurzíva_`.

## Zvýraznění
Text se ==zvýrazněným úsekem==. Barvu nastavuje `mark_bg`.
```md
Text se ==zvýrazněným úsekem==.
```

## Inline kód
Příkaz `docker ps` nebo cesta `/etc/hosts`.
Inline kód se zvýrazněním syntaxe: `#!python print("hi")`
```md
`docker ps`
`#!python print("hi")`
```
Backtick uvnitř kódu: ``` `` a`b `` ```

## Klávesy
++ctrl+shift+t++ · ++alt+tab++ · ++cmd+space++ · ++f5++ · ++enter++
```md
++ctrl+shift+t++  ++f5++  ++enter++
```
Známé názvy (`ctrl`, `alt`, `shift`, `cmd`, `win`, `tab`, `esc`, `up`, `down`, `f1`–`f24`, `page-up`, …) se převedou na popisky kláves. Jednotlivé klávesy se spojují znakem `+`.

## Zkratky
Konfigurace v TOML, styl v CSS. Najeď myší na zkratku.
```md
Konfigurace v TOML.
*[TOML]: Tom's Obvious Minimal Language
```
Definice může být kdekoli ve sloupci a platí pro celý sloupec.

*[TOML]: Tom's Obvious Minimal Language
*[CSS]: Cascading Style Sheets

## Inline HTML
<small>malý text</small> · x<sup>2</sup> · H<sub>2</sub>O · <span style="color:#ff9100">barva</span> · <u>podtržení</u>
```html
<small>malý</small> x<sup>2</sup> H<sub>2</sub>O
<span style="color:#ff9100">barva</span>
```
Markdown uvnitř HTML bloku se zpracuje, jen když má blok atribut `markdown="1"`.

## Escapování
Zpětné lomítko před znakem vypne jeho formátování: \*hvězdičky\*, \# křížek, \[závorky\], \`backtick\`.
```md
\*hvězdičky\*  \# křížek  \[závorky\]
```

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

## Odkazy
- [klasický odkaz](https://example.com)
- [s tooltipem](https://example.com "titulek při najetí")
- [relativní, jiná záložka](/docs)
- [odkaz s referencí][ref]

[ref]: https://example.com
```md
[text](https://example.com)
[text](https://example.com "tooltip")
[text](/docs)
[text][ref]
[ref]: https://example.com
```
Externí odkazy se otevírají v novém tabu (`links_new_tab`).

## Auto-odkazy
- <https://example.com>
- holá URL: https://example.com/path
- e-mail: <user@example.com>
```md
<https://example.com>
https://example.com/path
<user@example.com>
```

## Chráněný e-mail
Napiš mi: {{email jmeno example.com}}
```md
{{email jmeno example.com}}
```
Jméno a doména se píšou odděleně, takže v md ani v HTML není adresa se zavináčem. Čitelnou adresu a odkaz `mailto:` složí až JavaScript v prohlížeči. Funguje kdekoli v textu, i uprostřed řádku.

## Obrázky
![h6082](/media/demo-hero.cs.svg)

![logo](/static/img/logo.svg){width=20} ikona před textem · [![](/static/img/logo.svg){width=14} odkaz s ikonou](https://example.com)
```md
![h6082](/media/demo-hero.cs.svg)
![logo](/media/ikona.svg){width=20}
[![](/media/ikona.svg){width=14} text](https://…)
```
- **vlastní obrázky** ulož do `content/media/` a vlož přes `/media/<soubor>`. Povolené jsou `svg png jpg webp gif avif ico`.
- obrázek, který je v odstavci sám, se roztáhne na šířku bloku a dostane zaoblené rohy
- menší velikost nastavíš atributem `{width=…}`
- obrázky z webu (`https://…`) fungují taky, ale prohlížeč je pak stahuje z cizího serveru

Obrázky se posílají s přísnou CSP (`sandbox`), takže skript v SVG se nespustí ani při přímém otevření.

## Odrážky
- položka
- položka
    - vnořená (4 mezery)
        - další úroveň
```md
- položka
    - vnořená
```
Odrážky se kreslí jako `›`. Fungují i `*` a `+`.

## Číslované seznamy
1. první
2. druhý
    1. vnořený
3. třetí

5. začíná od pěti
6. šestý
```md
1. první
    1. vnořený
5. začíná od pěti
```

## Úkoly
- [x] hotovo
- [ ] rozpracováno
    - [x] podúkol
    - [ ] podúkol
```md
- [x] hotovo
- [ ] rozpracováno
```
V uživatelských záložkách jdou úkoly upravovat přímo na stránce:
- klik na políčko úkol zaškrtne nebo odškrtne
- ✕ (objeví se po najetí myší) smaže úkol i s podúkoly
- pole **+ nový úkol** pod seznamem přidá úkol na konec seznamu (++enter++)

Změna se hned zapíše do md souboru. Tady v dokumentaci jsou úkoly jen pro čtení.

## Definiční seznam
TTL
: doba platnosti DNS záznamu

MTU
: max. velikost paketu
: typicky 1500 B
```md
TTL
: doba platnosti záznamu
```

# Bloky

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
Zarovnání sloupce určuje oddělovací řádek: `:--` vlevo, `--:` vpravo, `:-:` na střed. Buňky smí obsahovat inline formátování.

## Bloky kódu
```python hl_lines="2"
def hello(name):
    return f"ahoj {name}"
```
````md
```python hl_lines="2"
def hello(name): ...
```
````
- jazyk: `bash`, `python`, `yaml`, `toml`, `json`, `rust`, `nix`, `diff`, …
- `hl_lines="2 4-6"` zvýrazní řádky
- `linenums="1"` čísla řádků v jednom bloku
- schéma barev a čísla řádků globálně: sekce `[code]`

## Citace
> Krátká citace nebo poznámka.
>> vnořená citace
```md
> citace
>> vnořená
```

## Callouty
> [!note]
> Bez titulku se jako titulek použije typ.

> [!tip] Tip
> Obsah může obsahovat **markdown**, `kód` i [odkazy](https://example.com).

> [!info] Info

> [!warning] Varování

> [!danger] Nebezpečí
```md
> [!tip] Titulek
> obsah
```
Barvy: `note` · `tip` · `info` · `warning` · `danger`. Fungují i aliasy z Obsidianu a GitHubu (`important`, `caution`, `question`, `bug`, `success`, …). Callout bez obsahu je jen barevný řádek.

## Sbalitelné callouty
> [!info]- Sbalený (klikni)
> Skrytý obsah.

> [!tip]+ Rozbalený
> Lze ho sbalit.
```md
> [!info]- Sbalený
> [!tip]+ Rozbalený
```

## Admonition
!!! warning "Titulek"
    Alternativní syntaxe calloutů. Obsah je odsazený 4 mezerami.
```md
!!! warning "Titulek"
    obsah
```

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
## Nákup
{{note}}
mléko, chleba
zavolat instalatérovi
{{/note}}
````
- text mezi `{{note}}` a `{{/note}}` je obyčejný text, markdown se v něm nevykresluje
- v uživatelských záložkách se dá psát přímo na stránce. Ukládá se samo ~0,8 s po poslední změně, stav je vpravo dole.
- při psaní se stránka neobnovuje. Změny odjinud se načtou po opuštění pole.
- když se poznámka mezitím změní jinde, uložení se odmítne a nic se nepřepíše
- zápis vyžaduje heslo editoru
- tady v dokumentaci je poznámka jen pro čtení

## Oddělovač
nad čarou

---

pod čarou
```md
text

---

text
```
Před `---` musí být prázdný řádek. Jinak se z předchozího řádku stane nadpis.

## Atributy
Odstavec s vlastní barvou.
{: style="color:#00bfa5" }

**tučně oranžově**{: style="color:#ff9100" }
```md
Odstavec.
{: style="color:#00bfa5" }
**text**{: style="color:#ff9100" }
![](/img.svg){width=16}
```
Za prvek jde přidat `{#id}`, `{.třída}`, `{klíč=hodnota}` i `{: style="…" }`.

# Živé prvky

## Stav služeb
Barevná tečka před odkazem ukazuje, jestli služba odpovídá.
- [GitHub](https://github.com){.check}
- [Hacker News](https://news.ycombinator.com){.check}
- [neexistující](https://nonexistent.invalid){.check}
- [h6082 přes TCP](/h6082){check="tcp://127.0.0.1:8080"}
```md
[GitHub](https://github.com){.check}
[NAS](http://nas.lan){check="tcp://192.168.1.50:22"}
```
- `{.check}`: HTTP(S) kontrola adresy odkazu
- `{check="…"}`: vlastní cíl, `https://…` nebo `tcp://host:port`
- 🟢 odpověď < 400 · 🟠 4xx (běží, ale vyžaduje přihlášení apod.) · 🔴 5xx, timeout nebo nedostupné
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
> [!info] Demo režim
> Ukázka výše má **vymyšlené hodnoty** (`demo`), skutečné údaje o serveru tady nejsou. Hodnoty se generují přímo v prohlížeči a server se na nic neptá. Funguje to i při `[system] enabled = false`.
>
> **Přepnutí na skutečné hodnoty:** 1) v `config.toml` nastav `[system] enabled = true`, 2) z bloku odeber `demo`, např. `{{sys cpu mem disk}}`.
- části: `cpu` `mem` `swap` `load` `temp` `uptime` `disk`, bez parametrů se zobrazí všechny
- `demo` ukáže vymyšlená data přímo v prohlížeči bez dotazu na server. Hodí se do ukázek a na veřejné stránky.
- skutečné hodnoty vyžadují `[system] enabled = true`. Výchozí stav je vypnuto, protože `/api/sys` vidí každý, kdo vidí stránku.
- hodnoty se obnovují každých `[system] interval_s` sekund, na skryté kartě se neobnovují
- jde o hostitele: kontejner čte `/proc` a `/sys`, které sdílí s hostitelem
- disky podle `[system] disks`. Kontejner vidí jen prázdné složky připojené z hostitele, žádná data.
- pruh: oranžový od 70 %, červený od 90 %

Procesy a docker kontejnery záměrně nejsou. Potřebovaly by oslabit izolaci kontejneru (`pid: host`, docker socket).

## Historie změn
{{history 5 demo}}
```md
{{history}}
{{history 20}}
{{history demo.md 5}}
{{history 5 demo}}
```
> [!info] Demo režim
> Ukázka výše má **vymyšlené změny** (`demo`): smyšlené soubory a časy, bez dotazu na server. Skutečná historie by ukázala názvy tvých souborů a kdy je upravuješ.
>
> **Přepnutí na skutečnou historii:** z bloku odeber `demo`, např. `{{history 5}}`. `[history] enabled = true` je výchozí.
- poslední změny: čas, soubor, přidané a odebrané řádky
- klik vede na diff s možností obnovit verzi (s heslem editoru)
- verze vznikají samy při úpravách z editoru i odjinud. Úpravy do 5 minut se slučují.
- všechny verze souboru najdeš v editoru pod odkazem **historie**

## RSS
{{rss https://news.ycombinator.com/rss 8}}
```md
{{rss https://news.ycombinator.com/rss 8}}
```
- celý řádek = jeden feed, číslo = počet položek (výchozí `[rss] default_limit`)
- RSS 2.0, RSS 1.0 i Atom
- 💬 = odkaz na komentáře, pokud je feed má (HN ano)
- server drží feed v cache `[rss] refresh_min` minut. Při výpadku zdroje ukáže poslední známý stav.
- stránka se vykreslí hned, feed se načte dodatečně

## Shortcody
Řádek obsahující **jen** shortcode se nahradí vygenerovaným obsahem.
```md
{{files}}
{{files user}}
{{newfile}}
{{rss URL [počet]}}
{{sys [části…] [demo]}}
{{history [soubor] [počet] [demo]}}
{{note}} … {{/note}}
{{lang}}
{{email jméno doména}}
```
- `{{files}}`: seznam `.md` souborů a `config.toml` s odkazy do editoru. Varianta `system` ukáže jen systémové soubory, `user` jen tvoje (s tlačítkem ✕ pro smazání).
- `{{newfile}}`: formulář pro vytvoření nového `.md`
- `{{rss …}}`: blok s feedem (viz RSS)
- `{{sys …}}`: stav serveru (viz Server), `demo` = vymyšlená data
- `{{note}}` … `{{/note}}`: upravitelná poznámka (viz Poznámka)
- `{{history …}}`: poslední změny souborů, `demo` = vymyšlená data
- `{{lang}}`: přepínač jazyka, uloží `[page] lang` do configu
- `{{email jméno doména}}`: chráněný e-mail, jako jediný funguje i uprostřed řádku

Uvnitř bloku kódu ani uprostřed řádku se shortcode nevykoná.

