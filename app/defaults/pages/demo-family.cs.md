// Demo: rodina Dvořákových. Petra a Tomáš, Ema (9) a Kuba (6). Nástěnka běží na tabletu
// v kuchyni a oba rodiče ji mají v mobilu. Osoby a kontakty jsou smyšlené.

#__ O nástěnce
## 🏡 Demo usecase: rodinná nástěnka
![Dvořákovi: týden, nákup, kroužky](/media/demo-family.cs.svg)

**Dvořákovi** jsou čtyři: Petra, Tomáš, Ema (9) a Kuba (6). Nástěnka visí na tabletu v kuchyni a rodiče ji mají i v mobilu. Nahradila papíry na lednici, skupinový chat a pět aplikací:

- **v neděli večer** naplánují jídelníček na týden přes ✎ (blok je v souboru `##*`) a z něj dopíšou nákup
- **kdokoli a odkudkoli** přidá do *Nákupu* položku polem *+ nový úkol*, v obchodě ji pak odškrtne v mobilu
- **ráno** se podívají na *Kroužky a vyzvedávání*, kdo dnes jede pro koho
- **blížící se platby** (STK, pojištění, poplatky) jsou zvýrazněné, nic nepropadne
- **vzkazy na lednici** píšou do poznámky, která se ukládá sama
- **chytrá domácnost**: scény jedním klikem, tečky ukážou, jestli běží modem, centrála, televize a senzory, a baterie senzorů hlídá tabulka
- *Kdo co změnil* ukazuje, kdo naposledy upravoval nákup nebo jídelníček

# Týden
## `Týden`

##* 🍽️ Jídelníček
| den | oběd (víkend) / večeře |
|:--|:--|
| Po | čočka na kyselo, vejce |
| Út | kuřecí stehna, rýže, okurkový salát |
| St | **bramboráky** podle babičky |
| Čt | těstoviny s rajčaty a mozzarellou |
| Pá | pizza doma, Kuba chce „jen sýr“ |
| So | svíčková u babičky Jarky |
| Ne | rizoto se zbytky, buchta |

## 🛒 Nákup
- [ ] brambory 2 kg
- [ ] vejce 10 ks
- [ ] mozzarella, rajčata
- [ ] ovesné mléko (Ema)
- [x] toaletní papír
- [ ] dárek na oslavu, sobota (Kuba)

<small>Položku přidá kdokoli polem *+ nový úkol* pod seznamem, i z mobilu.</small>

##* 🚸 Kroužky a vyzvedávání
| den | kdo | co | kde | vyzvedne |
|:--|:--|:--|:--|:--|
| Po | Ema | plavání 16:00 | Šutka | Tomáš |
| Út | Kuba | fotbal 16:30 | Bohemians, Ďolíček | Petra |
| St | Ema | klavír 15:00 | ZUŠ Taussigova | babička |
| Čt | Kuba | keramika 15:30 | DDM Spirála | Petra |
| Pá | oba | družina do 17:00 | škola | Tomáš |

## 📝 Vzkazy na lednici
{{note}}
Kuba potřebuje na pátek přezůvky do družiny.
Kotel: servis domluvený na 2. 12. dopoledne, někdo doma!
Ema chce na Vánoce bruslařský kurz, ne dárek.
{{/note}}

#+ Domácnost
## `Domácnost`

##* 💳 Platby a termíny
| co | kdy | částka | jak |
|:--|:--|--:|:--|
| hypotéka | 15. každý měsíc | 21 400 Kč | trvalý příkaz |
| záloha elektřina a plyn | 20. každý měsíc | 3 900 Kč | inkaso |
| družina, Kuba | do 10. v měsíci | 900 Kč | převod, VS v Bakalářích |
| ==STK Octavia== | ==do 3. 12.== | 1 350 Kč | objednáno na 28. 11. |
| povinné ručení | 1. 2. | 6 200 Kč | ročně |
| poplatek za odpad, 4 osoby | do 31. 5. | 4 × 1 200 Kč | Portál občana |
| daň z nemovitých věcí | do 31. 5. | 1 870 Kč | složenka, nebo QR |

> [!tip]- Kde co najdeme
> Smlouvy, pojistky a technický průkaz jsou naskenované v rodinném Disku ve složce *Domácnost*. Originály v šanonu v obýváku, druhá polička.

## 🏠 Chytrá domácnost
### Ovládání
[🌙 Večer](http://homeassistant.local:8123/lovelace/sceny) · [🎬 Film](http://homeassistant.local:8123/lovelace/sceny) · [🚪 Odchod z domu](http://homeassistant.local:8123/lovelace/sceny) [?](Zhasne všude, vypne televizi a stáhne topení na 17 °C. Hlásí, jestli zůstalo otevřené okno.)
[💡 Světla](http://homeassistant.local:8123/lovelace/svetla) · [🌡️ Topení](http://homeassistant.local:8123/lovelace/topeni) · [📷 Kamera u vchodu](http://homeassistant.local:8123/lovelace/kamera)

### Dostupnost
- [Internet](https://1.1.1.1){check="tcp://1.1.1.1:53"} · připojení ven
- [Modem a Wi-Fi](http://192.168.1.1){check="tcp://192.168.1.1:80"} · router v předsíni
- [Home Assistant](http://192.168.1.10:8123){check="tcp://192.168.1.10:8123"} · centrála
- [Zigbee brána](http://192.168.1.11){check="tcp://192.168.1.11:80"} [?](Přes ni jdou senzory oken a dveří. Když svítí červeně, senzory nehlásí nic.)
- [Světla, Hue bridge](http://192.168.1.12){check="tcp://192.168.1.12:443"}
- [PC v pracovně](http://192.168.1.20){check="tcp://192.168.1.20:445"} · sdílené fotky
- [Televize](http://192.168.1.30){check="tcp://192.168.1.30:8009"} · obývák

<small>Adresy v demu jsou smyšlené, červená tečka znamená, že zařízení v síti není. U tebe ukáže skutečný stav.</small>

### Senzory
| senzor | kde | baterie |
|:--|:--|:-:|
| dveře | vchod | 82 % |
| okno | ložnice | 64 % |
| okno | dětský pokoj | ==12 %== |
| únik vody | pod pračkou | 91 % |
| kouř | chodba | 77 % |

> [!warning]- Baterie v dětském pokoji
> Senzor okna v dětském pokoji má 12 %. Náhradní baterie CR2032 jsou v šuplíku u lednice.

##* ⚙️ Automatizace
| kdy | co |
|:--|:--|
| otevřené okno déle než 10 min | vypnout topení v místnosti, upozornit do mobilu |
| únik vody pod pračkou | zavřít ventil, hlasitá notifikace oběma |
| 22:30 ve všední den | vypnout televizi a světla v obýváku |
| nikdo doma (oba telefony pryč) | scéna Odchod z domu |

## 🏫 Škola, město, úřady
- [Bakaláři](https://www.bakalari.cz){.check} · známky, omluvenky, platby za družinu
- [Portál občana](https://obcan.portal.gov.cz){.check} · poplatky, výpis bodů, doklady
- [Datová schránka](https://www.mojedatovaschranka.cz){.check} · úřední pošta
- [PID odjezdy](https://pid.cz){.check} · tramvaj do školy
- [ČHMÚ výstrahy](https://www.chmi.cz){.check} · počasí, smog, vichřice

## 📞 Kontakty
| kdo | kontakt |
|:--|:--|
| pediatrička MUDr. Veselá | [+420 600 400 501](tel:+420600400501) · objednávky 7–9 h |
| zubař MUDr. Krejčí | [+420 600 400 502](tel:+420600400502) |
| třídní Emy, Mgr. Pokorná | {{email pokorna skola.example}} |
| babička Jarka | [+420 600 400 503](tel:+420600400503) |
| instalatér pan Doležal | [+420 600 400 504](tel:+420600400504) · kotel i voda |

## 🕓 Kdo co změnil
{{history 6 demo}}

<small>Ukázka má vymyšlené změny (`demo`). Skutečná historie ukazuje, kdo a kdy upravil nákup, jídelníček nebo platby, a dá se vrátit.</small>

# Jídlo a okolí
## `Jídlo a okolí`

##* ⭐ Oblíbená jídla
| jídlo | kdo nejvíc | recept |
|:--|:--|:--|
| bramboráky | všichni | babiččin sešit, str. 12 |
| svíčková | Tomáš | [rodinná kuchařka](https://docs.google.com) |
| kuře na paprice | Kuba | [rodinná kuchařka](https://docs.google.com) |
| zeleninové lasagne | Ema, Petra | [rodinná kuchařka](https://docs.google.com) |
| palačinky | děti, neděle ráno | z hlavy: 2 vejce, ¼ l mléka, 8 lžic mouky |

## 🕒 Obchody v okolí
| | po–pá | so | ne |
|:--|:--|:--|:--|
| Albert, Kobylisy | 6–22 | 6–22 | 7–22 |
| Lidl, Střelničná | 7–22 | 7–22 | 7–21 |
| pekárna u tramvaje | 6:30–18 | 7–12 | zavřeno |
| lékárna u metra | 8–19 | 8–12 | zavřeno |
| pošta Kobylisy | 8–18 | 8–11 | zavřeno |
| sběrný dvůr | 9–18 | 8–15 | zavřeno |

> [!info]- Kdy mají velké obchody zavřeno
> Prodejny nad 200 m² mají podle zákona o prodejní době zavřeno 1. 1., na Velikonoční pondělí, 8. 5., 28. 9., 28. 10., 25. 12. a 26. 12. Na Štědrý den jen do 12:00. Malé obchody a lékárny to nemusí dodržovat.

## 🍲 Inspirace na vaření
### TopRecepty
{{rss https://www.toprecepty.cz/rss/ 4}}

### Apetit
{{rss https://www.apetitonline.cz/rss 3}}

##* 🎁 Narozeniny a přání
| kdo | kdy | přání |
|:--|:--|:--|
| Ema | 12. 1. | bruslařský kurz, knihy o koních |
| Kuba | 3. 4. | dres Bohemians, stavebnice |
| babička Jarka | 28. 2. | výlet do Lednice |
| Petra | 9. 6. | ~~nový mixér~~ (už má), wellness víkend |
