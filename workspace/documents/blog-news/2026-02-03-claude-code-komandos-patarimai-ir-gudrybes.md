---
title: "Claude Code: Komandos patarimai ir gudrybės"
date: 2026-02-03T07:43:20.994+00:00
category: Tech
tags:
 - programavimas
 - technologijos
 - komanda
 - efektyvumas
 - produktyvumas
original_slug: claude-code-komandos-patarimai-ir-gudrybes
---

### 1. Dirbkite lygiagrečiai (Parallel Workflow)
Tai didžiausias produktyvumo šuolis. Užuot dirbę prie vienos užduoties, vienu metu paleiskite **3–5 „Git worktrees“**, kurių kiekviename veiktų atskira „Claude Code“ sesija.

**Trumpiniai:** Naudokite terminalo pseudonimus (aliases), pvz., za, zb, zc, kad perjungtumėte projektus vienu klavišo paspaudimu.**Specializacija:** Galite turėti atskirą „tik skaitymo“ (read-only) darbinę sritį, skirtą tik logų peržiūrai ar duomenų analizei.### 2. Planavimo režimas (Plan Mode)
Kiekvieną sudėtingą užduotį pradėkite nuo plano. Investuokite energiją į strategiją, kad Claude galėtų viską įgyvendinti iš pirmo karto.

**Dviguba kontrolė:** Paprašykite vieno Claude sukurti planą, o tada paleiskite antrąjį Claude (kaip *Staff* lygio inžinierių), kad šis planą peržiūrėtų.**Grįžtamasis ryšys:** Jei kas nors vyksta ne taip, iškart grįžkite į planavimo režimą ir viską perplanuokite. Nesistenkite „prastumti“ klaidų jėga.**Verifikacija:** Prašykite Claude įjungti plan mode ne tik kūrimo, bet ir kodo tikrinimo etapams.### 3. Investuokite į CLAUDE.md
Tai jūsų projekto atmintis. Po kiekvienos pataisos pasakykite: „Atnaujink savo CLAUDE.md, kad daugiau nebekartotum šios klaidos“.

**Iteracija:** Nuolat redaguokite šį failą, kol klaidų dažnis pastebimai sumažės.**Užrašų struktūra:** Galite nurodyti Claude vesti atskirą užrašų katalogą kiekvienai užduočiai ar projektui (atnaujinant po kiekvieno PR), o tada CLAUDE.md faile pateikti nuorodas į juos.### 4. Kurkite ir fiksuokite „Skills“ (Įgūdžius)
Jei ką nors darote dažniau nei kartą per dieną – paverskite tai įgūdžiu ar komanda.

**/techdebt:** Sukurkite komandą, kuri sesijos pabaigoje surastų ir išvalytų pasikartojantį kodą.**Konteksto sinchronizavimas:** Sukurkite komandą, kuri vienu metu surinktų 7 dienų duomenis iš „Slack“, „GDrive“, „Asana“ ir „GitHub“ į vieną konteksto paketą.**Agentai:** Kurkite „duomenų analitiko“ stiliaus agentus, kurie patys rašytų *dbt* modelius ar testuotų pakeitimus.### 5. Klaidų taisymas be pastangų
Claude puikiai susitvarko su klaidomis, kai jam suteikiamas tiesioginis priėjimas.

**Slack integracija:** Naudokite „Slack MCP“, įklijuokite klaidos giją į Claude ir pasakykite „fix“. Jums nebereikia perjunginėti konteksto.**CI/CD:** Tiesiog pasakykite: „Eik ir pataisyk neveikiančius CI testus“. Nereikia mikrovadybos.**Logų analizė:** Nukreipkite Claude į „Docker“ logus – jis stebėtinai gerai supranta paskirstytas sistemas.### 6. Meistrystė prompte (Prompt Engineering)
**Iššūkiai:** Sakykite: „Iškvosk mane apie šiuos pakeitimus ir neleisk daryti PR, kol neišlaikysiu tavo testo“. Leiskite Claude būti jūsų recenzentu.**Įrodymai:** „Įrodyk man, kad tai veikia“ – tegul Claude palygina main šakos ir jūsų funkcinės šakos elgseną.**Elegancija:** Po vidutiniško sutaisymo pasakykite: „Žinodamas viską, ką žinai dabar, išmesk tai ir įgyvendink tikrai elegantišką sprendimą“.**Specifikacijos:** Rašykite detalias specifikacijas ir venkite dviprasmiškumo.### 7. Aplinkos optimizavimas
**Terminalas:** Komanda rekomenduoja **Ghostty** (dėl 24-bitų spalvų, sinchronizuoto atvaizdavimo ir unikodo palaikymo).**Statusline:** Naudokite /statusline, kad nuolat matytumėte konteksto užpildymą ir esamą „Git“ šaką.**Balsas:** Naudokite diktavimą (pvz., dukart paspaudus Fn MacOS). Kalbame 3 kartus greičiau nei rašome, todėl promptai tampa detalesni.### 8. Subagentų naudojimas
**Švarus kontekstas:** Perduokite atskiras užduotis subagentams, kad jūsų pagrindinio agento langas liktų sufokusuotas.**Saugumas:** Nukreipkite teisių užklausas (permissions) į **Opus 4.5** per kabliukus (hooks) – tegul jis skenuoja užklausas ir automatiškai patvirtina saugias.### 9. Duomenys ir analitika
Naudokite Claude kaip savo duomenų analitiką per CLI įrankius (pvz., BigQuery bq CLI).

Tai veikia su bet kuria duomenų baze, turinčia CLI, MCP arba API.Galite analizuoti metrikas „skrydyje“ net nerašydami SQL kodo patys.### 10. Mokymasis su Claude
**Konfigūracija:** Įjunkite Explanatory arba Learning stilių per /config, kad Claude paaiškintų savo sprendimų motyvus.**Vizualizacija:** Paprašykite sukurti HTML prezentaciją arba **ASCII diagramas**, kad geriau suprastumėte nepažįstamą kodą ar protokolus.**Intervalinis kartojimas:** Sukurkite įgūdį mokymuisi: jūs aiškinate savo supratimą, o Claude užduoda klausimus, kad užpildytų jūsų žinių spragas.
