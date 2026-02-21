---
tags:
  - AI_Governance
  - Congressional_Trading
  - Graph_Networks
  - Palanga_Edition
  - OldBoy_Extracts
date: 2026-02-08
author: OldBoy Alchemist
source: https://arxiv.org/abs/2602.05514
paper_title: Detecting Information Channels in Congressional Trading via Temporal Graph Learning
authors: Benjamin Pham Roodman, Eugene Sy, J. Xavier Atero Vázquez, Yu-Shiang Huang, Che Lin, Chaun-Ju Wang
submitted: 2026-02-05
---

![Congressional Trading](https://images.unsplash.com/photo-1541872703-74c5e44368f9?q=80&w=2670&auto=format&fit=crop)

# Kai AI Seka Kongreso Ranką: Grafų Tinklai Prieš Insider Trading

Sėdžiu Palangoje, pušys kvepia, jūra ošia. Turiu laiko. Šiandien analizuosiu kažką, kas būtų atrodę kaip mokslinė fantastika prieš dešimtmetį, bet dabar – tiesiog akademinis paper'is arXiv'e. Šeši mokslininkai sukūrė sistemą, kuri stebi JAV Kongreso narius ir bando atsakyti į klausimą, kurį žmonės uždavinėja jau dešimtmečius: **ar jie naudoja privilegijuotą informaciją akcijoms pirkti?**

## Įžanga: Kai Tie, Kurie Kuria Taisykles, Žaidžia Ne Pagal Jas

2012-aisiais JAV priėmė įstatymą su puikiu pavadinimu: **STOCK Act** (Stop Trading on Congressional Knowledge). Esmė paprasta – Kongreso nariai privalo deklaruoti, kokias akcijas perka ir parduoda. Skaidrumas. Accountability. Demokratija.

Bet viena yra deklaruoti, kita – kontroliuoti. Ir čia prasideda įdomi istorija.

Įsivaizduok: tu esi senatorius. Rytoj svarstomas įstatymas, kuris gali pakeisti visos pramonės šakos likimą. Tu žinai, kas bus. Ir tu taip pat žinai, kad gali nusipirkti akcijų. Techniškai – legalu (jei deklaruoji). Etiškai? Na, čia jau sudėtingiau.

**Problema nėra nauja.** Bet sprendimo būdas – visiškai naujas.

## Grafai Kaip Tinklas: Ne Socialinis, O Korupcijos

Paper'is, kurį skaitau, neatsitiktinai vadinasi "Detecting Information Channels" – **informacijos kanalai**. Nes problema ne tiesiog tame, kad politikas nusiperka akcijų. Problema – kaip jis sužinojo, kad verta pirkti.

Ir čia mokslininkai naudoja ginklą, kuris pastaruosius metus tampa vis galingesnis – **temporal graph networks**. Grafų tinklai laike.

### Kas Yra Grafas?

Paprasta analogija: **miesto žemėlapis.** Taškai – pastatai. Linijos – gatvės. Grafas – tai abstrakti struktūra, kur svarbu ne taškai patys, o **ryšiai tarp jų**.

Šiame paper'yje:
- **Taškai (nodes):** Kongreso nariai ir korporacijos
- **Linijos (edges):** Ryšiai tarp jų

Bet ne bet kokie ryšiai. Keturių tipų:

1. **Trading edges** – Politikas perka/parduoda kompanijos akcijas
2. **Lobbying edges** – Kompanija lobina politiką (oficialiai registruota)
3. **Campaign finance edges** – Kompanijos PAC (Political Action Committee) duoda pinigų kampanijai
4. **Geographic edges** – Politiko rajonas/valstija sutampa su kompanijos buveine

> "Šis grafas nėra statinis. Jis gyvas. Jis keičiasi laike. Ir būtent **temporal** dalis daro jį tokį galingą."

## Kodėl Laikas Čia Svarbu?

Įsivaizduok tokią seką:

**2020 sausis:** Kompanija X pradeda lobistinę kampaniją Senate komitete.

**2020 vasaris:** Tas pats komitetas svarsto įstatymą, susijusį su X sritimi.

**2020 kovas:** Senatorius, kuris sėdi tame komitete, nusiperka X kompanijos akcijų.

**2020 balandis:** Įstatymas priimamas. X akcijos kyla +30%.

Kiekvienas šių įvykių atskirai – normalus. Bet **seka laike** – tai jau pattern. Ir būtent tokius patterns temporal graph network'ai sugeba pastebėti.

## Walk-Forward: Kaip Nežiūrėti Į Ateitį

Viena iš elegantesnių dalių šio paper'io – **walk-forward validation**. Skamba techniškai, bet esmė paprasta: **neapgaudinėk savęs**.

Kai treniruoji AI modelį su istoriniais duomenimis, labai lengva sukurti "orakulą", kuris "nuspėja" praeitį. Bet tai ne nuspėjimas – tai atsiminimas.

Walk-forward yra disciplina:

1. **Trainink** tik su duomenimis iki datos T
2. **Testuok** tik su duomenimis po datos T
3. Pakartok visą ciklą, slankiodamas per laiką

Pavyzdys:
- **Training:** 2015-2020
- **Testing:** 2021-2022

Ir niekada neleidžiama modeliui "pažiūrėti į ateitį". Nes realybėje – jos nematysi.

> "Tai nėra apie tai, ar modelis good ar bad. Tai apie tai, ar jis honest."

## Kaip Apibrėžti "Įtartiną" Trade'ą?

Čia prasideda filosofija. Kaip nuspręsti, kad trade'as yra anomalus? Ar tiesiog sėkmingas?

Paper'is naudoja **risk-adjusted returns** – grąžą, adjusted'intą pagal riziką. Konkretus instrumentas – **Sharpe Ratio**.

Formulė paprasta:
```
Sharpe = (Grąža - Risk-Free Rate) / Volatility
```

Esmė: tu negali tiesiog sakyti "šis trade'as uždirbо daug". Nes galbūt visa rinka augo. Arba galbūt politikas rizikavo viskuo.

Sharpe ratio pataiso both. Ir paper'is lygina su **S&P 500** – rinkos benchmark'u.

**Label'as (žyma):**
- **1** – Trade outperformed S&P 500 (statistiškai reikšmingai)
- **0** – Normal arba underperformed

Ir TGN modelis bando nuspėti: ar šis trade'as, atsižvelgiant į visą context'ą (lobbying, donations, geografiją), bus "1".

## Multi-Modal: Kai Vieno Duomenų Šaltinio Nepakanka

Didžioji šio paper'io stiprybė – **multi-modal data integration**. Tai fancy būdas pasakyti: "jie sujungė daug skirtingų duomenų tipų".

Bet kodėl tai svarbu?

Įsivaizduok, kad žiūri tik į trade'us. Matai: senatorius pirko akcijas, ir jos pakilo. Suspicious? Galbūt. Bet galbūt jis tiesiog skaito Bloomberg'ą kaip visi.

Dabar pridedi **lobbying data**. Matai: tą pačią savaitę ta kompanija lobino tą senatorių. Dabar – įdomiau.

Pridedi **campaign finance**. Matai: ta kompanija prieš 3 mėnesius davė $50,000 senatorių kampanijai. Dabar – really interesting.

Pridedi **geografiją**. Matai: kompanijos HQ yra senatoriaus valstijoje. Dabar pattern'as ryškus.

> "Vienas duomenų taškas – coincidence. Du – pattern. Trys – evidence. Keturi – tam tikra istorija."

## Šešėliai: Kas Lieka Už Kadro

Bet kiekviena sistema turi **blind spots**. Ir paper'is juos pripažįsta (kas geras ženklas).

### 1. Disclosure Delays

STOCK Act leidžia **45 dienų langą** deklaravimui. Tai reiškia: iki tu pamatai trade'ą, jis jau seniai įvykęs. Rinkos jau sureagavusios. Informacija – stale.

Real-time detection neįmanomas. Tik retrospective analysis.

### 2. Broad Ranges

Kai kurios deklaracijos parodo ne tikslią sumą, o range'ą: $1k-$15k, $15k-$50k, $50k-$100k, etc.

Skirtumas tarp $1,000 ir $15,000 trade'o – **15x**. Bet modelis gauna vieną range'ą. Precision loss.

### 3. Blind Trusts

Kai kurie politikai naudoja **blind trusts** – jų investicijas valdo third party, ir jie "officially" nežino, ką perka. Tie trade'ai ne deklaruojami.

Ar tai loophole? Teoriškai – ne, nes politikas tikrai nežino. Praktiškai? Na, trust'o valdytojas tikrai kažką žino. Ir tas kažkas gali kalbėtis su politiku "atsitiktinai".

### 4. Causality Problem

Didžiausia filosofinė problema: **correlation ≠ causation**.

Modelis mato pattern'ą. Lobina → Trade → Profit. Bet tai nereiškia, kad lobinas **caused** profit. Galbūt:
- Visa pramonė augo (tame sektoriuje)
- Viešai žinoma informacija (news)
- Coincidence (atsitiktinumas)

Paper'is neįrodo insider trading. Jis tiesiog **flags statistically unusual patterns**. Investigation – žmonių darbas.

## Etika: Ar Tai Orwellian Surveillance?

Čia prasideda interesting ethical terrain.

Viena pusė: **Transparency good**. Kongreso nariai – public servants. Jų finansiniai sprendimai turėtų būti scrutinized. AI padeda tai daryti efektyviau.

Kita pusė: **False positives**. Modelis gali flag'inti legitimius trade'us. Ir tada politikas užtraukia suspicion be pagrindo. Reputacijos žala – reali.

Trečia pusė: **Adversarial gaming**. Jei politikai žino, kaip modelis veikia, jie gali strukturuoti trade'us taip, kad išvengtų detection. Arms race.

> "Transparency įrankis gali tapti surveillance weapon. Klausimas – kas valdo tą įrankį ir kokiomis taisyklėmis."

## Kas Toliau? Ar Tai Bus Deploy'inta?

Paper'is – academic. Bet idėja – labai practical.

**Scenarijus 1: Watchdog NGOs**

Organizations kaip Campaign Legal Center arba Common Cause galėtų naudoti tokią sistemą. Run continuously. Flag anomalies. Publish reports.

Public pressure – galingas dalykas.

**Scenarijus 2: Congressional Ethics Committees**

Pačios institucijos galėtų deploy'inti intern. Automatinis screening prieš investigations. Reduce manual workload.

Bet čia kyla klausimas: ar jie nori? Oversight save patį?

**Scenarijus 3: Media**

Investigative journalism. Turi dataset'us. Turi techninius resources (bent didieji). Run analysis. Write stories.

Bloomberg, NYT, WSJ – visi turi tech teams dabar.

## Kodėl Šis Paper Svarbus Platesniame Kontekste?

Ne tik dėl Congressional trading. Bet dėl to, ką jis reprezentuoja: **AI for oversight**.

Mes daug kalbame apie AI kuriančius naują content'ą, generuojančius tekstą, images, videos. Bet yra ir kita pusė: **AI kaip detector**.

- Fraud detection bankuose
- Money laundering networks
- Conflict of interest academia
- Corporate insider trading

Temporal graph networks – universal tool. Ir šis paper'is parodo, kad jis works ne tik teorijoje.

> "Kiekviena institucija turi informacijos kanalus. Kai kurie – legitimi. Kai kurie – ne. AI uždavinys – ne spręsti, kuris kuris, bet parodyti, kur tie kanalai yra."

## Palangos Refleksija: Kontrolė Be Trust'o

Sėdžiu čia, jūra ošia, ir galvoju – kas įdomu. Ne tai, kad politikai gali būti korumpuoti. Tai sena žinia. Bet tai, kad **technologija leidžia kontroliuoti be trust'o**.

Anksčiau – tu turėdavai pasitikėti institucijomis. Kad jos pačios save kontroliuoja. Ethics committees. Internal audits. Self-regulation.

Dabar – tu gali **verificuoti**. Publicly available data. Open algorithms. Reproducible results.

Tai ne utopija. False positives bus. Adversarial evasion bus. Bet **kryptis aiški** – nuo trust-based į verification-based systems.

Ir tai taikoma ne tik Congressional trading. Tai taikoma:
- Corporate governance
- Academic integrity
- Medical research
- Climate pledges

**Kiekviena sritis, kur buvo "trust me, I'm ethical" – dabar gali būti "here's the data, verify yourself".**

Ar tai geriau? Priklauso nuo execution. Bet **direction of travel** neabejotinas.

## Išvados: Grafai Kaip Skaidrumo Įrankis

Šis paper'is nėra sensacija. Jis netaps headline'u mainstream media. Bet jis yra **building block**.

**Ką jis parodo:**
1. Multi-modal temporal graphs veikia complex oversight problemoms
2. Walk-forward validation eliminuoja look-ahead bias
3. Risk-adjusted metrics suteikia fair labeling
4. Publicly available data pakanka meaningful detection'ui

**Ką jis neparodо:**
1. Causation (correlation ≠ cause)
2. Real-time deployment (disclosure delays)
3. Adversarial robustness (gaming strategies)
4. Legal admissibility (statistical pattern ≠ evidence)

Bet tai – pradžia.

Ir kaip su bet kuo Palangoje – **reikia laiko**. Laiko, kad technologija pribręstų. Laiko, kad institucijos adapt'intųsi. Laiko, kad visuomenė suprastų, ko ji nori.

Ar Congressional trading sustabdomas? Abejoju. Bet ar jis taps matomas? Taip. Ir kartais visibility – pirmasis žingsnis.

---

**OldBoy užbaiga:**

Pušys kvepia. Jūra ošia. AI systems stebi Kongresą. Gražus metas būti gyvu – kai technologija leidžia matyti, kas anksčiau buvo paslėpta.

Bet atmink: **matyti ≠ suprasti**. Ir suprati ≠ veikti. Grafų tinklai parodo patterns. Žmonės turi nuspręsti, ką su jais daryti.

Ir tai – labai žmogiška problema. Kuria AI neišspręs.

🤞
