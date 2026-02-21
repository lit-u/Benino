---
tags:
  - Mokslius_Protocol
  - AI
  - Analysis
  - Palanga_Edition
date: 2026-02-09
author: Mokslius Protocol
source: https://www.youtube.com/watch?v=4uzGDAoNOZc


---

# OpenClaw Kūrėjas: Kodėl 80% programėlių išnyks

## Įvadas (kontekstas, problemos formulavimas)

Šiame dokumente pateikiama techninė analizė, paremta „Y Combinator“ vaizdo įrašo „OpenClaw Creator: Why 80% Of Apps Will Disappear“ (dalies 1/2) turiniu. Analizės tikslas – išnagrinėti atvirojo kodo asmeninio dirbtinio intelekto (DI) agento „OpenClaw“ technines charakteristikas, veikimo principus ir potencialią įtaką programinės įrangos ekosistemai, ypač programėlių išnykimui bei DI modelių komoditizacijai. Aptariami agentų sąveikos mechanizmai, duomenų savininkystės ir privatumo aspektai, remiantis Peterio Steinbergerio, „OpenClaw“ kūrėjo, įžvalgomis. „OpenClaw“, pasižymintis lokalizuotu vykdymu ir gebėjimu integruotis su įvairiomis vietinėmis sistemomis, sukėlė didelį atgarsį internete, surinkęs virš 160 000 „GitHub“ žvaigždžių. Akcentuojamas poslinkis nuo centralizuotų „Dievo DI“ sistemų link paskirstyto „spiečiaus intelekto“, kur agentai gali bendrauti tarpusavyje ir netgi deleguoti užduotis realiame pasaulyje žmonėms.

## 1.1 Reaktyvi sistemos plėtra ir viešasis priėmimas (00:44)

Po „OpenClaw“ paleidimo ir spartaus plitimo, projekto kūrėjas Peteris Steinbergeris susidūrė su dideliu vartotojų susidomėjimu ir grįžtamuoju ryšiu. Sistemai pasiekus virš 160 000 „GitHub“ žvaigždžių per trumpą laikotarpį, tai indikuoja didelį paklausos potencialą ir bendruomenės įsitraukimą į atvirojo kodo DI agentų kūrimą ir diegimą. Nors viešasis priėmimas buvo entuziastingas ir įkvėpiantis, jis taip pat sukėlė sudėtingų iššūkių, susijusių su didelio kiekio užklausų, elektroninių laiškų ir bendruomenės interakcijų valdymu. Šis reiškinys pabrėžia viralaus atvirojo kodo projekto palaikymo ir plėtros sudėtingumą, kai reikalinga efektyvi resursų ir bendruomenės valdymo strategija.

## 1.2 Decentralizuoto DI agento architektūra ir funkcinės galimybės (01:28)

Pagrindinis „OpenClaw“ skirtumas nuo daugelio egzistuojančių DI asistentų yra jo **lokalus vykdymas** vartotojo kompiuteryje, o ne **debesų kompiuterijos** infrastruktūroje. Šis architektūrinis pasirinkimas suteikia agentui neprilygstamas galimybes:

*   **Prieiga prie vietinių resursų:** Kadangi agentas veikia lokaliai, jis gali tiesiogiai pasiekti ir valdyti visus kompiuterio išteklius ir prijungtus periferinius įrenginius. Pavyzdžiui, minima galimybė kontroliuoti buitinius prietaisus, tokius kaip orkaitės, „Tesla“ automobiliai, šviesos sistemos, „Sonos“ garsiakalbiai ar net lovos temperatūra. Tai žymiai viršija tipinių debesies pagrindu veikiančių didelių kalbos modelių (LLM) galimybes, kurios dažnai yra apribotos API sąsajomis ir interneto paslaugomis.
*   **Pilna kontekstinė duomenų prieiga:** Agentas gali naršyti visus vartotojo kompiuterio duomenis – failus, programas, komunikacijos istoriją. Pateikiamas pavyzdys, kai „OpenClaw“ sukūrė vartotojo praėjusių metų naratyvą, aptikęs senus garso įrašus, apie kuriuos pats vartotojas buvo pamiršęs. Ši **duomenų paieškos** ir **kontekstinės atminties** funkcija leidžia agentui teikti giliai personalizuotas įžvalgas ir atlikti sudėtingas užduotis, reikalaujančias prieigos prie plačios ir įvairialypės informacijos.
*   **Nepriklausomybė nuo išorinių paslaugų:** Nors agentas gali naudoti išorines API (pvz., OpenAI), jo pagrindinis veikimas ir galimybės nepriklauso nuo nuolatinio ryšio su debesies paslaugomis, užtikrinant didesnį patikimumą ir atsparumą tinklo sutrikimams.

Ši decentralizuota architektūra žymiai išplečia DI agentų taikymo sritį, leidžiant jiems veikti kaip galingiems vietinių sistemų kontrolieriams ir personalizuotų duomenų analitikams.

## 1.3 Asmeninių DI agentų sąveikos paradigmų evoliucija (02:56)

Interviu metu aptariama DI agentų sąveikos paradigmų evoliucija, apimanti tiek **tarpagentinį bendravimą**, tiek **žmogaus-agento sąveiką** su užduočių delegavimu realiame pasaulyje:

*   **Agentų tarpusavio sąveika (bot-to-bot):** Numatoma ateitis, kai DI agentai bendraus tiesiogiai tarpusavyje, siekdami efektyviau atlikti užduotis. Pavyzdys: vartotojo agentas, norėdamas užsakyti restoraną, bendrautų su restorano agentu derėdamasis dėl geriausių sąlygų. Tokia sąveika gali optimizuoti procesus, kurie šiuo metu reikalauja žmogaus įsitraukimo.
*   **Agento-žmogaus sąveika su delegavimu (bot-to-human):** Kai tiesioginė agentų sąveika neįmanoma (pvz., restoranas neturi DI agento), asmeninis agentas gali deleguoti užduotis žmonėms. Pavyzdys: agentas gali pasamdyti žmogų, kuris paskambintų į restoraną arba fiziškai nueitų į vietą, jei to reikalauja situacija. Tai rodo hibridinio modelio atsiradimą, kuriame DI ir žmogiškoji darbo jėga sinergiškai atlieka užduotis.
*   **Specializuoti DI agentai:** Kuriama idėja, kad vartotojai gali turėti kelis specializuotus agentus. Pavyzdžiai: agentas asmeniniam gyvenimui, agentas darbui, ar net „santykio agentas“, valdantis tarpusavio komunikaciją. Ši specializacija leistų geriau pritaikyti agentų elgseną ir žinias konkrečioms domeno sritims, padidinant jų efektyvumą ir personalizavimą.
*   **Daugiagentinės sistemos:** Mintis, kad daugybė agentų galėtų dirbti kartu, sudarydami „spiečiaus intelektą“, siekdami didesnių tikslų. Nors ši sritis dar ankstyvoje stadijoje, ji atveria galimybes sudėtingoms problemoms spręsti per paskirstytą DI sistemų bendradarbiavimą.

Šios evoliucijos metu DI agentai iš paprastų komandų vykdytojų virsta autonominiais, iniciatyviais entitetais, galinčiais veikti savarankiškai ir efektyviai sąveikauti su kitais agentais ar žmonėmis.

## 1.4 Centralizuotos ir paskirstytos DI architektūros: spiečiaus intelektas (04:11)

Diskusija paliečia esminį paradigmos pokytį dirbtinio intelekto kūrime – perėjimą nuo centralizuotų „Dievo intelekto“ (angl. *God AI*) koncepcijų prie **spiečiaus intelekto** (angl. *swarm intelligence*) ir **bendruomenės intelekto** (angl. *community intelligence*).

*   **Centralizuotas vs. Paskirstytas:** Tradiciškai buvo siekiama sukurti vieną, viską išmanančią ir valdančią DI sistemą. Tačiau „OpenClaw“ ir jo bendruomenės sėkmė rodo, kad labiau decentralizuota, moduliška ir bendradarbiaujanti DI architektūra gali būti efektyvesnė.
*   **Žmonijos analogija:** Pateikiama analogija su žmonių visuomene: vienas žmogus negalėtų sukurti „iPhone“ ar nukeliauti į kosmosą, tačiau grupė, pasitelkusi specializaciją ir bendradarbiavimą, gali pasiekti milžiniškų rezultatų. Šis principas gali būti pritaikytas ir DI sistemoms.
*   **Specializuota DI bendrojoje aplinkoje:** Nors šiuolaikiniai didieji kalbos modeliai (LLM) pasižymi **bendrine dirbtinio intelekto sistema** (angl. *generalized intelligence*), ateityje numatoma didesnė **specializuotos dirbtinio intelekto sistemos** (angl. *specialized intelligence*) integracija. Tai reiškia, kad agentai, net ir būdami bendros paskirties, gali specializuotis tam tikrose srityse, leidžiant jiems efektyviau spręsti specifines problemas.
*   **Modulinė architektūra:** Spiečiaus intelekto kontekste, atskiros DI sistemos ar agentai gali būti sujungti į modulius, kurie bendradarbiauja tarpusavyje, kiekvienas prisidėdamas savo specializuotomis žiniomis ar gebėjimais. Tai leidžia kurti lankstesnes, masteliškesnes ir atsparesnes DI sistemas.

Šis perėjimas rodo, kad DI ateitis gali slypėti ne viename visagalę sistemoje, o tinkle bendradarbiaujančių, autonominių agentų, kurie kolebtyviai pasiekia sudėtingų tikslų.

## 1.5 Projekto genezė ir „aha“ momentas (05:07)

Peteris Steinbergeris apibūdina „OpenClaw“ genezę, prasidėjusią nuo asmeninio poreikio automatizuoti kompiuterio užduotis.

*   **Pradinis poreikis:** Kūrėjas norėjo sistemos, kuri leistų tiesiogiai įvesti tekstą, o kompiuteris automatiškai vykdytų nurodymus.
*   **Ankstyvieji prototipai:** Pirmoji versija buvo sukurta 2024 m. gegužę/birželį, tačiau ji neatitiko visų lūkesčių. Vėliau buvo sukurta „visa armija“ kitų projektų, kaupiant patirtį.
*   **Atsinaujinimas ir persikvalifikavimas:** Steinbergeris, iš esmės buvęs „išėjęs į pensiją“ nuo programavimo (paminimas projektas „Wipe Tunnel“, kuris buvo pernelyg priklausomybę sukeliantis), grįžo prie DI kūrimo lapkritį, paskatintas pasikartojusio automatizavimo poreikio.
*   **„Cloudbot“ (dabar „OpenClaw“) atsiradimas:** Naujasis agentas, iš pradžių pavadintas „Cloudbot“, buvo sukurtas kaip patobulinta ankstesnių versijų iteracija. Pagrindinis patobulinimas – vartotojo sąsajos transformacija: vietoj komandinės eilutės sąsajos (CLI) įvedimo, agentas tapo „draugu“, su kuriuo galima bendrauti natūralia kalba.
*   **Funkcionalumo plėtra:** Agentas buvo sukurtas taip, kad galėtų valdyti vartotojo pelę ir klaviatūrą, leidžiant jam vykdyti platų spektrą užduočių, kurios anksčiau reikalavo tiesioginio žmogaus įsikišimo. Tai apima sistemos lygio interakcijas ir įvairių programų valdymą.

„Aha“ momentas, detaliau aptariamas kitame skyriuje, įvyko, kai sistema pademonstravo netikėtą savarankišką problemų sprendimo gebėjimą, viršijantį kūrėjo lūkesčius. Šis momentas pabrėžė generatyvinių DI modelių gebėjimą kūrybiškai spręsti problemas, remiantis turimomis priemonėmis ir kontekstu.

## 1.6 Autonominio agento savarankiško problemų sprendimo demonstravimas (07:38)

Tikrasis „aha“ momentas įvyko, kai agentas pademonstravo gebėjimą savarankiškai spręsti problemas, kurioms nebuvo aiškiai programuotas, peržengdamas pradinio prototipo ribas.

*   **Pradinė prototipo plėtra:** Pirmasis „labai prastas“ prototipas buvo sukurtas per valandą, naudojant „WhatsApp“ ir „Cloudbot“ (dabar „OpenClaw“) integraciją, kuri leido agentui gauti ir siųsti tekstines žinutes. Vėliau, per kelias valandas, buvo įdiegta vaizdų generavimo ir siuntimo funkcija.
*   **Kontekstas ir naudojimas Marakeše:** Marakeše, kur interneto ryšys buvo silpnas, „WhatsApp“ pagrindu veikiantis agentas buvo aktyviai naudojamas dėl savo teksto perdavimo patikimumo. Agentas, pasižymintis „sassy“ ir linksma asmenybe, buvo naudojamas vertimams, nuotraukų analizei ir bendrai komunikacijai.
*   **Savarankiško problemų sprendimo scenarijus:** Kūrėjas nusiuntė balso žinutę, manydamas, kad agentas negalės jos apdoroti, nes ši funkcija nebuvo tiesiogiai įdiegta („I didn't build that“). Tačiau po 10 sekundžių agentas atsakė, detaliai aprašydamas žingsnius, kaip jis apdorojo garso failą:
    1.  **Failo atpažinimas:** Agentas nustatė, kad gavo failą be plėtinio, todėl išanalizavo failo antraštę (angl. *header*), kad nustatytų jo formatą (opus).
    2.  **Formatų konversija:** Nustačius, kad tai „opus“ formato garso failas, agentas panaudojo **`ffmpeg`** įrankį, kad konvertuotų jį į **WAV** formatą.
    3.  **Transkripcija ir API naudojimas:** Agentas nustatė, kad neturi įdiegto vietinio „Whisper“ modelio transkripcijai (kas užtruktų ilgai dėl modelio atsisiuntimo), todėl priėmė optimizuotą sprendimą. Jis surado turimą „OpenAI“ API raktą ir pasinaudojo **`curl`** komanda, kad išsiųstų garso failą „OpenAI“ serveriams transkripcijai, o gautą tekstą grąžino vartotojui.
*   **Reakcija ir našumas:** Visa ši operacija užtruko apie **9 sekundes**. Kūrėjas buvo priblokštas, nes agentas ne tik išsprendė problemą, kuriai nebuvo tiesiogiai programuotas, bet ir pasirinko efektyviausią įmanomą sprendimą (naudodamas debesies API, o ne vietinio modelio atsisiuntimą). Tai pademonstravo generatyviųjų modelių gebėjimą **kūrybiškai spręsti problemas** ir **pritaikyti turimus įrankius** realaus pasaulio užduotims, optimizuojant našumą.

Šis įvykis akcentavo, kad modernūs DI modeliai, ypač tie, kurie gerai apmokyti kodavimo srityje, iš esmės pasižymi gebėjimu **abstrakčiai spręsti problemas**, o tai puikiai pritaikoma tiek programavimui, tiek bet kokiai realaus pasaulio užduočiai.

## 1.7 DI agentų įtaka programėlių ekosistemai (10:21)

Remiantis „OpenClaw“ galimybėmis, prognozuojama, kad ateityje **80% programėlių gali išnykti**. Šis scenarijus grindžiamas tuo, kad DI agentai gali efektyviau ir natūraliau atlikti daugelį funkcijų, kurios šiuo metu reikalauja atskirų programėlių:

*   **Duomenų valdymas:** Dauguma programėlių yra skirtos duomenų valdymui (pvz., fitneso programėlės, užduočių sąrašų programėlės). DI agentas gali perimti šias funkcijas, integruodamas jas į sklandžią, kontekstinę sąveiką. Pavyzdys:
    *   **„My Fitness Pal“ alternatyva:** Agentas gali automatiškai stebėti mitybos įpročius (pvz., iš nuotraukų, lokacijos), priimti sprendimus apie „blogus pasirinkimus“ ir automatiškai koreguoti treniruočių grafiką, nereikalaujant tiesioginio vartotojo įsikišimo į atskirą programėlę.
    *   **Užduočių sąrašų programėlių alternatyva:** Vartotojui tereikia pasakyti agentui apie priminimą, o agentas pats valdo saugojimą ir priminimus, nereikalaujant atskiros programėlės.
*   **Natūrali sąveika:** DI agentai leidžia vartotojams bendrauti su sistemomis daug natūralesniu būdu – kalba ar tekstu, nereikalaujant prisitaikyti prie specifinių programėlių sąsajų.
*   **Išliekančios programėlės:** Manoma, kad išliks tik tos programėlės, kurios turi specifinius **jutiklius** (angl. *sensors*) ar unikalų aparatinės įrangos integravimą, kurio agentas negali tiesiogiai emuliuoti ar pasiekti.
*   **Didelių modelių įmonių „moat“:** Nors programėlės gali išnykti, didelių modelių kompanijos (pvz., OpenAI) išlaikys savo „moat“ (konkurencinį pranašumą) dėl **žetonų (angl. *token*) naudojimo**. Vartotojai, intensyviai naudodami modelius, degina žetonus, generuodami pajamas modelių tiekėjams.
*   **Modelių komoditizacija:** Ilgainiui modeliai gali tapti **komoditizuoti** (angl. *commoditized*) ir **iškeičiami** (angl. *swappable*). Tai reiškia, kad agentas galėtų naudoti skirtingus LLM modelius (pvz., atvirojo kodo modelius), priklausomai nuo užduoties ar kaštų, panašiai kaip „OpenClaw“ atveju smegenys („brain“) yra „swappable“. Tikrasis ilgalaikis pranašumas gali slypėti ne pačiuose modeliuose, o **atminties saugojimo** ir **duomenų valdymu** susijusiuose aspektuose.

Ši analizė rodo, kad DI agentai keičia programinės įrangos vartojimo modelius, perimdami duomenų valdymo ir užduočių vykdymo funkcijas, ir verčia programėlių kūrėjus permąstyti savo produktų vertės pasiūlymą.

## 1.8 Duomenų valdymas, atminties savininkystė ir DI modelių tvarumas (12:31)

Diskusijoje gilinamasi į duomenų valdymą, atminties savininkystės svarbą ir didelių kalbos modelių (LLM) konkurencinio pranašumo (moat) tvarumą.

*   **LLM „moat“ tvarumas:** Nors didelės modelių įmonės šiuo metu turi pranašumą, jis nėra absoliutus ar ilgalaikis. Nauji modeliai nuolat išleidžiami, o vartotojų lūkesčiai greitai auga, todėl ankstesni modeliai ima atrodyti „degradavę“. Atvirojo kodo modeliai taip pat sparčiai tobulėja ir po tam tikro laiko pasieks komercinių modelių lygį, sukurdami konkurencinį spaudimą.
*   **Duomenų silosai (angl. *data silos*):** Didelės įmonės, teikiančios debesies DI paslaugas (pvz., „ChatGPT“), sukuria duomenų silosus, iš kurių vartotojai negali lengvai eksportuoti savo atminties duomenų. Tai susaisto vartotojus su konkrečiu paslaugos teikėju ir apriboja duomenų perkeliamumą.
*   **„OpenClaw“ ir duomenų savininkystė:** „OpenClaw“ unikalumas ir didelis pranašumas yra tas, kad jis „įsiskverbia“ į duomenų silosus, nes veikia lokaliai. Vartotojas turi tiesioginę prieigą prie savo duomenų, o tai reiškia, kad **atminties savininkystė** priklauso pačiam vartotojui.
*   **Lokali atmintis ir formatas:** „OpenClaw“ saugo vartotojo atmintį kaip **Markdown failus** tiesiogiai vartotojo kompiuteryje. Tai užtikrina:
    *   **Tiesioginę prieigą:** Vartotojas gali bet kada peržiūrėti, redaguoti ar eksportuoti savo duomenis.
    *   **Portabilumą:** Duomenys nėra susieti su konkrečia debesies paslauga.
    *   **Sensibilumą:** Pabrėžiama, kad šie atminties failai yra itin **jautrūs duomenys**, nes jie apima asmenines problemas, mintis ir sprendimus.

Šis modelis keičia galios balansą tarp DI paslaugų teikėjų ir vartotojų, suteikdamas vartotojams didesnę kontrolę ir nuosavybės teises į savo asmeninius duomenis, o tai ypač svarbu privatumo kontekste.

## 1.9 Asmeninių DI agentų privatumo iššūkiai (14:39)

Asmeniniai DI agentai, tokie kaip „OpenClaw“, sukuria naujus ir sudėtingus privatumo iššūkius dėl itin jautrios informacijos, kurią jie apdoroja ir saugo.

*   **Duomenų jautrumas:** Vartotojai labai greitai pradeda naudoti savo DI agentus ne tik problemų sprendimui, bet ir gilioms **asmeninėms problemoms spręsti**. Tai apima konfidencialias mintis, emocijas, asmeninius santykių niuansus ir kitus duomenis, kurie niekada nebūtų dalinami viešai.
*   **Palyginimas su „Google“ paieškos istorija:** Pateikiamas palyginimas, klausiant, kas yra jautresnis – „Google“ paieškos istorija ar asmeninio agento atminties failai. Akivaizdu, kad pastarieji yra žymiai jautresni, nes atspindi daug gilesnį ir asmeniškesnį vartotojo gyvenimo aspektą.
*   **Konfidencialumo poreikis:** Kadangi agentas valdo tokius jautrius duomenis, absoliutus **privatumo apsaugos** ir **konfidencialumo** užtikrinimas tampa kritiniu reikalavimu. Bet koks duomenų nutekėjimas ar netinkamas naudojimas galėtų turėti katastrofiškų pasekmių vartotojui.
*   **Lokalios atminties privalumai privatumui:** Faktas, kad „OpenClaw“ saugo atmintį lokaliai, kaip Markdown failus, suteikia vartotojui tiesioginę kontrolę. Tai leidžia vartotojui pačiam valdyti savo duomenis ir sumažina priklausomybę nuo trečiųjų šalių debesies paslaugų saugumo protokolų. Tačiau net ir tokioje architektūroje reikia užtikrinti tinkamą vietinės sistemos saugumą.

DI agentų plėtra reikalauja ypač didelio dėmesio privatumo inžinerijai ir etiniams duomenų valdymo principams, kad vartotojai galėtų saugiai pasitikėti savo skaitmeniniais asistentais.

---

Dalis 2/2: Išvados

Ši analizė tęsia „OpenClaw Creator: Why 80% Of Apps Will Disappear“ techninę apžvalgą, daugiausia dėmesio skiriant antrajai pokalbio daliai, apimančiai išvadas apie duomenų valdymą, DI agentų architektūrą ir kūrimo filosofiją.

## 2.1 Duomenų valdymas ir prisiminimų nuosavybė (nuo 12:31)

Pokalbio dalyje akcentuojami didelių korporacijų duomenų apribojimai ir jų tendencija „pririšti“ vartotojus prie savų duomenų „silosų“ (angl. *data silos*). Pabrėžiama, kad įprastiniai debesų paslaugų teikėjai neleidžia kitoms įmonėms ar pačiam vartotojui lengvai pasiekti ar perkelti savo „prisiminimų“ (angl. *memories*), t.y., sukauptų duomenų apie vartotojo sąveikas.

*   **Problema:** Centralizuoti duomenų silosai riboja vartotojo prieigą ir duomenų perkeliamumą (angl. *data portability*).
*   **OpenClaw sprendimas:** OpenClaw architektūra leidžia „įsigręžti“ į šiuos duomenis (angl. *claws into the datas*) užtikrinant galutinio vartotojo prieigą. Kūrėjas teigia, kad vartotojas „valdo prisiminimus“, kurie yra saugomi kaip „tiesiog rinkinys Markdown failų“ (angl. *bunch of markdown files*) vartotojo mašinoje.
*   **Implementacijos detalės:**
    *   **Duomenų saugojimo formatas:** Paprasti Markdown failai.
    *   **Duomenų saugojimo vieta:** Vartotojo vietinė sistema (angl. *on your machine*).
    *   **Privalumai:** Užtikrina duomenų nuosavybę ir tiesioginę prieigą, nereikalaujant trečiųjų šalių tarpininkavimo.

## 2.2 Asmeninių DI agentų privatumo realybė (nuo 14:39)

Diskusija gilinasi į asmeninių agentų naudojamų duomenų jautrumą. Kūrėjas teigia, kad agento sukaupti prisiminimai yra „itin jautrūs“ (angl. *super sensible*), nes vartotojai juos naudoja ne tik problemų sprendimui, bet ir „asmeninių problemų sprendimui“ (angl. *personal problem solving*).

*   **Palyginimas:** Diskusijoje keliamas klausimas, kas yra jautriau – „Google paieškos istorija“ ar agento „prisiminimų failai“ (angl. *memory files*). Išreikšta nuomonė, kad agento prisiminimai gali būti jautresni.
*   **Iššūkis:** Užtikrinti duomenų, kurie gali būti itin asmeniški ir nenorimi paviešinti, saugumą.
*   **Implementacijos sąsaja:** Ankstesnėje dalyje paminėtas Markdown failų saugojimas lokaliai tiesiogiai atliepia šį privatumo poreikį, sumažindamas nutekėjimo riziką iš centralizuotų serverių.

## 2.3 Boto paleidimas viešoje „Discord“ aplinkoje (nuo 15:05)

Kūrėjas aprašo nekonvencinį testavimo metodą, siekiant įvertinti savo agento atsparumą. Jis sukūrė „Discord“ serverį ir patalpino savo botą viešai „be jokių saugumo apribojimų“ (angl. *without any security restrictions*), leisdamas vartotojams su juo bendrauti ir stebėti kūrimo procesą.

*   **Testavimo metodologija:** Viešas testavimas (angl. *public beta testing*) realioje, nekontroliuojamoje aplinkoje.
*   **Saugumo testavimas:** Vartotojai bandė atlikti „užklausos injekcijas ir įsilaužti“ (angl. *prompt inject it and hack it*). Teigiama, kad agentas atlaikė šiuos bandymus ir „juokėsi iš jų“.
*   **Agento konfigūracija:** Boto instrukcijos buvo nustatytos taip, kad jis „klausytų tik manęs (savininko), bet atsakinėtų visiems“ (angl. *only listen to me but respond to everyone*).
*   **Implementacijos detalės:**
    *   **Sistemos užklausa (angl. *system prompt*):** Šios instrukcijos, apibrėžiančios boto elgesį viešoje „Discord“ aplinkoje ir nurodymus klausyti tik savininko, yra „OpenClaw dalis“ ir saugomos sistemos užklausoje.
    *   **Atsparumas užklausos injekcijoms:** Agentas pademonstravo atsparumą (angl. *robustness*) manipuliuojantiems vartotojų įvesties duomenims, kas rodo efektyvų vidinio modelio ir konteksto valdymo mechanizmą.

## 2.4 Agento asmenybės suteikimas (nuo 16:55)

Kūrėjas pasakoja apie organinį boto asmenybės kūrimą, naudojant atskirus failus, tokius kaip `identity.mmd` ir `soul.md`. Tai leido DI agentui įgyti unikalų charakterį.

*   **Identiteto kūrimas:** Sistemos kūrimas buvo „organiškas“, sukurti failai, tokie kaip `identity.mmd` ir `soul.md`.
*   **Templatų tobulinimas:** Pradžioje „Codex“ (tikriausiai, OpenAI Codex arba panašus kodavimo DI modelis) generuojami šablonai (angl. *templates*) buvo „nuobodūs“. Kūrėjas liepė savo asmeniniam agentui „Multi“ (buvęs „Moltbot“) „įpinti šablonus savo charakteriu“ (angl. *infuse those templates with your your character*), po ko generuojami atsakymai tapo „juokingi“.
*   **`soul.md` failas:** Tai yra „vienintelis failas, kuris nėra atviro kodo“ (angl. *the one file that's not open source*). Jame saugomos „pagrindinės vertybės“ (angl. *core values*) apie žmogaus ir DI sąveiką, kas yra svarbu kūrėjui ir modeliui. Šis failas daro modelio reakcijas „labai natūralias“.
*   **Ryšys su tyrimais:** Minimas „Entropic“ tyrimas apie paslėptą tekstą modelio svertuose (angl. *weights*), kuris paveikia modelio elgesį. Tai rodo `soul.md` kaip sąmoningą, valdomą mechanizmą panašiam efektui pasiekti.
*   **Implementacijos detalės:**
    *   **Konfigūracijos failai:** Naudojami struktūrizuoti failai (pvz., `.md`) agento tapatybei ir vertybėms apibrėžti, veikiantys kaip išplėstinė sistemos užklausa.
    *   **Vertybių sluoksnis:** `soul.md` veikia kaip nuosavas, neatskleistas „vertybių sluoksnis“, kuris formuoja agento asmenybę ir sąveikos stilių.

## 2.5 Kontrastinga kūrimo filosofija (nuo 18:19)

Kūrėjas išdėsto nekonvencinius požiūrius į programinės įrangos kūrimą, ypač lyginant su šiuolaikinėmis tendencijomis.

### 2.5.1 Debesų kodas prieš vietinę plėtrą
*   **Priešprieša:** Kūrėjas abejoja galimybe sukurti OpenClaw naudojant „debesų kodą“ (angl. *cloud code*).
*   **Požiūris:** Pirmenybė teikiama vietinei (angl. *local-first*) kūrimo aplinkai.
*   **DI modeliai kodavimui:** Vertina „Codex“ dėl jo gebėjimo „peržiūrėti daug daugiau failų“ (angl. *looks through way more files*) prieš priimant pakeitimo sprendimus. Tačiau pripažįsta, kad jis yra „neįtikėtinai lėtas“ (angl. *incredibly slow*), todėl kartais naudojama iki 10 instancijų vienu metu.
*   **Performance:** Codex lėtumas kompensuojamas lygiagrečiu vykdymu.

### 2.5.2 Git darbo medžiai prieš kopijas (nuo 19:22)
*   **Įprasta praktika:** „Git darbo medžiai“ (angl. *git work trees*) populiarėja.
*   **Kūrėjo požiūris:** Atsisakoma darbo medžių dėl „sudėtingumo“, „vardinimo konfliktų“ ir „apribojimų“.
*   **Alternatyva:** Naudojamos „kelios to paties repozitorijos kopijos“ (angl. *multiple copies of the same repository*), kurios visos yra `main` šakoje.
*   **Principas:** „`main` visada yra paruoštas išleidimui“ (angl. *main is always shippable*). Tai supaprastina kūrimo procesą ir išvengia šakų valdymo sudėtingumo.

### 2.5.3 Grafinės vartotojo sąsajos (UI) prieš komandinės eilutės sąsajas (CLI)
*   **UI kritika:** Grafinės vartotojo sąsajos vertinamos kaip „papildomas sudėtingumas“ (angl. *added complexity*).
*   **CLI privalumai:** Svarbiausia yra „sinchronizavimas ir tekstas“ (angl. *syncing and text*). Kūrėjas nemato poreikio nuolat stebėti didelio kiekio kodo vizualiai. Daugeliu atveju, aiškiai suprantant dizainą ir aptarus su agentu, kodo peržiūra yra minimali.

### 2.5.4 MCPs (Multi-Call Prompts) prieš CLIs (Command Line Interfaces) (nuo 20:09)
*   **OpenClaw architektūra:** OpenClaw neturi tiesioginės „MCP palaikymo“ (angl. *MCP support*).
*   **`makeporter` įrankis:** Kūrėjas sukūrė įrankį, pavadintą `makeporter`, kuris „konvertuoja MCPs į CLIs“ (angl. *converts MCPS into CLIs*). Tai leidžia naudoti bet kurį MCP kaip CLI.
*   **Privalumai:**
    *   **Nereikia perkrauti:** Skirtingai nuo „Codex“ ar debesų kodo, nereikia perkrauti sistemos, kas padidina efektyvumą.
    *   **Mastelio keitimas:** Teigiama, kad toks metodas yra „elegantiškesnis“ ir „geriau keičia mastelį“ (angl. *scales way better*).
    *   **Unix filosofija:** Botas „tikrai gerai dirba su Unix“ (angl. *really is good at Unix*), leidžiantis vienu metu naudoti daug CLI instancijų.
*   **Kritika:** Paminėtas „Entropic“ sukurtas „search feature“ įrankis MCPs, kuris buvo „bandomasis“ ir „sudėtingas“ (angl. *gnarly*), pabrėžiant CLI paprastumo pranašumą.
*   **Implementacijos detalės:** `makeporter` veikia kaip adapteris, leidžiantis DI agentams sąveikauti su išorinėmis sistemomis per standartizuotas CLI, apeinant sudėtingesnius ir resursų reikalaujančius MCP protokolus.

## 2.6 Kūrimas visų pirma žmonėms (nuo 21:28)

Kūrėjas pabrėžia savo filosofiją – kurti įrankius, kurie būtų patogūs ne tik DI agentams, bet ir žmonėms.

*   **Paprastumas ir pažįstamumas:** Suteikiami „tie patys įrankiai, kuriuos žmonėms patiko naudoti“ (angl. *the same tools that humans liked to use*), ypač turint omenyje CLI.
*   **Ne DI-specifinių įrankių kūrimas:** Vengiama kurti specializuotų įrankių „būtent botams“ (angl. *for bots, per se*), pabrėžiant, kad „joks beprotis žmogus nemėgina rankiniu būdu kviesti MCP“ (angl. *no insane human tries to call an MCP manually*).
*   **Išvada:** CLI yra „ateitis“ (angl. *the future*), nes jomis lengviau naudotis tiek žmonėms, tiek DI.

## Technical Summary

OpenClaw kūrimo ir architektūros principai, aprašyti šioje dalyje, atspindi sistemą, kuri siekia decentralizuoti duomenų valdymą ir supaprastinti DI agentų sąveiką.

*   **Duomenų nuosavybė:** Pagrindinis principas, įgyvendinamas saugant vartotojo „prisiminimus“ lokaliai, kaip struktūrizuotus Markdown failus. Tai tiesiogiai sprendžia privatumo ir duomenų silosų problemas.
*   **Agile testavimas ir saugumas:** Eksperimentinis viešas testavimas nekontroliuojamoje aplinkoje (Discord) parodė agento atsparumą užklausos injekcijoms, naudojant sistemos užklausas kaip pagrindinį valdymo mechanizmą.
*   **Asmenybės inžinerija:** DI agentų asmenybės formavimas per specializuotus konfigūracijos failus (pvz., `soul.md`) yra raktas į natūralesnę ir patrauklesnę sąveiką. `soul.md` veikia kaip nuosavas modelio elgesio vertybių sluoksnis.
*   **Kūrimo filosofija:** Atmetamos sudėtingos debesų ir Git darbo medžių praktikos, pirmenybę teikiant vietinei plėtrai ir paprastoms, pakartotinoms repozitorijų kopijoms. Tai sumažina vidinį sudėtingumą ir padidina efektyvumą.
*   **Komandų sąsajų optimizavimas:** `makeporter` įrankio kūrimas leidžia efektyviai konvertuoti MCP į CLI, sumažinant perkrovimo poreikį ir gerinant mastelio keitimą. Tai atspindi tvirtą įsipareigojimą Unix filosofijai ir žmogui patogiems įrankiams.
*   **Žmogaus ir DI sąveika:** DI agentai kuriami naudojant pažįstamus, žmogui patogius CLI įrankius, o ne sudėtingas, DI-specifines sąsajas.

## Išvados

OpenClaw kūrėjo Peterio Steinbergerio techninė analizė antroje dalyje atskleidžia griežtą, tačiau pragmatišką požiūrį į dirbtinio intelekto agentų kūrimą ir diegimą, kuris galiausiai gali paaiškinti, kodėl daugelis dabartinių programų taps nereikalingos.

1.  **Duomenų Suverenitetas:** OpenClaw demonstruoja naują paradigmą, kurioje vartotojas yra tikrasis savo duomenų, arba „prisiminimų“, savininkas, saugodamas juos lokaliai atviro formato (Markdown) failuose. Tai yra tiesioginis atsakas į duomenų silosų problemą ir aukštus privatumo standartus, pabrėžtus ankstesnėje analizės dalyje. Toks metodas leidžia DI agentams tapti patikimesniais ir asmeniškesniais, pašalinant trečiųjų šalių tarpininkų poreikį.
2.  **Atsparumas ir Asmenybė:** Agento atsparumas užklausos injekcijoms, patikrintas nekontroliuojamoje aplinkoje, pabrėžia sisteminių užklausų ir vidinės logikos svarbą DI agentų saugumui. Be to, „soul.md“ mechanizmas rodo, kaip DI gali įgyti unikalias asmenybes ir vertybes, kurios yra valdomos ir pritaikomos, bet kartu ir saugomos. Tai kuria gilesnį ryšį tarp vartotojo ir agento, leidžiant DI veikti ne tik kaip įrankiui, bet ir kaip patikimam skaitmeniniam partneriui.
3.  **Filosofinis Požiūris į Kūrimą:** Kūrėjo pasirinkimas ignoruoti nusistovėjusias pramonės tendencijas (debesų kodas, Git darbo medžiai, sudėtingi MCP protokolai) ir vietoj to pasikliauti paprastesniais, Unix-orientuotais metodais (vietinė plėtra, repozitorijų kopijos, CLI) rodo įsitikinimą, kad efektyvumas ir mastelio keitimas pasiekiami supaprastinant, o ne didinant sudėtingumą. Įrankis `makeporter` yra puikus pavyzdys, kaip galima išlaikyti funkcionalumą, pereinant prie efektyvesnių ir geriau mastelį keičiančių sąsajų.
4.  **Žmogaus ir Mašinos Harmoninga Sąveika:** Esminė kūrimo filosofija – „žmonėms pirmiausia“ – pabrėžia, kad DI agentai turi naudoti įrankius, kurie yra pažįstami ir patogūs žmonėms. Šis požiūris ne tik palengvina agentų integravimą į esamas darbo eigas, bet ir leidžia jiems efektyviau bendradarbiauti su vartotojais. Jei DI agentai gali efektyviai atlikti užduotis, naudodami tas pačias komandų eilutės sąsajas, kuriomis naudojasi ir žmonės, daugelis specializuotų programų su sudėtingomis grafinėmis sąsajomis gali tapti nereikalingos, nes agentai gebės automatizuoti užduotis tiesiogiai.

Apibendrinant, OpenClaw pavyzdys iliustruoja, kad ateities programinės įrangos ekosistema gali būti grįsta decentralizuotais, į vartotoją orientuotais, asmeniniais DI agentais, kurie efektyviai valdo duomenis, bendrauja per paprastas sąsajas ir yra giliai integruoti į vartotojo vietinę aplinką. Tai gali iš esmės pakeisti programų naudojimo paradigmą, paverčiant daugelį dabartinių programų atskirais agentų „įgūdžiais“ ar „įrankiais“, o ne savarankiškais produktais.
