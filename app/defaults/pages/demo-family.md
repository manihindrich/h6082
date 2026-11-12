// Demo: the Dvořák family. Petra and Tomáš, Ema (9) and Kuba (6). The board runs on a tablet
// in the kitchen and both parents have it on their phones. People and contacts are made up.

#__ About this board
## 🏡 Demo use case: a family board
![The Dvořáks: week, shopping, after-school activities](/media/demo-family.svg)

**The Dvořáks** are a family of four: Petra, Tomáš, Ema (9) and Kuba (6). The board hangs on a tablet in the kitchen and the parents have it on their phones too. It replaced the papers on the fridge, the group chat and five apps:

- **on Sunday evening** they plan the week's menu with ✎ (the block is `##*` in the file) and add the shopping from it
- **anyone, from anywhere** adds an item to *Shopping* with the *+ new task* field, and ticks it off on the phone in the shop
- **in the morning** they check *Activities and pick-ups* to see who is picking up whom today
- **upcoming payments** (STK, insurance, fees) are highlighted, nothing gets missed
- **fridge notes** go into a note that saves itself
- **smart home**: scenes with one click, the dots show whether the modem, hub, TV and sensors are running, and a table keeps an eye on the sensor batteries
- *Who changed what* shows who last edited the shopping or the menu

# Week
## `Week`

##* 🍽️ Menu
| day | lunch (weekend) / dinner |
|:--|:--|
| Mon | sour lentils (čočka na kyselo), egg |
| Tue | chicken thighs, rice, cucumber salad |
| Wed | **potato pancakes** (bramboráky) Grandma's way |
| Thu | pasta with tomatoes and mozzarella |
| Fri | homemade pizza, Kuba wants "just cheese" |
| Sat | svíčková (beef in cream sauce) at Grandma Jarka's |
| Sun | leftovers risotto, buchta (sweet bun) |

## 🛒 Shopping
- [ ] potatoes 2 kg
- [ ] eggs 10 pcs
- [ ] mozzarella, tomatoes
- [ ] oat milk (Ema)
- [x] toilet paper
- [ ] present for a party, Saturday (Kuba)

<small>Anyone can add an item with the *+ new task* field below the list, even from a phone.</small>

##* 🚸 Activities and pick-ups
| day | who | what | where | picks up |
|:--|:--|:--|:--|:--|
| Mon | Ema | swimming 16:00 | Šutka | Tomáš |
| Tue | Kuba | football 16:30 | Bohemians, Ďolíček | Petra |
| Wed | Ema | piano 15:00 | ZUŠ (art school) Taussigova | Grandma |
| Thu | Kuba | pottery 15:30 | DDM (children's leisure centre) Spirála | Petra |
| Fri | both | after-school club until 17:00 | school | Tomáš |

## 📝 Fridge notes
{{note}}
Kuba needs indoor shoes for the after-school club on Friday.
Boiler: service booked for 2 Dec in the morning, someone at home!
Ema wants a skating course for Christmas, not a present.
{{/note}}

#+ Household
## `Household`

##* 💳 Payments and deadlines
| what | when | amount | how |
|:--|:--|--:|:--|
| mortgage | 15th of every month | 21 400 Kč | standing order |
| electricity and gas advance | 20th of every month | 3 900 Kč | direct debit |
| after-school club, Kuba | by the 10th of the month | 900 Kč | transfer, payment reference (VS) in Bakaláři |
| ==STK (vehicle inspection) Octavia== | ==by 3 Dec== | 1 350 Kč | booked for 28 Nov |
| compulsory car insurance | 1 Feb | 6 200 Kč | yearly |
| waste fee, 4 people | by 31 May | 4 × 1 200 Kč | Portál občana |
| property tax | by 31 May | 1 870 Kč | payment slip or QR |

> [!tip]- Where to find things
> Contracts, insurance policies and the vehicle registration certificate are scanned in the family Drive in the *Household* folder. Originals in the binder in the living room, second shelf.

## 🏠 Smart home
### Controls
[🌙 Evening](http://homeassistant.local:8123/lovelace/sceny) · [🎬 Movie](http://homeassistant.local:8123/lovelace/sceny) · [🚪 Leaving home](http://homeassistant.local:8123/lovelace/sceny) [?](Turns off all lights, switches off the TV and turns the heating down to 17 °C. Reports if a window was left open.)
[💡 Lights](http://homeassistant.local:8123/lovelace/svetla) · [🌡️ Heating](http://homeassistant.local:8123/lovelace/topeni) · [📷 Front door camera](http://homeassistant.local:8123/lovelace/kamera)

### Availability
- [Internet](https://1.1.1.1){check="tcp://1.1.1.1:53"} · outside connection
- [Modem and Wi-Fi](http://192.168.1.1){check="tcp://192.168.1.1:80"} · router in the hallway
- [Home Assistant](http://192.168.1.10:8123){check="tcp://192.168.1.10:8123"} · hub
- [Zigbee gateway](http://192.168.1.11){check="tcp://192.168.1.11:80"} [?](The window and door sensors go through it. When it is red, the sensors report nothing.)
- [Lights, Hue bridge](http://192.168.1.12){check="tcp://192.168.1.12:443"}
- [Study PC](http://192.168.1.20){check="tcp://192.168.1.20:445"} · shared photos
- [TV](http://192.168.1.30){check="tcp://192.168.1.30:8009"} · living room

<small>The addresses in the demo are made up, a red dot means the device is not on the network. On your board it shows the real status.</small>

### Sensors
| sensor | where | battery |
|:--|:--|:-:|
| door | entrance | 82 % |
| window | bedroom | 64 % |
| window | children's room | ==12 %== |
| water leak | under the washing machine | 91 % |
| smoke | hallway | 77 % |

> [!warning]- Battery in the children's room
> The window sensor in the children's room is at 12 %. Spare CR2032 batteries are in the drawer by the fridge.

##* ⚙️ Automations
| when | what |
|:--|:--|
| window open for more than 10 min | turn off the heating in the room, notify the phone |
| water leak under the washing machine | close the valve, loud notification to both |
| 22:30 on weekdays | turn off the TV and the living room lights |
| nobody home (both phones away) | Leaving home scene |

## 🏫 School, city, authorities
- [Bakaláři](https://www.bakalari.cz){.check} · school system: grades, absence notes, after-school club payments
- [Portál občana](https://obcan.portal.gov.cz){.check} · citizen portal: fees, driving licence points, documents
- [Datová schránka](https://www.mojedatovaschranka.cz){.check} · data box: official mail
- [PID odjezdy](https://pid.cz){.check} · Prague public transport departures: tram to school
- [ČHMÚ výstrahy](https://www.chmi.cz){.check} · weather service warnings: weather, smog, gales

## 📞 Contacts
| who | contact |
|:--|:--|
| paediatrician MUDr. Veselá | [+420 600 400 501](tel:+420600400501) · appointments 7–9 am |
| dentist MUDr. Krejčí | [+420 600 400 502](tel:+420600400502) |
| Ema's class teacher, Mgr. Pokorná | {{email pokorna skola.example}} |
| Grandma Jarka | [+420 600 400 503](tel:+420600400503) |
| plumber Mr Doležal | [+420 600 400 504](tel:+420600400504) · boiler and water |

## 🕓 Who changed what
{{history 6 demo}}

<small>The demo has made-up changes (`demo`). The real history shows who edited the shopping, menu or payments and when, and changes can be reverted.</small>

# Food and neighbourhood
## `Food and neighbourhood`

##* ⭐ Favourite meals
| meal | who likes it most | recipe |
|:--|:--|:--|
| potato pancakes | everyone | Grandma's notebook, p. 12 |
| svíčková | Tomáš | [family cookbook](https://docs.google.com) |
| chicken paprikash | Kuba | [family cookbook](https://docs.google.com) |
| vegetable lasagne | Ema, Petra | [family cookbook](https://docs.google.com) |
| pancakes | kids, Sunday morning | from memory: 2 eggs, ¼ l milk, 8 spoons of flour |

## 🕒 Shops nearby
| | Mon–Fri | Sat | Sun |
|:--|:--|:--|:--|
| Albert, Kobylisy | 6–22 | 6–22 | 7–22 |
| Lidl, Střelničná | 7–22 | 7–22 | 7–21 |
| bakery by the tram stop | 6:30–18 | 7–12 | closed |
| pharmacy by the metro | 8–19 | 8–12 | closed |
| Kobylisy post office | 8–18 | 8–11 | closed |
| recycling centre | 9–18 | 8–15 | closed |

> [!info]- When the big shops are closed
> Under the Czech law on shop opening hours, shops over 200 m² are closed on 1 Jan, Easter Monday, 8 May, 28 Sep, 28 Oct, 25 Dec and 26 Dec. On Christmas Eve only until 12:00. Small shops and pharmacies don't have to follow it.

## 🍲 Cooking inspiration
### TopRecepty
{{rss https://www.toprecepty.cz/rss/ 4}}

### Apetit
{{rss https://www.apetitonline.cz/rss 3}}

##* 🎁 Birthdays and wishes
| who | when | wish |
|:--|:--|:--|
| Ema | 12 Jan | skating course, books about horses |
| Kuba | 3 Apr | Bohemians jersey, building set |
| Grandma Jarka | 28 Feb | trip to Lednice |
| Petra | 9 Jun | ~~new blender~~ (already has one), spa weekend |
