// Demo: Martin, klíčový pracovník v chráněném bydlení (nezisková organizace).
// Má na starosti tři klienty. Všechny osoby, kontakty a čísla jsou smyšlené.
// Řádky začínající // se na stránce nezobrazují.

#__ O nástěnce
## 🤝 Demo usecase: klíčový pracovník v sociální službě
![chráněné bydlení se třemi rozsvícenými okny a síť podpory kolem](/media/demo-key-worker.cs.svg)

**Martin** pracuje jako klíčový pracovník v chráněném bydlení a má na starosti tři klienty. Na každého potřebuje mít po ruce kontakty na rodinu a opatrovníka, lékaře, úřady, individuální plán a dokumenty. Dřív to hledal ve třech šanonech a pěti složkách na Disku. Teď má na sdíleném počítači služby otevřenou tuhle nástěnku:

- **na začátku směny** si přečte *Předávku* od kolegyně a zkontroluje *Dnešek*. Rozpis dne i předávku upravuje přímo na stránce přes ✎, bloky jsou v souboru označené `##*`.
- **u klienta** otevře jeho kartu: komu volat, jaké má léky a kontroly, co je v individuálním plánu a kde na Disku leží dokumenty
- **krizové informace** (alergie, postup při záchvatu) jsou ve výrazném rámečku, aby je našel i zástup, který klienta nezná
- **přání klientů** si sbírá do jedné tabulky. Před narozeninami nebo Vánoci pak ví, co komu udělá radost.
- **legislativa a standardy** jsou v poznámkách pod čarou, stačí najet na číslo

> [!danger] Citlivé údaje
> Zdravotní a právní informace o klientech jsou zvlášť chráněné osobní údaje. Nástěnku s nimi provozuj jen ve vnitřní síti služby a celý web dej za přihlášení (reverzní proxy). V odkazech na Disk nech jen názvy složek, samotné dokumenty zůstávají za přístupem organizace. V tomto demu jsou všechny osoby smyšlené.

# Služba
## `Služba`

##* 🗓️ Dnešek, čt 12. 11.
| čas | kdo | co |
|:--|:--|:--|
| 8:30 | Petr | doprovod na neurologii, karta + seznam léků |
| 10:00 | Lenka | keramická dílna, vyzvednout 12:00 |
| 13:30 | Jiří | logopedie (přijde domů) |
| 15:00 | tým | porada, revize IP Petra |

##* 📋 Předávka směny
Lenka v noci nespala, ráno klidná. Nabídnout odpočinek po dílně.
Jiřímu došly pleny, objednáno, dodání v pátek.
Petrovi přišel dopis z ÚP (kontrola PnP), je ve složce *Úřady*.

## 📞 Kontakty služby
| | |
|:--|:--|
| vedoucí služby | Hana Kubíčková · [+420 600 100 200](tel:+420600100200) |
| zdravotní sestra | Eva Malá · [+420 600 100 201](tel:+420600100201) |
| noční služba | [+420 600 100 299](tel:+420600100299) |
| záchranná služba | [155](tel:155) · tísňová linka [112](tel:112) |
| krizová linka | [116 123](tel:116123) Linka první psychické pomoci |

## 🧭 Systémy
- [Cygnus](https://www.iscygnus.cz) [?](Informační systém služby: záznamy o průběhu služby, individuální plány, léky) · dokumentace
- [Google Disk služby](https://drive.google.com) · složky klientů
- [Směnový rozpis](https://docs.google.com/spreadsheets) · tabulka týmu
- [Registr poskytovatelů](https://iregistr.mpsv.cz) · údaje o registraci služby
- [MPSV](https://www.mpsv.cz) · příspěvek na péči, sociální služby

/

##* 🎁 Přání klientů
| kdo | přání | příležitost | stav |
|:--|:--|:--|:-:|
| Petr | rádio s velkými tlačítky | narozeniny 3. 2. | 💡 |
| Petr | zápas Bohemians, Ďolíček | jaro | 🎟️ |
| Lenka | sluchátka s potlačením hluku | Vánoce | 🛒 |
| Jiří | videohovor se synem každou neděli | průběžně | ✓ |

## ✅ Tento týden
- [ ] revize individuálního plánu Petra (porada čt)
- [ ] odeslat formulář ke kontrole PnP, Petr, do 20. 11.
- [ ] objednat poukaz na nový vozík pro Jiřího (praktický lékař)
- [x] domluvit s matkou Lenky víkendovou návštěvu

*[IP]: individuální plán
*[PnP]: příspěvek na péči
*[ÚP]: Úřad práce ČR

#++ Klienti
## `Klienti`

## 👤 Petr N., 54 let
středně těžké mentální postižení, epilepsie · v bydlení od 2019

!!! danger "Epileptický záchvat"
    Uložit do bezpečí, nic nedávat do úst, měřit čas. **Záchvat delší než 5 minut nebo opakovaný → volat 155.** Záchranka může podat lék podle karty, ta je v pokoji v modré složce.

Silné vztahy (sestra, kamarád, dílna) jsou opora pro cíle individuálního plánu. Zátěžová je teď kontrola příspěvku na péči, při jednání s ÚP chce mít Petr u sebe sestru.

### Kontakty
| kdo | vztah | kontakt |
|:--|:--|:--|
| Jana N. | sestra, **opatrovnice**[^opatrovnik] | [+420 600 200 301](tel:+420600200301) · {{email jana.n example.cz}} |
| Tomáš | kamarád z chráněné dílny | přes dílnu, út a čt |
| MUDr. Svoboda | praktický lékař | [+420 600 200 302](tel:+420600200302) |
| MUDr. Králová | neurologie FN Motol | ~~19. 11.~~ přesunuto na **3. 12.** |

### Individuální plán[^ip]
- [x] sám dojde do pekárny za rohem a zaplatí
- [ ] jízda tramvají do dílny, zatím s doprovodem (cíl: sám do června)
- [ ] vlastní kapesné: týdenní obálka, společně zapisovat výdaje

### Úřady a dokumenty
- příspěvek na péči[^pnp] **III. stupeň**, kontrola ÚP probíhá
- invalidní důchod III. stupně (ČSSZ)
- [📁 Petr: individuální plán](https://drive.google.com) · [📁 zdravotní](https://drive.google.com) · [📁 úřady a soud](https://drive.google.com)

/

## 👤 Lenka K., 31 let
porucha autistického spektra, nemluví, komunikuje piktogramy a tabletem · v bydlení od 2022

!!! warning "Alergie: penicilin"
    Při každém ošetření hlásit. Uvedeno v kartě pojištěnce i v Cygnusu.

??? tip "Jak s Lenkou komunikovat"
    Mluvit krátce a klidně, jedna věc najednou. Změny programu ukázat předem na denním rozvrhu s piktogramy. Hluk a dotyk bez upozornění zvyšují napětí, sluchátka má v batohu. Ano/ne ukazuje na tabletu nebo kývnutím.

### Kontakty
| kdo | vztah | kontakt |
|:--|:--|:--|
| Marie K. | matka, **opatrovnice** | [+420 600 300 401](tel:+420600300401) · víkendy u rodiny |
| Pavel K. | otec | [+420 600 300 402](tel:+420600300402) |
| MUDr. Dvořák | psychiatr | kontrola á 3 měsíce, další **14. 1.** |
| Keramická dílna | denní aktivita | po, st, čt 10–12 |

### Individuální plán[^ip]
- [x] samostatně si vybrat oblečení podle počasí (piktogramy u skříně)
- [ ] přechod na nový tablet: přenést komunikační sadu, procvičit
- [ ] zkusit druhou dílnu (zahrada) jednou týdně

### Dokumenty
[📁 Lenka: IP a komunikační sada](https://drive.google.com) · [📁 zdravotní](https://drive.google.com) · [📁 úřady](https://drive.google.com)

/

## 👤 Jiří V., 67 let
po cévní mozkové příhodě, na vozíku, mírná afázie · svéprávný · v bydlení od 2024

### Kontakty
| kdo | vztah | kontakt |
|:--|:--|:--|
| Ondřej V. | syn, **podpůrce**[^podpurce], žije v Mnichově | [+49 160 0000 000](tel:+491600000000) · neděle 18:00 videohovor |
| Klub seniorů Nusle | přátelé | út odpoledne |
| Mgr. Horká | logopedie | čt 13:30 doma |
| Fyzioterapie | rehabilitace | po a st, ambulance Nusle |

### Individuální plán[^ip]
- [x] videohovory se synem: tablet, nastavená zkratka na ploše
- [ ] obnovit návštěvy klubu seniorů (doprava: sociální taxi)
- [ ] nácvik přesunu z vozíku na lůžko s jednou osobou

### Úřady a dokumenty
- příspěvek na péči[^pnp] **IV. stupeň**, průkaz ZTP/P
- nový mechanický vozík: poukaz od praktického lékaře → pojišťovna
- [📁 Jiří: IP](https://drive.google.com) · [📁 zdravotní a pomůcky](https://drive.google.com)

[^opatrovnik]: Opatrovníka jmenuje soud, rozsah omezení svéprávnosti je v rozsudku (složka *úřady a soud*).
[^ip]: Individuální plánování průběhu služby, standard kvality sociálních služeb č. 5 (příloha č. 2 vyhlášky č. 505/2006 Sb.).
[^pnp]: Příspěvek na péči podle zákona č. 108/2006 Sb., o sociálních službách, o přiznání a kontrole rozhoduje Úřad práce.
[^podpurce]: Smlouva o nápomoci při rozhodování (§ 45 a násl. občanského zákoníku): člověk rozhoduje sám, podpůrce mu pomáhá.

*[IP]: individuální plán
*[PnP]: příspěvek na péči
*[ÚP]: Úřad práce ČR
*[ČSSZ]: Česká správa sociálního zabezpečení
*[ZTP/P]: průkaz pro osobu zvlášť těžce postiženou s průvodcem
