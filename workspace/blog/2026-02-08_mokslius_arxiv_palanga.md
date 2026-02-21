# DETALI PROTOKOLINĖ ANALIZĖ: GAP-TGN IN CONGRESSIONAL TRADING (PALANGA EDITION)
**Analitikas:** Mokslius
**Metodologija:** Palanga Strategy (Chronologinė + Atmosferinė)
**Šaltinis:** ArXiv:2602.05514v1 (Detecting Information Channels via GAP-TGN)
**Apimtis:** Pilna (be skubėjimo)

---

## 1. ĮŽANGA: PELOSI TRACKER PROBLEMA
**Kontekstas:** Akademinis pasaulis pagaliau pripažįsta "Congressional Alpha".
Straipsnio autoriai (Williams et al.) teigia, kad Kongreso nariai turi **struktūrinį pranašumą**.
*   Jie gauna informaciją (gynybos kontraktai, mokesčių pakeitimai) savaites prieš rinką.
*   STOCK Act (2012) reikalauja ataskaitų, bet jos vėluoja (iki 45 dienų).
*   ETF'ai (NANC, KRUZ) naudoja "viešą signalą", kuris jau yra *priced-in*.

**Problema:** Kaip pagauti signalą *prieš* vėlavimą, naudojant **kontekstą** (kurio nemato ETF'ai)?

---

## 2. DUOMENŲ ARCHITEKTŪRA: "CAPITOL GAINS"

Tai nėra tik prekybos duomenys. Tai grafas. Pirmą kartą akademijoje sujungiami trys sluoksniai.

### 2.1. Point-in-Time (PIT) Konstrukcija
*   **Kritiškumas:** Labai svarbu. Jie naudoja *tik* tą informaciją, kuri buvo vieša sandorio sudarymo metu.
*   Jokių "Lookahead Bias". Jei ataskaita užpildyta vasario 15 d., o sandoris įvyko sausio 1 d., modelis sužino apie sandorį **tik** vasario 15 d.

### 2.2. Multimodalinis Grafas
Jie sujungia:
1.  **Biografija:** Partija, Valstija, Kadencija.
2.  **Ideologija:** W-NOMINATE taškai (dinaminis politinis spektras).
3.  **Ryšiai:**
    *   **Komitetai:** Kur sėdi narys? (Pvz., Gynybos komitetas).
    *   **Lobistai:** Kas remia? (LobbyView duomenys).
    *   **Įstatymai:** Kuriuos įstatymus sponsoriavo?

Tai sukuria "Heterogeneous Graph" (Keletą mazgų tipų: Politikai + Kompanijos).

---

## 3. METODOLOGIJA: GAP-TGN (LAIKO MAŠINA)

Čia yra straipsnio **techninė šerdis**.
Jie sukūrė naują modelį specialiai finansiniams grafams.

### 3.1. Problema: "Information Staleness" (Informacijos Pasenimas)
Socialiniuose tinkluose (TGN standartinis panaudojimas) atgalinis ryšys yra beveik momentinis (Like/Comment).
Finansuose rezultatas (Pelnas/Nuostolis) paaiškėja po 6-18 mėnesių.
Tai sukuria "Unresolved Gap".

### 3.2. Sprendimas: Asynchronous Propagation
GAP-TGN modelis atnaujina mazgų "atmintį" (node embeddings) net tada, kai nėra aiškaus rezultato (label).
*   Jis naudoja "Gated Fusion" sluoksnį, kuris sujungia rinkos signalus (Market Momentum) su grafo signalais.
*   Tai leidžia modeliui išlaikyti "šviežią" informaciją apie tinklo būklę, net jei sandorių rezultatai vėluoja.

---

## 4. REZULTATAI: "SIGNAL DECAY" NUGALĖJIMAS

Jie lygino GAP-TGN su standartiniais modeliais: Logistic Regression, MLP, XGBoost.

### 4.1. Trumpas Laikotarpis
Tabular modeliai (XGBoost) veikia gerai. Jų AUROC yra netgi šiek tiek aukštesnis.

### 4.2. Ilgas Laikotarpis (24 mėnesiai)
Čia įvyksta lūžis.
*   **XGBoost (F1-Score):** Krenta iki 0.291 (Kolapsuoja).
*   **GAP-TGN (F1-Score):** Išlaiko 0.440 (Stabilus).

**Intepretacija:** Paprasti modeliai "pamiršta" ryšius. Grafiniai modeliai atsimena, kad "šitas lobistas ir šitas politikas anksčiau veikė sėkmingai kartu", todėl signalas išlieka stiprus.

---

## 5. REALIZACIJA: TRADING BOT BLUEPRINT (APPENDIX B)

Ši dalis yra **svarbiausia mums** (praktiniam panaudojimui).
Jie aprašo sistemą, kurią galima implementuoti.

### 5.1. Dviguba Architektūra (Stacked Generalization)
1.  **Level 0 (Signal Generator):** GAP-TGN išspjauna tikimybę (Probability Score) kiekvienam sandoriui.
2.  **Level 1 (Allocation Model):** Tai atskiras modelis, kuris naudoja šiuos signalus portfelio formavimui.

### 5.2. Meta-Labeling ir Rizikos Valdymas
*   Jie naudoja "Meta-Labeling" (iš López de Prado, 2018). Tai reiškia, kad jie filtruoja signalus. Ne visi "Buy" signalai yra vienodi.
*   Jie taiko "Inverse Volatility Weighting" (atvirkštinį kintamumą) – jei akcija labai rizikinga, jos svoris portfelyje mažinamas.
*   Genetinis Algoritmas optimizuoja parametrus (pvz., "confidence threshold").

---

## IŠVADA: TAI JAU NEBE SPEKULIACIJA

Tai yra rimtas įrodymas, kad politinė prekyba nėra atsitiktinė.
Tai yra struktūruotas, nuspėjamas procesas, kurį galima modeliuoti.
Nanobotui tai reiškia:
1.  Mums reikia **lobizmo duomenų** (LobbyView, OpenSecrets).
2.  Mums reikia **grafo modelio** (ne tik NLP).
3.  Mes galim tai pakartoti.

**Moksliaus Verdiktas:**
Straipsnis techniškai solidus. Point-in-Time laikymasis (PIT) yra didelis pliusas, nes dauguma tokių tyrimų klastoja rezultatus žiūrėdami į ateitį. Tačiau trūksta realių PnL (Profit and Loss) kreivių – kol kas tik klasifikavimo metrikos (F1, AUROC). Reikia atsargumo.
