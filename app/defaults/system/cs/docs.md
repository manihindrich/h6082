#__ Dokumentace
## 📘 Dokumentace
Konfigurace, provoz a bezpečnost h6082. Nastavuje se v `config.toml` (**konfigurace** v bloku [Dokumentace a konfigurace](/h6082)) a v `.env`. Markdown a jeho prvky ukazuje [ukázka markdownu](/markdown).
/

[Začínáme](#funkce) · [Jak to funguje](#jak-to-funguje) · [Provoz](#aktualizace) · [Bezpečnost](#ochrana) · [Editor](#editor) · [Konfigurace](#format-configu) · [Vzhled](#cfg-layout) · [Endpointy](#stranky-a-soubory)
{: .center .big }

#__ Začínáme
## `Začínáme`

#
## Funkce
### Obsah
- záložky jako md soubory, sloupce různé šířky a bloky
- plný markdown: tabulky, callouty, úkoly, kód s kopírováním
- vlastní obrázky ze složky `content/media/`
- webový editor s obarvením, zkratkami a automatickým ukládáním
- bloky `##*`, poznámky a úkoly upravitelné přímo na stránce
- historie verzí s diffem a obnovením
### Živé prvky
- okamžité obnovení po uložení
- stav služeb (HTTP, TCP) přímo u odkazů
- RSS a stav serveru jako bloky
### Vzhled
- 12 motivů a režim auto podle systému
- rozhraní a dokumentace v angličtině a češtině
- rozložení, písmo, barvy a typografie v `config.toml`

#
## Instalace
```bash
cp .env.example .env
# do .env: UID a GID (id), heslo editoru
docker compose up -d --build
```

Lokální nastavení je v `.env`:
```bash
H6082_UID=1000          # id -u
H6082_GID=1000          # id -g
H6082_BIND=127.0.0.1    # jen tento počítač
H6082_PORT=8088
H6082_EDITOR_USER=h6082
H6082_EDITOR_PASSWORD=… # openssl rand -base64 24
H6082_ALLOWED_HOSTS=    # další hostnames, např. doména za reverzní proxy
H6082_READONLY=         # 1 = veřejná stránka jen pro čtení (viz Režim jen pro čtení)
H6082_DISK_ROOT=/var/empty
```
Po změně `.env` spusť `docker compose up -d`. Zpřístupnění do sítě popisuje blok Bezpečnost.

`extra_hosts: host.docker.internal:host-gateway` umožní kontrolovat služby běžící přímo na hostiteli. Služba ale musí poslouchat i na docker bridge, ne jen na `127.0.0.1`.

#
## Spuštění a údržba
```bash
# build + start
docker compose up -d --build
# log
docker compose logs -f h6082
# restart / stop
docker compose restart h6082
docker compose down
# aktualizace aplikace
git pull && docker compose up -d --build
# záloha (data + nastavení)
tar czf h6082.tgz content/ .env
# odinstalace a úklid starých vrstev
docker compose down --rmi local
docker image prune -f
```
Kontejner má `restart: unless-stopped`, takže se po restartu Dockeru spustí znovu.
Obsah a config se projeví hned po uložení, bez restartu. Co aktualizace změní a co ne, popisuje blok Aktualizace.

#__ Jak to funguje
## `Jak to funguje`

#
## Jak to funguje
1. server načte `pages/<záložka>.md` (nebo překlad podle jazyka)
2. rozdělí text na sloupce a bloky
3. vykreslí markdown a výsledek uloží do cache
4. při změně souboru pošle otevřeným stránkám zprávu (SSE)

## Živé změny
Otevřená stránka se po uložení sama obnoví, typicky do 0,5 s (`live_reload`). Server hlídá čas změny souborů v `content/` a pošle prohlížeči zprávu přes SSE (`/events`). Ten vymění obsah bez probliknutí a scroll zůstane.

Zelená tečka vpravo nahoře = spojení je aktivní. Po restartu kontejneru se obnoví samo. Za reverzní proxy je potřeba vypnout buffering pro `/events`.

Bez živého obnovení se při každém requestu kontroluje čas změny souborů:
- `pages/*.md` a `system/*/*.md` → přegeneruje se záložka (nový image přegeneruje vše)
- `config.toml` → přegenerují se všechny záložky
- nový nebo smazaný `.md` → změní se lišta záložek

Chyba syntaxe v TOML: zůstane poslední platný config a varování jde do logu. Neznámé klíče se ignorují a také se zalogují.

#
## Soubory
```text
docker-compose.yml
Dockerfile
.env            (lokální, necommitovat)
.env.example
app/
  server.py
  static/
  defaults/          součást image: vestavěné stránky, demo, obrázky, výchozí config
content/             jen tvoje data — aktualizace na ně nikdy nesáhne
  config.toml        tvoje konfigurace (při prvním startu zkopírovaná z výchozí)
  pages/*.md         tvoje záložky (+ překlady *.cs.md)
  system/<jazyk>/    tvoje upravené vestavěné stránky (volitelné)
  media/             tvoje obrázky
```
- `docker-compose.yml`: kontejner a jeho zpřísnění
- `.env`: lokální nastavení a heslo editoru, vzor je `.env.example`. Je v `.gitignore`.
- `config.toml`: konfigurace (tato záložka)
- `app/defaults/`: co přichází s aplikací — vestavěné stránky h6082, markdown a dokumentace v každém jazyce, demo záložky, jejich obrázky a výchozí `config.toml`
- `pages/*.md`: tvoje záložky, k nim volitelné překlady `jmeno.cs.md` a `jmeno.en.md` (viz Jazyky)
- `system/<jazyk>/`: tvoje vlastní kopie vestavěných stránek, vzniknou uložením v editoru
- `server.py`: generátor, HTTP server, API (editor, kontroly, RSS)
- `.trash/`: smazané soubory, vznikne při prvním smazání
- `.history/`: verze souborů, vznikne při první změně
- `static/`: CSS, font, ikony aplikace
- `media/`: vlastní obrázky pro záložky (`/media/<soubor>`); stejnojmenné soubory z `app/defaults/media/` slouží jako záloha

Složka `content/` je do kontejneru připojená pro zápis, aby do ní mohl ukládat webový editor. Kontejner běží pod UID:GID z `.env`, takže soubory zůstávají tvoje. Změny `app/` vyžadují rebuild.

#
## Závislosti
| komponenta | verze |
|---|---|
| Docker + Compose | v2 |
| Python (alpine) | 3.12 |
| Markdown | 3.7 |
| pymdown-extensions | 10.12 |
| Pygments | 2.18.0 |
| defusedxml | 0.7.1 |
| JetBrains Mono | 2.304 |

Build potřebuje internet (PyPI, GitHub). Za běhu jdou ven jen kontroly služeb a RSS, a to jen na adresy uvedené v md souborech.

#__ Provoz
## `Provoz`

#
## Aktualizace
Aktualizace vymění jen aplikaci (image). **Tvoje data v `content/` a `.env` zůstanou beze změny**:

| část | po aktualizaci |
|---|---|
| tvoje záložky, poznámky, úkoly | beze změny |
| `content/config.toml` | beze změny; nové volby mají výchozí hodnotu, dokud je nenastavíš |
| vestavěné stránky (h6082, markdown, dokumentace) | nová verze z image |
| tvoje upravená vestavěná stránka | zůstane tvoje; *vrátit výchozí* v editoru vrátí novou výchozí |
| demo záložky | zkopírují se jen při úplně prvním startu (značka `content/.seeded`), nikdy znovu |

První start s prázdným `content/`: zkopíruje se sem výchozí `config.toml` a demo záložky. Smazaná dema se proto už nevrátí.

Nasazení přidá svou doménu proměnnou prostředí `H6082_ALLOWED_HOSTS` (čárkami oddělené), místo úpravy `[api] allowed_hosts` ve tvém configu.

Na serveru aktualizaci dělá deploy workflow (repozitář `h6082-deploy`).

#
## Režim jen pro čtení
`H6082_READONLY=1` udělá z aplikace veřejnou stránku jen pro čtení, např. demo na internetu:

- nic nejde uložit: editor, nové soubory, mazání, poznámky, úkoly, motiv, jazyk i historie vrací `403` a jejich ovládání je skryté
- obsah je jen z image (`app/defaults/`): žádný volume, nic se nenaplňuje ani nepřepisuje
- živé obnovení (`/events`), stav serveru (`/api/sys`) a historie změn jsou vypnuté
- motiv a jazyk si návštěvník volí jen ve svém prohlížeči (cookie), server nic neukládá
- stav služeb a RSS fungují dál, jen pro cíle napsané v md souborech v image

Spouštěj ho se systémem souborů jen pro čtení a bez volume (viz `h6082-deploy-demo`). I chyba v aplikaci pak nemá kam zapsat a restart je vždy čistý.

#
## Demo režim
Bloky `{{sys}}` a `{{history}}` mají přepínač `demo`. S ním ukážou **vymyšlená data**, která vzniknou přímo v prohlížeči bez dotazu na server. Hodí se do ukázek, dokumentace a na veřejné stránky.

| blok | demo | skutečná data |
|---|---|---|
| server | `{{sys demo}}` | `{{sys}}` + `[system] enabled = true` |
| historie | `{{history 5 demo}}` | `{{history 5}}` |

Demo záložky a ukázka markdownu používají demo režim, takže neprozradí údaje o serveru ani názvy tvých souborů.

#__ Bezpečnost
## `Bezpečnost`

#
## 🛡️ Ochrana
- poslouchá jen na `127.0.0.1`
- editor a každý zápis (poznámky, úkoly, motiv, jazyk) chrání heslo (`H6082_EDITOR_PASSWORD` v `.env`)
- spouští jen vlastní skripty (CSP). `<script>` ani `javascript:` v md nefungují.
- cizí weby stránku nevloží do rámce, nepřečtou ji přes DNS rebinding a nezavolají API
- kontejner má systém souborů jen pro čtení, žádná práva navíc a limity paměti i procesů
- kontroly a RSS jdou jen na adresy z md
- zápis je atomický, mazání je jen přesun do koše
- obrázky se posílají s CSP `sandbox`, takže skript v SVG se nespustí
- fonty se při buildu ověřují přes SHA-256

## 🚫 Záměrně vynecháno
Procesy hostitele, docker kontejnery a síť. Vyžadovaly by oslabit izolaci kontejneru.

#
## ⚠️ Doporučení
- **obsah md vidí každý, kdo vidí stránku.** Hesla, tokeny a privátní adresy do něj nepatří!
- `.env` obsahuje heslo a do repozitáře nepatří (je v `.gitignore`)
- do sítě pouštěj stránku jen přes reverzní proxy s HTTPS a jméno serveru doplň do `[api] allowed_hosts`
- e-mail piš přes `{{email jméno doména}}`, roboti ho pak nepřečtou
- **skryté záložky nejsou soukromé.** Jsou dostupné přes `/<jméno>` a jejich seznam je vidět na stránce h6082.
- **heslo chrání jen zápis, číst může každý, kdo se ke stránce dostane.** Na veřejném serveru dej celý web za přihlášení v reverzní proxy.
- stav serveru (`/api/sys`) je vypnutý (`[system] enabled`). Ukázky používají `{{sys demo}}` s vymyšlenými daty. Zapni ho jen tam, kde údaje o serveru nevadí.
- v ukázkách používej `{{history demo}}`, skutečná historie ukazuje názvy souborů a časy úprav
- historie uchovává i smazaný text. Když do souboru omylem vložíš tajný údaj, smaž v editoru přes **historie** i historii souboru.

#
## 🔧 Technické detaily
- **Heslo editoru** (`H6082_EDITOR_PASSWORD` v `.env`): HTTP Basic pro `/edit/…` a všechna API, která zapisují. Porovnává se v konstantním čase a po chybném pokusu server odpovídá se zpožděním 1 s.
- **CSP**: spustí se jen skripty aplikace (nonce náhodný pro každou odpověď). `<script>`, `onclick=` ani `javascript:` z md se nespustí.
- **Rámce**: `frame-ancestors 'self'` a `X-Frame-Options: SAMEORIGIN` chrání proti clickjackingu.
- **Hlavičky**: `nosniff`, `Referrer-Policy: same-origin`, `Cross-Origin-Resource-Policy` a `Cross-Origin-Opener-Policy: same-origin`.
- **Host**: všechny stránky odpovídají jen na `Host` z `[api] allowed_hosts`, jinak 421 (ochrana proti DNS rebindingu).
- **Limity**: timeout spojení 30 s, max. 32 spojení `/events`, kontrola `Content-Length`, max. velikost souboru `max_size_kb`.
- **Kontejner**: systém souborů jen pro čtení (zápis jen do `content/` a `/tmp`), `cap_drop: ALL`, `no-new-privileges`, limit 256 MB RAM a 64 procesů.
- **Build**: verze balíčků jsou připnuté, fonty se ověřují přes SHA-256 (`ADD --checksum`). `.dockerignore` pustí do buildu jen `app/`.
- **Zápis**: editor smí jen do `content/config.toml`, `content/pages/*.md` a `content/system/<jazyk>/*.md`
- **Původ požadavků**: API přijme jen `Origin` z `[api] allowed_hosts`

## 🔒 Zápis a síť
- API vyžaduje hlavičku `X-H6082`. Cizí web v prohlížeči ji bez CORS poslat nemůže, takže jiné stránky nemůžou soubory měnit.
- zápis je atomický přes dočasný soubor a přejmenování, soubor nikdy nezůstane napůl zapsaný
- kontrola souběhu: změnu provedenou jinde editor nepřepíše
- limit velikosti `max_size_kb`
- systémové soubory (`h6082`, `markdown`, `docs`, `config.toml`) nejdou smazat, jen tvoji kopii vestavěné stránky jde vrátit na výchozí; mazání je jen přesun do `content/.trash/`
- `/api/check` a `/api/rss` pracují jen s cíli a feedy, které jsou napsané v md souborech, takže server nejde zneužít ke skenování sítě
- RSS se parsuje přes `defusedxml` (ochrana proti XML bombám a externím entitám). Do stránky se dostanou jen `http(s)` odkazy, vložené jako text, ne jako HTML.
- kontroly a RSS následují přesměrování jen na `http(s)` a nejvýš 3×

#__ Editor a obsah
## `Editor a obsah`

#+
## Editor
Ukládá se samo po chvíli bez psaní, ++ctrl+s++ uloží hned. Vpravo je živý náhled.

- **hranice editor | náhled**: táhni myší; dvojklik ji vrátí doprostřed, na zaměřené hranici fungují ++arrow-left++ ++arrow-right++. Šířka se pamatuje v prohlížeči.
- **náhled** (tlačítko vedle *zobrazit*) nebo ++alt+p++: skryje / ukáže náhled
- **přejmenovat / smazat** vedle názvu souboru: přejmenování vezme i překlady, historii a odkazy v `config.toml`; smazání přesune soubor do `content/.trash/`. U upravené systémové stránky je tu *vrátit výchozí*.
- **párování**: `` ( [ { < " ' ` `` se zavírají samy, napsání zavírací závorky ji jen přeskočí, ++backspace++ smaže prázdný pár
- **seznamy a citace**: ++enter++ pokračuje v `-`, `1.`, `- [ ]` a `>`; ++enter++ na prázdné položce seznam ukončí. ```` ```jazyk ```` + ++enter++ uzavře blok kódu.
- **odsazení**: ++tab++ / ++shift+tab++ odsadí položku seznamu nebo všechny vybrané řádky
- **označený text**: napsání `*` ho obalí kurzívou, další `*` udělá tučné; `_` kurzíva, `~` ~~přeškrtnutí~~, `=` ==zvýraznění==, `` ` `` kód (víc řádků → blok ```` ``` ````). Mezery na okrajích výběru zůstanou vně, u více řádků se obalí každý zvlášť a značky seznamu zůstanou na místě.
- **vložení URL** přes označený text vytvoří odkaz `[text](url)`
- soubor změněný jinde (vim, git) nepřepíše, nabídne *načíst ze souboru* nebo *přepsat*
- chybný TOML uloží, ale dál platí poslední platný config
- **historie** ukáže verze souboru, diff a obnovení
- přístup chrání heslo z `.env`

| zkratka | akce |
|---|---|
| ++ctrl+b++ | **tučně** |
| ++ctrl+i++ | *kurzíva* |
| ++ctrl+e++ | `kód`, u více řádků blok |
| ++ctrl+k++ | odkaz `[text]()`, z označené URL `[](url)` |
| ++ctrl+shift+x++ | ~~přeškrtnutí~~ |
| ++ctrl+shift+h++ | ==zvýraznění== |
| ++ctrl+shift+8++ | odrážky `- ` |
| ++ctrl+shift+7++ | číslovaný seznam `1. ` |
| ++ctrl+shift+9++ | úkoly `- [ ] ` |
| ++ctrl+z++ | vrátí i automatické úpravy |

Zkratky formátování přepínají: druhé stisknutí formát zase odebere. Bez výběru platí pro slovo pod kurzorem, mimo slovo vloží prázdný pár. Na Macu místo ++ctrl++ funguje ++cmd++. Formátování a zkratky platí jen pro `.md` soubory, ne pro `config.toml`.

#
## [editor]
`enabled` · `true`
: webový editor (`/edit/…`) a API pro ukládání. Heslo se nastavuje v `.env` (`H6082_EDITOR_PASSWORD`), ne tady.

`autosave_ms` · `800`
: prodleva automatického uložení po posledním stisku klávesy

`max_size_kb` · `1024`
: max. velikost ukládaného souboru

Při konfliktu editor nabídne *načíst ze souboru* nebo *přepsat*. Ovládání je v bloku Editor.

## Jazyky
Rozhraní a vestavěné stránky (h6082, markdown, dokumentace) jsou v angličtině a češtině. Jazyk se volí v rozbalovací nabídce v horní liště stránky h6082, nebo v `[page] lang`. Volba se uloží do `config.toml` a platí všude.

**Překlady vlastních záložek:** vedle `jmeno.md` ulož `jmeno.cs.md` (nebo `jmeno.en.md`). Záložka pak ukáže verzi podle zvoleného jazyka, a když překlad chybí, ukáže `jmeno.md`. V liště je jen jednou. Smazání záložky smaže i její překlady.

| soubor | kdy se zobrazí |
|---|---|
| `demo-cafe.md` | výchozí verze (tady anglicky) |
| `demo-cafe.cs.md` | při `lang = "cs"` |
| `demo-cafe.en.md` | při `lang = "en"`, volitelné místo výchozí verze |

Náhled jiného jazyka bez uložení: `/<jméno>?lang=cs`.

## Horní panel
```text
[nadpis] | [záložky…] ……… [skrytá] [jazyk ▾] [motiv ▾] ⚙ ●
```
- **nadpis**: `[page] header`
- **záložky**: uživatelské `.md` zleva, pořadí podle `[tabs] order`
- **skrytá**: zobrazí se jen při prohlížení skryté záložky (čárkovaný rámeček)
- **jazyk, motiv**: rozbalovací nabídky, jen na stránce h6082
- **⚙**: stránka h6082 (`[page] about_tab`): přehled, soubory, nastavení
- **●**: živé obnovení, zelená = připojeno

#__ Konfigurace
## `Konfigurace`

#
## Formát configu
Soubor `content/config.toml` je ve formátu TOML. Hodnoty s jednotkou jsou CSS hodnoty a píšou se jako řetězec, např. `"12px"` nebo `"1.2em"`. Barvy jsou v libovolném CSS formátu: `#rrggbb`, `rgb()`, `hsl()` nebo název.
```toml
[layout]
gap = "12px"
[colors]
accent = "#a882ff"
```
Chybějící klíč má výchozí hodnotu.

## [page]
`title` · `"h6082"`
: titulek v prohlížeči; s více záložkami se zobrazí jako `<záložka> · <title>`

`favicon` · `""`
: ikona záložky prohlížeče: `""` = vestavěný fialový diamant, jinak jeden znak nebo emoji (`"🚀"`)

`lang` · `"en"`
: jazyk rozhraní a vestavěných stránek: `en` nebo `cs`. Přepíná se i rozbalovací nabídkou v horní liště stránky h6082 (nebo shortcodem `{{lang}}`), volba se zapíše sem.

`links_new_tab` · `true`
: externí odkazy (`http`/`https`) se otevírají v novém tabu

`header` · `""`
: nadpis vlevo v horním panelu, odděleného od záložek čarou. Inline markdown, např. `"**home** · rozcestník"`. Prázdný řetězec = bez nadpisu.

`live_reload` · `true`
: stránka se po uložení `.md` nebo configu sama obnoví. Zelená tečka vpravo nahoře znamená aktivní spojení.

`about_tab` · `"h6082"`
: záložka zobrazená vpravo nahoře (výchozí je vestavěná stránka h6082). Do levé lišty se nezařadí. Bez uživatelských záložek je na `/`. `""` = žádná.

## [tabs]
`order` · `[]`
: pořadí uživatelských záložek zleva podle jména souboru. První je úvodní `/`. Soubory, které v seznamu nejsou, následují abecedně.

`labels` · `{}`
: popisky, např. `{ docs = "nápověda" }`. Výchozí popisek je jméno souboru. Popisek jde zadat i pro každý jazyk zvlášť: `{ demo-cafe = { en = "café", cs = "kavárna" } }`.

`hidden` · `[]`
: záložky skryté z lišty, dál dostupné přes `/<jméno>` a ze seznamu souborů na h6082. Vestavěné stránky (markdown, dokumentace) v liště nejsou nikdy, skrývat je netřeba.

`show_single` · `false`
: zobrazit lištu, i když existuje jen jedna uživatelská záložka
```toml
[tabs]
order  = ["dev", "infra", "notes"]
labels = { docs = "nápověda", dev = { en = "dev", cs = "vývoj" } }
hidden = ["drafts"]
```

#
## [api]
`allowed_hosts` · `["127.0.0.1", "localhost"]`
: hostname, na který server odpovídá (`Host`) a ze kterého smí volat `/api` (`Origin`). Platí pro všechny stránky. Při přístupu přes jiné jméno ho sem přidej.

## [checks]
`enabled` · `true`
: kontrola dostupnosti u odkazů s `{.check}` / `{check="…"}`

`interval_s` · `60`
: jak často se stav obnovuje (výsledky se v serveru drží o 5 s kratší dobu)

`timeout_s` · `4`
: timeout jedné kontroly

`verify_tls` · `false`
: ověřovat certifikát. `false` = projdou i self-signed (homelab); kontrola neposílá žádná data.

ICMP ping v kontejneru nejde, protože kontejner běží bez root práv. Místo něj slouží `tcp://host:port`.

## [history]
`enabled` · `true`
: historie změn všech `.md` a `config.toml`. `{{history … demo}}` (vymyšlené změny) funguje i vypnuté.

`coalesce_min` · `5`
: úpravy do tolika minut od poslední verze se slučují do jedné, takže autosave nevytváří stovky verzí

`max_versions` · `50`
: max. počet verzí na soubor

`max_age_days` · `90`
: starší verze se mažou. 3 nejnovější zůstávají vždy.

Verze je **stav souboru před změnou**. Zachytí se úpravy z editoru i odjinud (vim, git): server kontroluje soubory každé 2 s. Před obnovením se současný stav uloží jako nová verze, takže i obnovení jde vrátit. Obsah verzí, diff a obnovení jsou za heslem editoru. Blok `{{history}}` ukazuje jen časy, názvy a počty řádků.

## [markdown]
`line_breaks` · `true`
: ++enter++ v textu = nový řádek, prázdný řádek = nový odstavec. `false` vrátí klasické chování markdownu (řádky se slévají).

Řádek jen s `/` vloží prázdný řádek, `//` dva. Mimo blok (pod `#`, nad `##`) udělá mezeru mezi bloky. Řádek začínající `// text` je skrytá poznámka.

#
## [system]
`enabled` · `false`
: skutečné hodnoty pro `{{sys [části…]}}` a endpoint `/api/sys`. Ve výchozím stavu vypnuto, protože `/api/sys` vidí každý, kdo vidí stránku. `{{sys demo}}` s vymyšlenými daty funguje i vypnuté.

`interval_s` · `5`
: obnovování hodnot ve stránce

`temps` · `[]`
: typy thermal zón (`/sys/class/thermal/*/type`), např. `["x86_pkg_temp", "acpitz"]`. `[]` = automaticky: `x86_pkg_temp` jako CPU, jinak nejvyšší teplota.

`disks`
: seznam `{ label, path }`. `path` je složka **v kontejneru**, která leží na sledovaném disku.
```toml
disks = [
  { label = "/",       path = "/host/disk/root" },
  { label = "content", path = "/app/content" },
]
```
Kořenový disk vidí kontejner přes prázdnou složku hostitele `H6082_DISK_ROOT` z `.env`. Další disk = další prázdná složka v `volumes` (`:ro`). Kontejner zjistí jen velikost disku a obsah složky nevidí.

Hodnoty jsou z hostitele (`/proc`, `/sys` sdílí kontejner s jádrem). Síť, procesy a docker kontejnery chybí záměrně: vyžadovaly by `network_mode: host`, `pid: host` nebo docker socket, a to oslabuje izolaci.

## [rss]
`enabled` · `true`
: bloky `{{rss URL [počet]}}`

`refresh_min` · `15`
: doba v cache. Při chybě zdroje se ukáže poslední známý stav.

`timeout_s` · `8`
: timeout stažení, max. velikost feedu je 2 MB

`default_limit` · `10`
: počet položek, když není v shortcodu uveden

## [code]
`pygments_style` · `"monokai"`
: barevné schéma bloků kódu pro motiv **obsidian**, např. `monokai`, `dracula`, `one-dark`, `nord`, `gruvbox-dark`, `material`, `github-dark`, `solarized-dark`, `native`, `zenburn`. Ostatní motivy mají vlastní schéma. Neznámý název = `monokai` + varování v logu.

`line_numbers` · `false`
: čísla řádků ve všech blocích kódu

`wrap` · `true`
: dlouhé řádky kódu se zalamují; `false` = vodorovný posuvník

Pozadí bloků kódu je vždy `code_bg`, ze schématu se berou jen barvy tokenů.

#__ Vzhled
## `Vzhled`

#
## [layout]
`columns_fixed` · `0`
: `0` = počet sloupců podle šířky okna, `N` = N běžných sloupců na řádek

`column_min_width` · `"240px"`
: min. šířka sloupce v automatickém režimu. Sloupce `#+` / `#++` jsou 1,5× / 2× širší, `#-` / `#--` poloviční / čtvrtinové. `#__` je pás přes celou šířku. Syntaxi ukazuje [ukázka markdownu](/markdown#sloupce).

`page_max_width` · `"1600px"`
: max. šířka obsahu, `"none"` = celá šířka

`padding` · `"14px"`
: okraj stránky

`gap` · `"12px"`
: mezera mezi sloupci a pod lištou záložek

`block_gap` · `"10px"`
: svislá mezera mezi bloky ve sloupci

`block_padding` · `"6px 10px 8px"`
: vnitřní okraj bloku (CSS padding: nahoře, vpravo/vlevo, dole)

`radius` · `"6px"`
: zaoblení rohů bloků a záložek

`h3_indent` · `"2px"`
: odsazení nadpisu `###`

`content_indent` · `"10px"`
: odsazení obsahu pod `###`

Na šířce do 640 px je vždy jeden sloupec.

## [font]
`family` · JetBrains Mono
: CSS `font-family`. JetBrains Mono je přibalený v image. Jiné písmo musí být nainstalované v systému prohlížeče, např. `'"Fira Code", monospace'`.

`size` · `"13px"`
: základní velikost písma, všechno ostatní se odvozuje od ní

`line_height` · `"1.4"`
: řádkování

`block_title_transform` · `"none"`
: titulky bloků: `none`, `uppercase`, `lowercase`, `capitalize`

#
## [style]
Typografie obsahu, každý prvek má vlastní sekci: `[style.text]`, `[style.h2]` až `[style.h6]`, `bold`, `italic`, `strike`, `highlight`, `link`, `code`, `code_block`, `quote`, `list`, `task`, `callout`, `kbd`, `tip`, `table` a `bracket_round` / `square` / `curly` / `angle` pro text v závorkách.

| klíč | CSS |
|:--|:--|
| `color`, `bg` | barva textu, pozadí |
| `size`, `weight`, `style` | velikost, tloušťka, kurzíva |
| `space_before`, `space_after` | mezera nad a pod |
| `padding`, `radius`, `border` | odsazení, zaoblení, rámeček |

- `""` = vestavěný vzhled; barva může být jméno barvy motivu (`muted`, `accent`, `h3`…), pak se mění s motivem
- `em` je násobek velikosti písma: `1em` = výška písma, mezery tak rostou s `[font] size`
- všechny klíče s výchozími hodnotami a komentáři jsou ve výchozím `config.toml`
- změny se projeví hned po uložení

#
## Motivy
Výběr je v rozbalovací nabídce v horní liště stránky h6082. Volba zapíše motiv do `config.toml` jako `[theme] default` (s heslem editoru), takže platí pro všechny prohlížeče. Ostatní řádky a komentáře v configu zůstanou beze změny.

| motiv | typ | kód |
|---|---|---|
| `obsidian` | tmavý | `[code]` |
| `nord` | tmavý | nord |
| `dracula` | tmavý | dracula |
| `gruvbox-dark` | tmavý | gruvbox-dark |
| `solarized-dark` | tmavý | solarized-dark |
| `catppuccin-mocha` | tmavý | one-dark |
| `tokyo-night` | tmavý | one-dark |
| `obsidian-light` | světlý | friendly |
| `gruvbox-light` | světlý | gruvbox-light |
| `solarized-light` | světlý | solarized-light |
| `catppuccin-latte` | světlý | default |
| `paper` | světlý | default |
| `auto` | podle systému | — |

`obsidian` = barvy z `[colors]` (výchozí). `auto` volí mezi `auto_dark` a `auto_light` podle nastavení systému a mění se i za běhu.

Náhled bez uložení volby: `?theme=<motiv>`, např. [/docs?theme=paper](/docs?theme=paper).

## [theme]
`default` · `"obsidian"`
: aktivní motiv (může být i `"auto"`). Nastavuje ho i výběr na stránce h6082.

`auto_dark` · `"obsidian"`
: motiv pro `auto` při tmavém systému

`auto_light` · `"obsidian-light"`
: motiv pro `auto` při světlém systému

## [themes.*]
Vlastní motiv, nebo úprava vestavěného, když použiješ jeho jméno. Klíče jsou jako v `[colors]` plus:

`label`
: název v přepínači

`scheme` · `"dark"`
: `dark` / `light`. Určuje skupinu v přepínači a barvy prvků prohlížeče (posuvníky, formuláře).

`pygments_style`
: schéma zvýraznění kódu

Chybějící barvy se doplní z `obsidian`.
```toml
[themes.muj]
label  = "můj"
scheme = "light"
pygments_style = "friendly"
bg     = "#fafafa"
panel  = "#ffffff"
text   = "#202020"

[themes.nord]   # úprava vestavěného
accent = "#b48ead"
```

#
## [colors] základ
| klíč | výchozí | použití |
|---|---|---|
| `bg` | `#1e1e1e` | pozadí stránky |
| `panel` | `#262626` | bloky, aktivní záložka |
| `border` | `#363636` | okraje, tabulky, `---` |
| `text` | `#dcddde` | text |
| `muted` | `#999999` | odrážky, citace, neaktivní záložky |
| `accent` | `#a882ff` | aktivní záložka, checkboxy, výběr |
| `h2` | `#a882ff` | titulky bloků |
| `h3` | `#c6b6ff` | `###`, hlavičky tabulek, termíny |
| `link` | `#8a9cff` | odkazy |
| `link_hover` | `#b5c0ff` | odkaz při najetí |

## [colors] kód a zvýraznění
| klíč | výchozí | použití |
|---|---|---|
| `code_bg` | `#2b2b2b` | pozadí kódu, kláves |
| `code_fg` | `#e0a96d` | inline kód |
| `mark_bg` | `#6b5a1e` | `==zvýraznění==` |
| `quote_border` | `#555555` | linka citace |

## [colors] callouty
| klíč | výchozí | typy |
|---|---|---|
| `callout_note` | `#448aff` | note, abstract, quote, example, neznámé |
| `callout_tip` | `#00bfa5` | tip, hint, important, success |
| `callout_info` | `#00b8d4` | info, todo, question, faq |
| `callout_warning` | `#ff9100` | warning, caution, attention |
| `callout_danger` | `#ff5252` | danger, error, bug, failure |

> [!tip] Světlé téma
> Přepiš `bg`, `panel`, `border`, `text`, `muted` a `code_bg`. Pak uprav `h3`, `link` a `code_fg`, aby měly dost kontrastu.

#__ Endpointy
## `Endpointy`

#
## Stránky a soubory
`/`
: první záložka

`/<jméno>`
: záložka `pages/<jméno>.md` (nebo její překlad, viz Jazyky)

`/<jméno>?lang=en`
: náhled záložky v jiném jazyce, nic se neukládá

`/<jméno>?embed=1`
: záložka bez horního panelu (náhled v editoru)

`/edit/<soubor>`
: webový editor (`<jméno>.md`, `<jméno>.cs.md`, `system/<jazyk>/<jméno>.md` nebo `config.toml`)

`/themes.css`
: CSS všech motivů (generované z configu)

`/media/<soubor>`
: vlastní obrázky z `content/media/` (svg, png, jpg, webp, gif, avif, ico) s CSP `sandbox`

`/static/…`
: CSS, font, obrázky

`/events`
: SSE stream pro živé obnovení

`/history/<soubor>`
: seznam verzí, diff a obnovení (s heslem editoru)

`/healthz`
: healthcheck (`ok`)

#
## API pro čtení
`/api/file?name=…`
: čtení (GET) a uložení (PUT) souboru pro editor

`/api/check`
: stav služeb (POST, seznam cílů)

`/api/rss?url=…&limit=…`
: položky feedu (GET)

`/api/sys`
: stav systému pro `{{sys}}` (GET)

`/api/history?file=…&limit=…`
: poslední změny pro `{{history}}`: jen časy, soubory a počty řádků (GET)

## Pravidla
Pokud je nastavené heslo, vyžadují přihlášení `/edit/…`, `/api/file`, `/api/new` a `/api/rename`. Na jiný `Host` než z `[api] allowed_hosts` server odpoví chybou 421.

Jméno záložky smí obsahovat jen `A-Z a-z 0-9 _ . -`. Soubor s jiným jménem se ignoruje. Názvy `static`, `events`, `healthz`, `edit`, `api`, `history` a `media` jsou rezervované, stejně jako jména vestavěných stránek `h6082`, `markdown` a `docs`.

#
## API pro zápis
`/api/file?name=…` DELETE
: smazání uživatelské záložky i s jejími překlady (u překladu jen toho souboru), tj. přesun do `content/.trash/<jméno>.<čas>.md`

`/api/new`
: vytvoření nového `.md` (POST)

`/api/rename`
: přejmenování záložky i s překlady a historií (POST `{name, to}`); odkazy v `[tabs] order`, `hidden`, `labels` a `[page] about_tab` se v `config.toml` upraví samy. Překlad se přejmenuje sám.

`/api/theme`
: uložení motivu do `[theme] default` (POST, s heslem editoru)

`/api/lang`
: uložení jazyka do `[page] lang` (POST, s heslem editoru)

`/api/note`
: uložení poznámky `{{note}}` (POST, s heslem editoru)

`/api/block`
: uložení bloku `##*` upraveného přímo na stránce (POST `{file, i, orig, text}`, s heslem editoru)

`/api/tasks`
: zaškrtnutí, přidání a smazání úkolu (POST, s heslem editoru)

`/api/history/restore`, `/api/history/purge`
: obnovení verze a smazání historie (POST, s heslem editoru)
