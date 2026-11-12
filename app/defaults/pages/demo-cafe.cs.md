// Demo: interní nástěnka týmu Kavárny U Mlýnku (vedoucí, baristé, pekařka, brigádníci).
// Česky demo-cafe.cs.md, anglicky demo-cafe.md pro zahraniční kolegy.
// Kavárna, lidé a čísla jsou smyšlené.

#__ O nástěnce
## ☕ Demo usecase: nástěnka týmu kavárny
![Kavárna U Mlýnku](/media/demo-cafe.cs.svg)

**Kavárnu U Mlýnku** vede Lucie se šesti lidmi: tři baristé, pekařka a dva brigádníci. Nástěnka běží na tabletu za barem a každý ji má v mobilu:

- **kdo otevírá** projde *Otevření* a odškrtá body, **kdo zavírá** *Zavření*. Druhý den je vidět, co se udělalo.
- **směny** a vzkazy pro další směnu se upravují přímo na stránce přes ✎ (bloky `##*`)
- **recepty nápojů** a postupy (ladění espressa, mléko, filtr, cold brew) jsou pro všechny stejné, chuť nezávisí na tom, kdo stojí za barem
- **nový kolega** projde *Zaučení* krok za krokem, dokumenty a čísla najde na jednom místě
- **zahraniční kolegové** mají stejnou nástěnku anglicky: [English version](/demo-cafe?lang=en)

> [!warning] Interní stránka
> Telefony a dokumenty jsou jen pro tým: nástěnku provozuj za přihlášením. Kódy od alarmu, PIN ke kase a hesla sem nepatří nikdy.

##* 📌 Vzkazy pro směnu
**čt 12. 11.** ve 14:00 přiveze Mlékárna Polná mléko, zkontrolovat teplotu při převzetí
nový sirup *perník* je ve skladu, recept v tabulce nápojů
mlýnek na decaf hlučí, servis objednán na pondělí

# Provoz
## `Provoz`

## ☀️ Otevření
- [ ] zapnout kávovar a nechat 20 min nahřát
- [ ] zkušební shot, upravit mletí (18 g → 36 g za 27–30 s)
- [ ] teploty lednic do HACCP sešitu (≤ 5 °C)
- [ ] vitrína: pečivo od pekařky, cenovky, alergeny
- [ ] otevřít směnu v pokladně
- [ ] terasa: stolky, popelníky pryč, cedule ven

## 🌙 Zavření
- [ ] backflush: voda, pak Cafiza 5 × 10 s, znovu voda
- [ ] parní tryska: otřít a odfouknout, namočit na noc
- [ ] portafiltry a sítka do roztoku
- [ ] uzavřít pokladnu, tržba do obálky a do trezoru
- [ ] odpad: třídit, sklo a kartony do dvora
- [ ] teploty lednic, zhasnout, alarm

##* 📅 Týdenní úklid
| den | úkol | kdo |
|:--|:--|:--|
| po | čištění mlýnků tabletami | ranní |
| út | odvápnění rychlovarné konvice | odpolední |
| st | objednávka kávy do 12:00 | Lucie |
| čt | hloubkové čištění lednic | ranní |
| pá | inventura mléka a sirupů | odpolední |
| ne | těsnění pák a sprchy hlav | zavírající |

##* 👥 Směny 16.–22. 11.
| den | ranní 7–13 | odpolední 13–18:30 |
|:--|:--|:--|
| po | Ondra | Kája |
| út | Ondra | Mia |
| st | Kája | Mia |
| čt | Ondra | Kája |
| pá | Mia | Ondra |
| so | Kája + brigáda | Mia |
| ne | Ondra | Kája |

Výměnu směny napiš sem a dej vědět Lucii.

#+ Bar
## `Bar`

## ☕ Nápoje
| nápoj | espresso | mléko | šálek |
|:--|:--|:--|:--|
| espresso | 18 g → 36 g, 27–30 s | — | 80 ml |
| doppio | 18 g → 36 g, celý výtěžek | — | 80 ml |
| cappuccino | 1 shot | 150 ml, pěna 1 cm | 180 ml |
| flat white | ristretto 18 g → 28 g | 120 ml, tenká pěna | 160 ml |
| latte | 1 shot | 250 ml | sklo 300 ml |
| cortado | 1 shot | 1 : 1 teplé mléko | sklo 120 ml |
| perníkové latte | 1 shot + 15 ml sirupu | 250 ml | sklo 300 ml |

??? tip "Ladění espressa"
    **Teče rychle (pod 25 s), chuť kyselá** → mlít jemněji.
    **Teče pomalu (nad 32 s), chuť hořká** → mlít hruběji.
    Dávku 18 g neměnit, ladí se jen mletím. Po každé změně dva zkušební shoty. Teplota 93 °C.

## 🥛 Mléko
1. studené mléko z lednice, konvička naplněná do třetiny
2. tryska těsně pod hladinou, nasávat vzduch, dokud není konvička vlažná (asi 37 °C)
3. trysku zanořit a točit mléko do 60–65 °C, konvička je horká na dotek
4. ťuknout o pult, zakroužit, lesklý povrch bez bublin
5. rostlinné mléko jen do 55 °C, jinak se srazí

## 💧 Filtr V60
1. 15 g kávy, mletí jako hrubá sůl, voda 94 °C, celkem 250 g
2. papírový filtr propláchnout horkou vodou, vodu vylít
3. bloom: 40 g vody, počkat 30 s
4. dolévat pomalu v kruzích do 150 g, pak do 250 g
5. hotovo za 2:30–3:00. Rychlejší = jemněji mlít, pomalejší = hruběji.

## 🧊 Cold brew
100 g hrubě mleté kávy na 1 l studené vody, 16–18 h v lednici, přecedit přes filtr.
Podává se ředěný 1 : 1 s vodou nebo mlékem, s ledem.
==Na nádobu vždy štítek s datem, vydrží 5 dní.==

# Tým
## `Tým`

## 🎓 Zaučení nováčka
- [ ] **den 1:** hygiena a HACCP, kde co je, pokladna, alergeny
- [ ] **den 2:** espresso a ladění mlýnku, čištění kávovaru
- [ ] **den 3:** mléko a latte art (srdce, tulipán)
- [ ] **den 4:** filtr, cold brew, objednávky a příjem zboží
- [ ] **den 5:** samostatná směna, zaučující je na telefonu

Zaučuje Ondra. Do konce prvního týdne podepsat BOZP a požární poučení.

## 📂 Dokumenty
- [HACCP plán a sešit teplot](https://drive.google.com) · povinné, kontrola KHS
- [Alergeny ve vitríně](https://drive.google.com) · tabulka 1–14 pro každý výrobek
- [Provozní řád](https://drive.google.com) · otevírací doba, úklid, odpad
- [BOZP a požární poplachové směrnice](https://drive.google.com)
- [Receptury pečiva](https://drive.google.com) · pro pekařku a brigádu
- [Výplaty a dovolené](https://drive.google.com) · výplata k 15. dni v měsíci

## 📞 Důležitá čísla
| kdo | telefon |
|:--|:--|
| Lucie, vedoucí | [+420 600 500 601](tel:+420600500601) |
| Pavel, majitel | [+420 600 500 602](tel:+420600500602) |
| servis kávovaru | [+420 600 500 603](tel:+420600500603) · nonstop |
| Pražírna Zrno | [+420 600 500 604](tel:+420600500604) · objednávky st |
| Mlékárna Polná | [+420 600 500 605](tel:+420600500605) · do 14:00 na zítra |
| správce domu | [+420 600 500 606](tel:+420600500606) · voda, elektřina |
| hasiči · záchranka · policie | [150](tel:150) · [155](tel:155) · [158](tel:158) · [112](tel:112) |

## 🔗 Systémy
- [Dotykačka](https://www.dotykacka.cz){.check} · pokladna, tržby
- [Směny](https://docs.google.com/spreadsheets) · rozpis a výměny
- [Pražírna Zrno](/demo-designer) · káva, etikety od designérky z vedlejší záložky

*[HACCP]: systém kritických bodů pro bezpečnost potravin
*[KHS]: krajská hygienická stanice
*[BOZP]: bezpečnost a ochrana zdraví při práci
