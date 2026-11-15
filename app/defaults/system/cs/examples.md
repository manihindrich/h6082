
---
#-
## 📱 Tip pro telefon {.mobile}
Ukázky si otevři i na počítači: editor a výsledek uvidíš vedle sebe a líp pochopíš, jak z markdownu vzniká stránka.

Stránka samotná je ale pro telefony optimalizovaná, takže ji pak klidně používej jen v mobilu.

##+ Ukázky
Ukázky markdownu, kterým je homepage napsána

- [formátování textu](#scene:formatovani.md)
- [práce se sloupci](#scene:sloupce.md)
- [karty a nadpisy](#scene:karty.md)
- [seznamy](#scene:seznamy.md)
- [úkoly](#scene:ukoly.md)
- [tabulka](#scene:tabulka.md)
- [blok kódu](#scene:kod.md)
- [citace a callouty](#scene:callouty.md)
- [poznámka na stránce](#scene:poznamka.md)
- [obrázky](#scene:obrazky.md)
- [živé prvky](#scene:zive-prvky.md)
- [vzhled textu, HTML a CSS](#scene:vzhled.md)
- [řádky, poznámky, zkratky](#scene:text.md)

##+ Demo záložka
Mohla by tě zajímat konkrétní možná podoba homepage. Vše je přizpůsobitelné tomu jak to zrovna ty potřebuješ, ale hrubý nástřel úplně základních funkcí najdeš v [demo záložce](/demo).

##- Chceš vědět víc?
Kompletní dokumentaci s příklady vždy najdeš v [markdown.md](/markdown).

Další zajímavé a užitečné informace o aplikaci jsou v [dokumentaci](/documentation). Branou ke všemu je [nastavení](/settings) skryté v pravém horním rohu pod {{gear}}.

##- Skryj záložku
Záložku [Ukázky](/examples) můžeš skrýt přepínačem v hlavičce [markdown dokumentace](/markdown).

Další záložky můžeš odstranit tím, že je v [nastavení](/settings) ({{gear}}) otevřeš k editaci a v hlavičce editoru dáš odstranit.

#++
##
{{livedemo 0.75}}

{{scene formatovani.md}}
{{part pismo}}
#
##. `✍️ Formátování`
---
#
##
**tučně** · *kurzíva* · ***obojí***
~~přeškrtnuto~~ · ==zvýrazněno==
{{part klavesy}}
#
##
klávesy ++ctrl+b++
nápověda [?](ukáže se po najetí myší)
vlastní ikona [★](?místo ⓘ může být libovolný znak)
nastavení pod {{gear}} vpravo nahoře
{{hover 1}}
{{hover 2}}
{{part odkazy}}
#
##
odkaz https://code.nolog.cz/hindrich/h6082
hezký odkaz [h6082](https://code.nolog.cz/hindrich/h6082)
s titulkem [h6082](https://code.nolog.cz/hindrich/h6082 "titulek v uvozovkách po najetí myší")
jiná záložka [dokumentace](/documentation)
s referencí [h6082][repo], adresa je dole zvlášť
e-mail {{email jmeno example.com}}

[repo]: https://code.nolog.cz/hindrich/h6082

{{scene sloupce.md}}
# Sloupec
## Karta v 1. sloupci
---
/
{{after ## Karta v 1. sloupci}}
Pomocí `---` uděláš enter. Tento sloupec je tu sám a proto bude jeho obsah přes celou šířku.
{{end}}

#
## \#
defaultní šířka sloupce (`#`) je `1/x`
`x`=počet sloupců
#+
## #`+`
do zápisu sloupce můžeš přidat značku `+` nebo `-`
`#+` odpovídá `1.5x` defaultního sloupce
#-
## #`-`
`#-` je naopak `0.5x`
---
#
## \#
opět `1x` pro srovnání
#++
## #`++`
2x `+` pro `1.75x`
#--
## #`--`
`0.25x`
---
/
# 
## vlastní relativní šířka
Můžeš také specifikovat šířku sloupce pomocí čísla za `#`
---
#1.2
## #`1.2`
tj. 1.2x
#1.8
## #`1.8`
tj. 1.8x
---
#1.11
## #`1.11`
tj. 1.11x
#0.35
## #`0.35`
tj 0,35x
#3
## #`3`
tj 3x
{{after Můžeš také specifikovat šířku sloupce pomocí čísla za `#`}}
Lze použít celá čísla i čísla s desetinnou čárkou či tečkou.
{{end}}

---
/
#
## pevná šířka
Sloupec může mít i pevnou šířku v `px`, `em`, `rem` nebo `%`, např. `#120px`. Ostatní sloupce v řádku si rozdělí zbytek místa.
---
#120px
## 120px
`120px` pevně
#500px
## 500px
`500px` pevně
#200px
## 200px
`200px` pevně
{{after `120px` pevně}}
#
## zbytek
dopočítaná šířka
{{end}}
---
#100px
## 100px
`100px` pevně
#10em
## 10em
`10em` pevně
#10rem
## 10rem
`10rem` pevně
#10%
## 10%
`10%` pevně
#
## zbytek
dopočítaná šířka

{{scene karty.md}}
{{part karty}}
#
##. 🧱 Karty a nadpisy
## Karta
Každé `##` začne novou kartu s rámečkem, patří do ní vše až do dalšího `##` nebo `#`.
{{part podnadpisy}}
### Podnadpis
`###` člení obsah uvnitř karty.
#### malý popisek
`####` je tlumený popisek,
##### ještě menší
###### a nejmenší
{{part karty-sloupec}}
#
## Druhý sloupec
Další `#` = další sloupec vedle.
/
## Mezera nad kartou
Řádek `/` mezi kartami či sloupci udělá volný řádek, `//` dva.
##
Karta bez nadpisu: stačí samotné `##`.
{{part bez-ramecku}}
{{after Každé `##`}}
`##.` místo `##` je karta bez rámečku, třeba nadpis sloupce (nahoře).
{{wait 1.5}}
{{part fill}}
{{swap ## Druhý sloupec "## Roztažená karta {.fill}"}}
{{after Další `#` = další sloupec vedle.}}
`{.fill}` za nadpisem protáhne kartu do výšky nejvyššího sloupce.
{{part sbalitelne}}
{{end}}
##+ Sbalitelná karta
`##+` místo `##`: klik na nadpis kartu sbalí, `##-` je sbalená od začátku. Prohlížeč si to pamatuje.
{{fold 1}}
{{wait 1}}
{{fold 1}}

{{scene seznamy.md}}
{{part odrazky}}
#
##. `📋 Seznamy`
---
#
##
Odrážka je `-`, vnoření = 2 mezery navíc (tabulátor).
- odrážka
- další
  - vnořená
    - a ještě hlouběji
{{part cislovane}}
#
##
Číslovaný seznam: `1.`, vnoření zase 2 mezery.
1. první
2. druhý
   1. vnořený
3. třetí
{{wait 1.5}}
{{swap 1. první "5. začít jde i pětkou"}}
{{after Číslovaný seznam}}
Seznam může začít libovolným číslem, další se dopočítají.
{{part definice}}
{{end}}
#
##
Pojem a pod ním `: vysvětlení`.

TTL
: doba platnosti DNS záznamu

MX
: poštovní server domény

{{scene ukoly.md}}
{{part ukoly}}
#
##. `✅ Úkoly`
---
#
##
`- [ ]` je úkol, `- [x]` hotový úkol.
- [ ] ověřit zálohy
- [ ] aktualizovat router
  - [ ] stáhnout firmware
- [x] objednat toner
#
##
Klikni na políčko a úkol se odškrtne rovnou v souboru. Pole **+ nový úkol** přidá další.
{{tick 1}}
{{tick 3}}
{{add 1 zkontrolovat UPS}}
{{part terminy}}
#
##
Termín na konci úkolu: datum `@2026-12-01`, nebo za kolik dní `@+3`, `@-1` (včera), i s časem `@+0 14:00`.
- [ ] porada @+0 14:00
- [ ] obnovit certifikát @+2
- [ ] vrátit knihu do knihovny @-3
- [ ] prodloužit doménu @+40
- [x] podat přiznání @-10
##
Po termínu červeně, do 3 dnů oranžově, hotový šedě.
{{wait 1}}
{{tick 7}}

{{scene tabulka.md}}
#
##. `📊 Tabulka`
##
Buňky odděluje `|`, pod hlavičkou je řádek `|---|`.
| služba | port | stav |
|---|---|---|
| web | 443 | ✓ |
| ssh | 22 | ✓ |
| zálohy | — | 3:00 |
{{wait 1.5}}
{{swap |---|---|---| "|:--|:-:|--:|"}}
{{after Buňky odděluje}}
Dvojtečka zarovná sloupec: `:--` vlevo, `:-:` na střed, `--:` vpravo.
{{swap | zálohy "| zálohy | — | ~~3:00~~ **4:00** |"}}
{{end}}

V buňkách funguje i **tučné** a ~~přeškrtnuté~~.

{{scene kod.md}}
{{part inline-kod}}
#
## 💻 Kód v řádku
jednořádkový `kód` 
obarvený `#!python print("ahoj")`
backtick uvnitř: ``` `` a`b `` ```
{{part blok-kodu}}
#
## 💻 Blok kódu
```python
def greet(name):
-    return "Ahoj"
+    return f"Ahoj {name}!"  # s jménem
print(greet("světe"), 42)
```
{{end}}
s obarvením dle jazyka
{{wait 2}}
{{swap ```python "```diff"}}
{{copy 1}}
{{wait 1.5}}
{{swap ```diff '```python hl_lines="3" linenums="1"'}}
{{after s obarvením dle jazyka}}
`hl_lines="3"` zvýrazní 3. řádek, `linenums="1"` řádky očísluje.

{{scene callouty.md}}
{{part citace}}
#
##. `💬 Citace a callouty`
##
> Obyčejná citace začíná `>`.
>> `>>` je vnořená citace.

{{part callouty}}
##
> [!tip] Tip
> Callout je citace s typem `[!…]` a titulkem.

> [!warning] Pozor
> Typy: `note` `tip` `info` `warning` `danger`.
{{wait 1}}
{{swap > [!tip] Tip "> [!danger] Nebezpečí"}}
{{end}}

{{part sbalitelne-callouty}}
##
> [!info]- Sbalený callout
> `-` za typem ho sbalí, klik ho otevře.

> [!tip]+ Rozbalený callout
> `+` = otevřený, ale jde sbalit.
> Uvnitř funguje **markdown**, `kód` i [odkazy](/markdown).
{{open 1}}
{{wait 1}}
{{part callouty-typy}}
#
##. `🎨 Další úpravy`
##
> [!note]
> Bez titulku se jako titulek použije typ.

> [!success] Bez obsahu je callout jen barevný řádek.

##
Fungují i názvy z Obsidianu a GitHubu, barvu převezmou od základního typu:

> [!question] question = info

> [!bug] bug = danger

> [!example] example = note

{{part mkdocs}}
##
Zápis z MkDocs funguje taky:
!!! warning "Admonition"
    obsah odsazený 4 mezerami

??? note "Sbalený blok"
    `???+` ho otevře hned.

{{open 3}}
{{wait 1}}

{{scene poznamka.md}}
{{part poznamka}}
#
##. `📝 Poznámka`
##
Mezi `{{note}}` a `{{/note}}` je pole, do kterého se píše přímo na stránce.
{{note}}
nakoupit: mléko, chleba
{{/note}}

##
Ukládá se samo do md souboru. Markdown se v ní nevykresluje, je to čistý text.
{{note 1 zavolat instalatérovi}}
{{note 1 **tohle zůstane s hvězdičkami**}}

{{part upravitelna-karta}}
#
##. `✎ Upravitelná karta`
##* Tento týden
**po** tenis
**st** sbor

##
`##*` místo `##` přidá kartě ✎. Upravíš ji rovnou na stránce, bez editoru, a uloží se jen tato karta.
{{edit 1 **pá** kino}}
{{edit 1 **ne** výlet\n**po** zase práce}}

{{scene obrazky.md}}
#
![Údolí ve dne](/media/foto-den.svg)
---
#
##. `🖼️ Obrázky`
##
Karta jen s obrázkem (nahoře) je banner bez rámečku.
##
Obrázek sám v odstavci se roztáhne na šířku karty:
![Stéblo nad údolím](/media/foto-detail.svg "titulek v uvozovkách se ukáže po najetí myší")
##
Ikona v textu ![](/media/ikona.svg){width=20} se zmenší přes `{width=20}`.
Hodí se i do seznamu:
- ![](/media/ikona.svg){width=18} Sněžka
- ![](/media/ikona.svg){width=18} Pálava
#
##. `🧩 Další možnosti`
##
Obrázek jako odkaz: `[![](…) text](URL)`
[![](/media/ikona.svg){width=20} mapa hor](https://mapy.cz)
##
Ikony v tabulce:
| | výlet | km |
|:-:|:--|--:|
| ![](/media/ikona.svg){width=18} | Sněžka | 12 |
| ![](/media/ikona.svg){width=18} | Šumava | 25 |
##
Šířka v procentech a na střed:

![Stéblo nad údolím](/media/foto-detail.svg){width=55%}
{: .center }
##
Vlastní obrázky ulož do `content/media/` (`svg png jpg webp gif avif`) a vlož přes `![popis](/media/soubor.svg)`. Popis v `[…]` přečte čtečka obrazovky.
{{wait 1.5}}
{{swap ![Údolí ve dne] "![Údolí v noci](/media/foto-noc.svg)"}}
{{wait 1}}
{{swap Ikona v textu "Ikona v textu ![](/media/ikona.svg){width=32} se zvětší přes `{width=32}`."}}

{{scene zive-prvky.md}}
{{part stav-sluzeb}}
#
##. `🟢 Živé prvky`
---
# 
## Stav služeb
`{.check}` za odkazem: 🟢 běží, 🟠 odpovídá chybou, 🔴 neběží.
- [Web](https://example.com){.check}
- [API](https://example.com){.check .warn}
- [Záloha](https://example.com){.check .down}
{{part server}}
## Server
`{{sys}}`: procesor, paměť a disk serveru.
{{sys cpu mem disk}}
{{part rss}}
#
## RSS
`{{rss URL 3}}`: poslední 3 články z feedu.
{{rss https://news.ycombinator.com/rss 3}}
{{part historie}}
## Změny
`{{history 3}}`: poslední úpravy souborů, klik vede na rozdíl.
{{history 3}}
{{part odpocet}}
## Odpočet
`{{countdown 2026-12-24}}` kdekoli v textu, nebo za kolik dní: dovolená {{countdown +12}}.
Po datu počítá zpátky, `dny` ukáže jen počet: h6082 běží {{countdown 2026-11-12 dny}}.
{{wait 3}}

{{scene vzhled.md}}
{{part zarovnani}}
#
##. `🎯 Vzhled textu`
---
#
## ↔️ Zarovnání
Rozcestník
{: .center }

podpis vpravo
{: .right .muted }

Řádek `{: … }` hned pod odstavcem mu přidá třídy.
#
## 🔠 Velikost
malé `.small`
{: .small }

běžné písmo

větší `.big`
{: .big }

velké `.huge`
{: .huge }
{{wait 1}}
{{swap {: .center } "{: .center .huge }"}}
{{swap {: .right .muted } "{: .muted }"}}
{{part atributy}}
{{end}}
---
#
## 🎨 Barvy
Vlastní barva odstavce přes `style`:
{: style="color:#00bfa5" }

Jen kus textu: **oranžově**{: style="color:#ff9100" } a dál normálně.
#
## 🏷️ Atributy
### Podnadpis vpravo {: .right }
Odkaz do nového okna: [mapy](https://mapy.cz){target=_blank}

Kotva `{#kontakt}` za nadpisem: odkaz `[…](#kontakt)` na ni skočí.
{{part html}}
---
#
## 🧩 HTML v textu
x<sup>2</sup> · H<sub>2</sub>O · <u>podtržení</u> · <small>malý text</small>

<details><summary>HTML details</summary>skrytý obsah</details>
#
## 💅 Vlastní CSS
<span style="background:#a882ff33;border-radius:6px;padding:1px 8px">štítek</span> <span style="background:#ff910033;border-radius:6px;padding:1px 8px">⚠ pozor</span>

<span style="font-size:1.6em;letter-spacing:.2em">VELKÉ</span>

<div style="border:1px dashed #00bfa5;border-radius:10px;padding:6px 10px" markdown="1">
Rámeček z `<div>`, uvnitř **markdown** díky `markdown="1"`.
</div>
{{open 1}}
{{part zarizeni}}
---
#
## 🖥️ Jen na počítači {.desktop}
Kartu s `{.desktop}` za nadpisem vidíš jen na větší obrazovce.
## 📱 Jen na telefonu {.mobile}
Tahle karta se ukáže jen na telefonu.
#
## 📏 Hranice
Pod odstavcem `{: .mobile }` nebo `{: .desktop }` platí jen pro něj. Hranice je 640 px.

{{scene text.md}}
{{part radky}}
#
##. `📝 Text a řádky`
---
#
## Řádky
První řádek
druhý řádek (stačí Enter)
/
po řádku s `/` 
///
lze použít více lomítek za sebou pro větší rozestup, zde jsou `///`

Nový odstavec po prázdném řádku.
{{part skryte}}
## Skryté poznámky
Řádek s textem začínající `//` se nezobrazí:
{{paste}}
// zavolat Petrovi kvůli klíčům
{{/paste}}
{{part escapovani}}
## Escapování
\*hvězdičky\*, \# křížek, \[závorky\], \`backtick\`
Zpětné lomítko vypne formátování znaku.
{{part pod-carou}}
#
## Poznámky a zkratky
Tvrzení s poznámkou[^1] a zkratkou HTML.
`[^1]` odkáže na poznámku dole, `*[HTML]: …` vysvětlí zkratku po najetí myší.
{{paste}}
*[HTML]: HyperText Markup Language
[^1]: Text poznámky pod čarou.
{{/paste}}
{{part oddelovac}}
## Oddělovač
Nad čarou.

---

Pod čarou: `---` s prázdným řádkem nad sebou.
{{/livedemo}}
