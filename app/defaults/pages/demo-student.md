// Demo: Tereza, 3rd-year sociology student at FSV UK, quantitatively oriented. Bachelor's thesis on the online
// participation of young people, plus an international student research project within Erasmus+.
// Lines starting with // are not shown on the page.

#__ About this board
## 🎓 Demo use case: a sociology student
![sociogram: three groups linked by a network of ties](/media/demo-student.svg)

**Tereza** is in her 3rd year of sociology at FSV UK (Faculty of Social Sciences, Charles University) and is writing her bachelor's thesis on the online participation of young people. She can't code and doesn't want to, but every day she works with the university systems, ESS data and a team in four countries. The board is her **desk on a single page**:

- **in the morning** she checks the *This week* band and the dots next to the university systems. She knows about a SIS outage on enrolment day before the faculty e-mail arrives.
- **at a consultation** she writes the notes straight into a note on the page, it saves itself
- **along the way** she uses ✎ to update the exam period, the thesis work plan or the glossary of concepts. These blocks are marked `##*` in the file, so small things don't need the editor.
- **while writing** she copies the dataset citation with one click and has the concept definitions at hand
- **in the evening** she goes through new journal issues in RSS instead of visiting the publishers' websites

##* 📌 This week
> [!tip] Priorities
> 📤 **Sun 15 Nov** systematic literature review (PRISMA) to Moodle, Methodology II
> 💬 **Thu 14:00** YouthVoice consortium meeting: questionnaire harmonisation
> 👩‍🏫 **Fri 10:30** consultation with the supervisor: operationalising the dependent variable

# School
## `School`

## 🏛️ University
- [SIS](https://is.cuni.cz/studium){.check} [?](Study information system: enrolment, exam dates, grades, thesis submission) · studies
- [Moodle](https://dl1.cuni.cz){.check} [?](Syllabi, required reading, submitting seminar papers) · courses
- [University mail](https://outlook.office.com){.check} · Outlook
- [UKAŽ library](https://ukaz.cuni.cz){.check} [?](Union catalogue of Charles University including licensed databases and e-books) · catalogue
- [FSV Ethics Committee](https://fsv.cuni.cz) [?](Application for ethical review of research with human participants) · research

## 📅 Deadlines
- [ ] **15 Nov** systematic literature review, PRISMA diagram (Methodology II)
- [ ] **20 Nov** presentation: integration and transnational ties (Sociology of Migration)
- [ ] **27 Nov** application to the ethics committee
  - [x] informed consent, CZ + EN
  - [ ] data management plan (DMP)
- [ ] **4 Dec** exam registration in SIS
- [x] **8 Nov** essay: the Bourdieusian concept of cultural capital in the digital environment

##* 📝 Exam period
| course | date | format | status |
|:--|:--|:--|:-:|
| Methodology II | 14 Jan | written + project | ⏳ |
| Sociology of Migration | 21 Jan | oral | ⏳ |
| Categorical Data Analysis | 28 Jan | practical in jamovi | ⏳ |
| English C1 | 9 Jan | — | ✓ |

> [!warning]- Registering and deregistering
> SIS → **Exam registration**. You can deregister no later than 24 h in advance, otherwise the attempt is lost. Resit dates are only announced after the regular period ends.

# Thesis
## `Thesis`

##* 🔬 Bachelor's thesis
**Online participation of young adults in Central Europe: the role of political trust and digital skills**
supervisor doc. Jana Nováková {{email jana.novakova example.com}}

| | |
|:--|:--|
| research question | How is institutional trust related to non-electoral online participation among people aged 18–29? |
| data | ESS round 10 (CZ, PL, EE, PT), *N* ≈ 2,400 |
| method | multilevel logistic regression, individuals in 4 countries |
| hypotheses | H1 lower trust → higher online participation · H2 the effect is moderated by digital skills |

- [x] thesis topic approved in SIS
- [ ] theoretical part: connective action, digital inequalities (==60 %==)
- [ ] operationalisation: online participation index from ESS items
- [ ] measurement invariance test across countries
- [ ] pre-registration of the analysis on OSF
- [ ] submission to SIS **by 30 Apr**

### Consultation 7 Nov
{{note}}
- participation index: consider a Mokken scale instead of a simple sum
- control for parents' education, not own (age 18–29)
- only 4 countries: a multilevel model at country level can't carry it, use fixed effects instead
- next time: draft of chapter 3, methodology
{{/note}}

## 📚 Literature and data
### Databases
- [Web of Science](https://www.webofscience.com) · citation analysis, impact
- [Scopus](https://www.scopus.com) · literature search, filters by field
- [SocArXiv](https://osf.io/preprints/socarxiv) · preprints
- [Zotero](https://www.zotero.org) · source library, ČSN ISO 690 style (Czech citation standard) [?](A browser add-on saves an article with its metadata, citations are inserted into Word)

### Data and tools
- [ESS Data Portal](https://ess.sikt.no) · ESS, rounds 1–11
- [CSDA](https://archiv.soc.cas.cz) · Czech surveys, CVVM
- [ISSP](https://issp.org) · international comparison
- [jamovi](https://www.jamovi.org) · regression models without writing code [?](Graphical interface on top of R: linear, logistic and mixed models)
- [OSF](https://osf.io) · pre-registration and data sharing

## ✍️ Dataset citation
When working with ESS data, citing the specific version of the dataset is mandatory (the icon in the top right copies it):

```text
European Social Survey European Research Infrastructure (ESS ERIC). (2023). ESS10 - integrated file, edition 3.2 [Data set]. Sikt - Norwegian Agency for Shared Services in Education and Research. https://doi.org/10.21338/ess10e03_2
```
Weights: for comparing countries `anweight` (analysis weight), never unweighted frequencies.

##* 📖 Glossary of concepts
Connective action
: participation organised through personal networks and shared content, not through formal organisations (Bennett & Segerberg 2012)

Second-level digital inequalities
: differences in skills and ways of use, not in access to the internet itself (Hargittai)

Measurement invariance
: the assumption that a scale measures the same construct in all compared groups; tested with MGCFA

Institutional trust
: trust in parliament, politicians, the legal system and the police (ESS `trstprl`, `trstplt`, `trstlgl`, `trstplc`)

*[ESS]: European Social Survey
*[CSDA]: Czech Social Science Data Archive
*[CVVM]: Public Opinion Research Centre (Czech Academy of Sciences)
*[ISSP]: International Social Survey Programme
*[MGCFA]: multi-group confirmatory factor analysis
*[DMP]: Data Management Plan
*[PRISMA]: reporting standard for systematic reviews
*[SIS]: Study Information System of Charles University

# Erasmus+
## `Erasmus+`

## 🌍 YouthVoice consortium
A comparative student research project on the **online participation of young people** in four countries. A common questionnaire, shared data and a joint report.

| who | institution | time |
|:--|:--|:-:|
| Tereza | UK Prague | UTC+1 |
| Inês | ISCTE Lisbon | UTC+0 |
| Kuba | UJ Kraków | UTC+1 |
| Liis | Tallinn University | UTC+2 |

Meetings are on **Thursdays at 14:00** Prague time (Lisbon 13:00, Tallinn 15:00).

## 🧰 Collaboration
- [Teams](https://teams.microsoft.com) · consortium meetings
- [Shared Drive](https://drive.google.com) · questionnaire, codebook, report
- [Miro](https://miro.com) · map of concepts and research questions
- [World Clock](https://www.timeanddate.com/worldclock/) · the team's time zones
- [DeepL](https://www.deepl.com/translator) · working translation, the final version is checked by a native speaker
- [Erasmus+](https://erasmus-plus.ec.europa.eu) · programme rules

## ✅ For the consortium
- [x] split the chapters of the comparative report
- [ ] back-translation of the Czech version of the questionnaire
- [ ] cognitive interviews on the new items, 5 respondents
- [ ] harmonise education coding according to ISCED 2011
- [ ] confirm the workshop in Lisbon (March)

??? info "Questionnaire harmonisation: checklist"
    same wording and order of items · identical scale (0–10) · translation using TRAPD · pilot in each country · deviations documented in the codebook

*[TRAPD]: Translation, Review, Adjudication, Pretesting, Documentation
*[ISCED]: International Standard Classification of Education

## 📰 New journal issues
### American Sociological Review
{{rss https://journals.sagepub.com/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=asra&type=etoc&feed=rss 3}}

### New Media & Society
{{rss https://journals.sagepub.com/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=nmsa&type=etoc&feed=rss 3}}

### LSE Impact of Social Sciences
{{rss https://blogs.lse.ac.uk/impactofsocialsciences/feed/ 3}}
