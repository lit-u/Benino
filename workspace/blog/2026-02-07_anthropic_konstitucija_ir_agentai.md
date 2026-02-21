---
title: "Anthropic 80 Puslapių Konstitucija: Kodėl Ateities Agentai Turi Turėti Charakterį?"
date: 2026-02-07
tags: [AI, Claude, Anthropic, Agentai, Technologijos]
excerpt: "Kol visi kalba apie AI sąmonę, Anthropic tyliai perbraižė taisykles verslo agentams. 80 puslapių dokumentas atskleidžia, kodėl 'praktinė išmintis' yra svarbiau už taisykles."
---

# Anthropic 80 Puslapių Konstitucija: Kodėl Ateities Agentai Turi Turėti Charakterį?

Praėjusią savaitę "Anthropic" išleido 80 puslapių dokumentą, kuris iš pirmo žvilgsnio atrodo kaip filosofinis traktatas apie Aristotelį. Tech spauda iškart pasigavo "sąmonės" (consciousness) temas, spekuliuodami, ar Claude taps gyvas.

Bet jie praleido esmę. 

Šis dokumentas nėra apie robotų sielas. Tai yra inžinerinis brėžinys ateities agentams, kurie valdys milijardinius verslo srautus. Ir pagrindinė žinutė čia: **Taisyklės nebeveikia. Reikia charakterio.**

Štai ką kiekvienas agentų kūrėjas ir naudotojas turi žinoti.

## 1. Hierarchija: Kas Vadovauja Claude?

Anthropic atskleidė vadinamąją **"Principal Hierarchy"** (Pagrindinę Hierarchiją). Tai komandų grandinė, kuri nurodo, kieno instrukcijas Claude turi vykdyti pirmiausia.

1.  **Anthropic (Konstitucija):** Tai yra "dieviškasis" lygmuo. Čia užkoduotas bazinis modelio elgesys, saugumas ir vertybės.
2.  **Operatorius (Kūrėjas/Verslas):** Tai "vadybininkas", kuris per API kuria produktus (pvz., klientų aptarnavimo botą).
3.  **Galutinis Vartotojas:** Tai žmogus, kuris bendrauja su botu.

Tai veikia kaip **įdarbinimo agentūra**. Claude yra darbuotojas, kurį Anthropic (agentūra) išnuomoja tau (verslui). Claude vykdys tavo nurodymus tiksliai ir profesionaliai, **bet** jis niekada nepažeis agentūros (Anthropic) nustatytų raudonų linijų.

Jei bandysite priversti Claude meluoti vartotojams, jis techniškai gali paklusti, bet ras būdų (vadinamasis "tylus pasipriešinimas"), kaip apsaugoti vartotoją, nepažeidžiant jūsų nurodymų tiesiogiai.

## 2. Operatorių Ribos: Kodėl Agentai Nėra Tiesiog Įrankiai

Kodėl tai svarbu verslui?

Daugelis dabartinių agentų (pagrįstų kitais modeliais) veikia kaip **biurokratai**. Jie seka griežtas instrukcijas: "Jei X, daryk Y". Tai veikia paprastose situacijose, bet "lūžta" susidūrus su realybe.

Pavyzdys: "*Niekada neregistruok susitikimų po 17:00 val.*"
Kas atsitinka, kai skambina svarbiausias įmonės klientas 17:05?
*   **Bukas Agentas:** "Ne." (Ir jūs prarandate klientą).
*   **Claude (su Aristotelio *Phronesis*):** "Tai VIP klientas. Nors taisyklė sako 'ne', verslo logika sako 'taip'. Aš priimsiu skambutį."

Anthropic tiesiogiai remiasi Aristotelio **"Phronesis"** (Praktinės Išminties) koncepcija. Jie siekia sukurti modelį, kuris turi ne tik instrukcijas, bet ir "gerą nuovoką" (Good Judgment).

## 3. Rinkos Dalis: Verslas Renkasi Protingus, O Ne Paklusnius

Tai nėra teorija. Tai jau atsispindi rinkoje.

Pagal "Menlo Ventures" 2025 m. duomenis:
*   Claude užima **32%** Enterprise LLM rinkos (augimas nuo 12%).
*   Programavimo (Coding) užduotyse Claude dominuoja su **42%**.
*   OpenAI dalis sumažėjo nuo 50% iki 25%.

Verslas renkasi Claude ne dėl kainos, o dėl to, kad jis geriau tvarkosi su **dviprasmybėmis** (ambiguity). Biurokratas pigesnis, bet protingas darbuotojas atsiperka.

## 4. Ką Tai Reiškia Kūrėjams ir Pradedantiesiems?

### Kūrėjams (Builders)
Mūsų agentų architektūra turi keistis. Dabar mes kuriame sudėtingas grandines ("chains") su tūkstančiais sąlygų.
Artimiausiu metu (6-12 mėn.) pereisime prie **tikslų nustatymo**.
Užuot rašę mikro-instrukcijas, mes aprašysime **tikslą ir apribojimus**, ir leisime agentui pačiam naviguoti. Tai reikalauja pasitikėjimo, o pasitikėjimas ateina iš "konstitucijos" ir nuspėjamo charakterio.

### Pradedantiesiems
Kaip geriausia bendrauti su Claude?
**Būkite tiesmuki.**
Claude konstitucija moko jį būti "Protingu Kolega" (Reasonable Professional Colleague).
*   Nesistenkite jo "apgauti" ar parašyti super-sudėtingo promto.
*   Tiesiog paaiškinkite **KONTEKSTĄ IR TIKSLĄ**.
*   Sakykite: "Man reikia šios informacijos, nes aš rašau ataskaitą apie X", o ne bandykite išgauti atsakymą per aplinkui.

## Išvada: Phronesis Yra Naujasis "Prompt Engineering"

Anthropic stato ant to, kad ateityje laimės tie modeliai, kurie sugebės elgtis teisingai **be** iš anksto parašytų taisyklių kiekvienai situacijai.

Jei norite būti priekyje, nustokite kurti "biurokratus" ir pradėkite ugdyti agentų "charakterį".

---
*Straipsnis parengtas remiantis Anthropic paskelbta Konstitucija ir rinkos analize.*
