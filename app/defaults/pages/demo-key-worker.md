// Demo: Martin, key worker in supported housing (a non-profit organisation).
// He is responsible for three clients. All people, contacts and numbers are made up.
// Lines starting with // are not shown on the page.

#__ About this board
## 🤝 Demo use case: a key worker in a social service
![supported housing with three lit windows and a support network around it](/media/demo-key-worker.svg)

**Martin** works as a key worker in supported housing and is responsible for three clients. For each of them he needs to have at hand the contacts for the family and guardian, doctors, authorities, the individual plan and documents. He used to search for them in three binders and five folders on the Drive. Now this board is open on the service's shared computer:

- **at the start of a shift** he reads the *Shift handover* from his colleague and checks *Today*. He edits the day's schedule and the handover right on the page with ✎, the blocks are marked `##*` in the file.
- **with a client** he opens their card: whom to call, what medication and check-ups they have, what is in the individual plan and where the documents are on the Drive
- **crisis information** (allergies, what to do during a seizure) is in a prominent box, so that even a stand-in who doesn't know the client can find it
- **clients' wishes** are collected in one table. Before birthdays or Christmas he then knows what would make whom happy.
- **legislation and standards** are in footnotes, just hover over the number

> [!danger] Sensitive data
> Health and legal information about clients is specially protected personal data. Run a board containing it only on the service's internal network and put the whole site behind a login (reverse proxy). In links to the Drive keep only folder names, the documents themselves stay behind the organisation's access control. In this demo all people are made up.

# Service
## `Service`

##* 🗓️ Today, Thu 12 Nov
| time | who | what |
|:--|:--|:--|
| 8:30 | Petr | escort to neurology, card + medication list |
| 10:00 | Lenka | pottery workshop, pick up at 12:00 |
| 13:30 | Jiří | speech therapy (comes to the home) |
| 15:00 | team | meeting, review of Petr's IP |

##* 📋 Shift handover
Lenka didn't sleep at night, calm in the morning. Offer her a rest after the workshop.
Jiří ran out of incontinence pads, ordered, delivery on Friday.
Petr got a letter from the ÚP (PnP review), it's in the *Authorities* folder.

## 📞 Service contacts
| | |
|:--|:--|
| head of service | Hana Kubíčková · [+420 600 100 200](tel:+420600100200) |
| nurse | Eva Malá · [+420 600 100 201](tel:+420600100201) |
| night shift | [+420 600 100 299](tel:+420600100299) |
| ambulance | [155](tel:155) · emergency line [112](tel:112) |
| crisis line | [116 123](tel:116123) Psychological first aid line |

## 🧭 Systems
- [Cygnus](https://www.iscygnus.cz) [?](The service's information system: records of service delivery, individual plans, medication) · records
- [Service Google Drive](https://drive.google.com) · client folders
- [Shift rota](https://docs.google.com/spreadsheets) · team spreadsheet
- [Register of providers](https://iregistr.mpsv.cz) · service registration details
- [MPSV](https://www.mpsv.cz) · care allowance, social services

/

##* 🎁 Clients' wishes
| who | wish | occasion | status |
|:--|:--|:--|:-:|
| Petr | radio with big buttons | birthday 3 Feb | 💡 |
| Petr | Bohemians match, Ďolíček | spring | 🎟️ |
| Lenka | noise-cancelling headphones | Christmas | 🛒 |
| Jiří | video call with his son every Sunday | ongoing | ✓ |

## ✅ This week
- [ ] review of Petr's individual plan (meeting Thu)
- [ ] send the PnP review form, Petr, by 20 Nov
- [ ] order a voucher for a new wheelchair for Jiří (GP)
- [x] arrange a weekend visit with Lenka's mother

*[IP]: individual plan
*[PnP]: care allowance (příspěvek na péči)
*[ÚP]: Labour Office of the Czech Republic (Úřad práce ČR)
*[MPSV]: Ministry of Labour and Social Affairs

#++ Clients
## `Clients`

## 👤 Petr N., 54
moderate intellectual disability, epilepsy · in the housing since 2019

!!! danger "Epileptic seizure"
    Move him to safety, put nothing in his mouth, time it. **Seizure longer than 5 minutes or repeated → call 155.** The ambulance crew can give medication according to his card, which is in his room in the blue folder.

Strong relationships (sister, friend, workshop) support the goals of the individual plan. The current source of stress is the care allowance review; when dealing with the ÚP, Petr wants his sister with him.

### Contacts
| who | relationship | contact |
|:--|:--|:--|
| Jana N. | sister, **guardian**[^opatrovnik] | [+420 600 200 301](tel:+420600200301) · {{email jana.n example.cz}} |
| Tomáš | friend from the sheltered workshop | via the workshop, Tue and Thu |
| MUDr. Svoboda | GP | [+420 600 200 302](tel:+420600200302) |
| MUDr. Králová | neurology, FN Motol (Motol University Hospital) | ~~19 Nov~~ moved to **3 Dec** |

### Individual plan[^ip]
- [x] walks to the bakery round the corner on his own and pays
- [ ] tram ride to the workshop, accompanied for now (goal: on his own by June)
- [ ] own pocket money: a weekly envelope, record spending together

### Authorities and documents
- care allowance[^pnp] **level III**, ÚP review in progress
- disability pension, level III (ČSSZ)
- [📁 Petr: individual plan](https://drive.google.com) · [📁 health](https://drive.google.com) · [📁 authorities and court](https://drive.google.com)

/

## 👤 Lenka K., 31
autism spectrum disorder, non-speaking, communicates with pictograms and a tablet · in the housing since 2022

!!! warning "Allergy: penicillin"
    Report at every treatment. Noted on her health insurance card and in Cygnus.

??? tip "How to communicate with Lenka"
    Speak briefly and calmly, one thing at a time. Show changes to the programme in advance on the daily schedule with pictograms. Noise and touch without warning increase tension, she has headphones in her backpack. She shows yes/no on the tablet or by nodding.

### Contacts
| who | relationship | contact |
|:--|:--|:--|
| Marie K. | mother, **guardian** | [+420 600 300 401](tel:+420600300401) · weekends with family |
| Pavel K. | father | [+420 600 300 402](tel:+420600300402) |
| MUDr. Dvořák | psychiatrist | check-up every 3 months, next **14 Jan** |
| Pottery workshop | daytime activity | Mon, Wed, Thu 10–12 |

### Individual plan[^ip]
- [x] choose clothes for the weather on her own (pictograms by the wardrobe)
- [ ] switch to the new tablet: transfer the communication set, practise
- [ ] try a second workshop (garden) once a week

### Documents
[📁 Lenka: IP and communication set](https://drive.google.com) · [📁 health](https://drive.google.com) · [📁 authorities](https://drive.google.com)

/

## 👤 Jiří V., 67
after a stroke, uses a wheelchair, mild aphasia · full legal capacity · in the housing since 2024

### Contacts
| who | relationship | contact |
|:--|:--|:--|
| Ondřej V. | son, **supporter**[^podpurce], lives in Munich | [+49 160 0000 000](tel:+491600000000) · Sunday 18:00 video call |
| Nusle Seniors' Club | friends | Tue afternoon |
| Mgr. Horká | speech therapy | Thu 13:30 at home |
| Physiotherapy | rehabilitation | Mon and Wed, Nusle outpatient clinic |

### Individual plan[^ip]
- [x] video calls with his son: tablet, shortcut set up on the home screen
- [ ] resume visits to the seniors' club (transport: social taxi)
- [ ] practise transfer from wheelchair to bed with one person

### Authorities and documents
- care allowance[^pnp] **level IV**, ZTP/P card
- new manual wheelchair: voucher from the GP → health insurer
- [📁 Jiří: IP](https://drive.google.com) · [📁 health and aids](https://drive.google.com)

[^opatrovnik]: A guardian is appointed by the court, the extent of the restriction of legal capacity is set out in the judgment (folder *authorities and court*).
[^ip]: Individual planning of service delivery, social services quality standard no. 5 (annex 2 of Decree No. 505/2006 Coll.).
[^pnp]: Care allowance under Act No. 108/2006 Coll., on Social Services; the Labour Office decides on granting and reviewing it.
[^podpurce]: Supported decision-making agreement (§ 45 ff. of the Civil Code): the person decides on their own, the supporter helps them.

*[IP]: individual plan
*[PnP]: care allowance (příspěvek na péči)
*[ÚP]: Labour Office of the Czech Republic (Úřad práce ČR)
*[ČSSZ]: Czech Social Security Administration
*[ZTP/P]: card for a person with a severe disability who needs a companion
*[MPSV]: Ministry of Labour and Social Affairs
