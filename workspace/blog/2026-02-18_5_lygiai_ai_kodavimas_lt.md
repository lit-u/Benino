# 5 AI kodavimo lygiai (kodėl dauguma jūsų neperžengs 2 lygio)

**Šaltinis (YouTube):** [https://www.youtube.com/watch?v=bDcgHzCBgmQ](https://www.youtube.com/watch?v=bDcgHzCBgmQ)

Kas iš tikrųjų vyksta, kai 90 % „Claude Code“ parašyta pačiu „Claude Code“, bet dauguma programuotojų, naudodami AI, tampa pamatuojamai lėtesni? Įprasta istorija sako, kad AI kodavimo įrankiai visus greitina, bet realybė sudėtingesnė: griežtas tyrimas parodė, kad patyrę kūrėjai užduotis atliko 19 % lėčiau, nors tikėjo, kad dirbo 24 % greičiau.

## Atotrūkis tarp „dark factory“ komandų ir visų kitų
90 % „Claude Code“ parašė „Claude Code“. „Codex“ leidžia funkcijas, parašytas vien „Codex“. Ir vis tiek dauguma kūrėjų, bent pradžioje, su AI tampa lėtesni. Tarp šių dviejų faktų ir gyvena programinės įrangos ateitis.

Įsivaizduokite, kad darbe išgirstate: „Kodo negali rašyti žmonės. Kodo negali net peržiūrėti žmonės.“ Tai realios komandos principai „StrongDM Software Factory“. Tik trys inžinieriai. Niekas nerašo kodo. Niekas neperžiūri kodo. Sistema – AI agentų orkestravimas per markdown specifikacijas. Žmonės rašo specifikacijas ir vertina rezultatą. Mašinos daro viską tarp to.

Tuo pačiu „Anthropic“ pusėje 90 % „Claude Code“ kodo bazės parašyta pačiu įrankiu. Projekto vadovas Boris Cherny viešai sakė, kad jau mėnesius pats kodo nerašo. Vadovybė vertina, kad funkciškai beveik visas kodas įmonėje jau AI generuotas.

Ir vis dėlto 2025 m. METR randomizuotas kontroliuojamas tyrimas parodė: patyrę open-source kūrėjai su AI įrankiais užduotis atliko 19 % lėčiau nei be jų. Dar labiau trikdo tai, kad jie tikėjo priešingai – manė, jog yra 24 % greitesni.

Keli „lights out“ fabrikai dirba žaibiškai. Didžioji industrijos dalis lėtėja, tuo pačiu save įtikinėdama, kad greitėja. Šis atotrūkis šiandien yra svarbiausias technologijų skirtumas.

## Penki „vibe coding“ lygiai
Dan Shapiro pasiūlė 5 lygių modelį.

**Lygis 0 – „spicy autocomplete“**. Tu rašai kodą, AI siūlo kitą eilutę. Tai pagreitintas tab klavišas.

**Lygis 1 – „coding intern“**. Duodi aiškų, mažą darbą: parašyk funkciją, sukurk komponentą, refaktorizuok modulį. AI atlieka, žmogus peržiūri viską.

**Lygis 2 – „junior developer“**. AI daro kelių failų pakeitimus, juda per kodų bazę, supranta priklausomybes. Žmogus vis dar skaito visą kodą.

**Lygis 3 – „developer as manager“**. Santykis apsiverčia. Daugiausia neberašai, o valdai: patvirtini / atmeti feature ar PR lygiu. Įgyvendina modelis.

**Lygis 4 – „developer as product manager“**. Parašai specifikaciją, išeini, grįžęs tikrini rezultatus ir evaluaciją. Kodo beveik nebeskaitai, vertini elgseną.

**Lygis 5 – „dark factory“**. Juoda dėžė: specifikacija į vidų, veikianti programinė įranga į išorę. Žmogus kodo nerašo ir neperžiūri.

Dauguma rinkos šiandien yra tarp 1 ir 3 lygių, o daug kas sustoja ties 3 lygiu dėl psichologinio sunkumo paleisti kontrolę.

## Kaip atrodo tikras 5 lygis
„StrongDM“ pavyzdys laikomas vienu aiškiausių realaus 5 lygio atvejų. Trijų žmonių komanda, nuo 2025 m. vasaros dirbanti „fabriko“ režimu. Jie nurodo, kad lūžis atėjo su „Claude 3.5 Sonnet“, kai ilgų sesijų agentinis kodavimas pradėjo dauginti teisingumą, o ne klaidas.

Sistema veikia su atviro kodo agentu ir trimis markdown specifikacijų failais. Specifikacija aprašo, ką sistema turi daryti. Agentas parašo kodą, paleidžia evaluaciją, išleidžia rezultatą.

## Scenarijai prieš testus: kodėl skirtumas kritiškas
Čia kertinė idėja: jie naudoja ne tradicinius testus, o „scenarijus“.

Tradiciniai testai gyvena kodų bazėje, todėl AI gali „mokytis testui“ ir optimizuoti praeinamumą, nebūtinai teisingumą. Scenarijai laikomi išorėje, kaip holdout rinkinys. Agentas jų nemato kurdamas. Taip sistema negali „apžaisti“ evaluacijos.

Tai naujas praktinis principas AI eros inžinerijai: atskirti kūrimą nuo tikro vertinimo kriterijų.

## „Digital twin“ visata autonominiam kūrimui
Antra kertinė architektūros dalis – „digital twin universe“: išorinės sistemos (pvz., Slack, Jira, Google Docs ir pan.) emuliuojamos kaip elgsenos klonai. Agentai kuria prieš šią simuliaciją, ne prieš realias produkcines sistemas ir duomenis.

Tai leidžia vykdyti pilnas integracines evaluacijas su aukštu saugumu ir aukštu iteracijos greičiu.

## Savireferencinė kilpa Anthropic ir OpenAI viduje
„Codex 5.3“ buvo svarbia dalimi kuriamas ankstesnių „Codex“ versijų darbu: modelis analizavo logus, aptiko nesėkmes, siūlė treniravimo skriptų pataisas. OpenAI skelbė apie reikšmingą spartėjimą ir mažiau švaistomų tokenų šiame cikle.

„Claude Code“ daro panašiai: didelė dalis įrankio kodo parašyta pačiu įrankiu. Tai užsidaranti kilpa: įrankiai kuria įrankius, kurie kuria geresnius įrankius.

## Kodėl patyrę kūrėjai tampa 19 % lėtesni
Pagrindinė priežastis – workflow neatitikimas. AI generuoja greitai, bet žmonės praranda laiką vertindami „beveik teisingą“ kodą, perjungdami kontekstą ir gaudydami subtilias klaidas.

Tai J-kreivė: pradžioje produktyvumas krenta, kol organizacija nepersiprojektuoja proceso aplink AI. Daug įmonių šiandien sėdi J-kreivės apačioje ir klaidingai daro išvadą, kad AI „neveikia“.

Įrankio įdiegimas nėra transformacija. Transformacija yra pilnas proceso perstatymas: specifikacijos standartai, nauji review vartai, naujas CI/CD, nauja klaidų taksonomija.

## Organizacijos sukurtos žmonėms rašyti kodą
Dabartiniai procesai – standup, sprint planning, tradicinis code review, QA struktūros – sukurti žmonių apribojimams kompensuoti. Kai kodą rašo agentai, dalis šių sluoksnių tampa trintimi.

Vaidmenių gravitacija slenka nuo koordinavimo prie artikuliavimo: ne „suderink komandą“, o „aprašyk kryptį taip tiksliai, kad mašina galėtų įgyvendinti“. Tai naujas vadybos ir inžinerinio lyderystės branduolys.

## Siauroji vieta persikelia į specifikacijos kokybę
Implementacijos greitis nebėra pagrindinė problema. Pagrindinė problema – spec kokybė. Jei specifikacija dviprasmė, agentas užpildys spragas savo spėjimais.

Todėl svarbiausi įgūdžiai tampa sisteminis mąstymas, kliento kontekstas, aiškus problemos modeliavimas ir griežta evaluacija.

## „Brownfield“ realybė, kur gyvena dauguma įmonių
Didžioji ekonomikos dalis nėra „greenfield“. Tai seni monolitai, nepilni testai, tribal knowledge ir metai ad-hoc pataisų. Ten neįmanoma tiesiog „uždėti fabriko“ per naktį.

Praktinis kelias dažniausiai toks:
1. AI naudoti 2–3 lygyje esamam darbui spartinti.
2. AI naudoti sistemos elgsenai dokumentuoti ir specifikacijoms kelti iš realaus kodo.
3. Perstatyti CI/CD AI generuojamo kodo mastui.
4. Naują kūrimą perkelti į 4–5 lygio modelius, seną sistemą palaikant paraleliai.

Tai dažnai ne savaičių, o mėnesių ar metų perėjimas.

## Jaunųjų kūrėjų pipeline griūva
Duomenys rodo stiprų junior rolės smukimą: mažiau entry-level pozicijų, mažiau klasikinių mokymosi užduočių, kurios anksčiau augino karjerą. Jei AI paima paprastus bugfix ir CRUD, dingsta įprastas „mokymosi laiptelis“.

Tai nereiškia „programavimo mirties“. Tai reiškia didesnę kartelę nuo pirmų metų: daugiau sisteminio mąstymo, daugiau produkto intuicijos, daugiau gebėjimo dirbti su AI kaip su vykdymo varikliu.

## Samdos poslinkis link generalistų
Rinka vis labiau vertina žmones, kurie mąsto per domenus, o ne tik siaurai per vieną stack'ą. Kai implementaciją daro AI, žmogaus vertė yra problemos erdvės supratimas, prioritetai ir teisinga kryptis.

Specialistas be produkto/domeno suvokimo tampa mažiau vertingas nei generalistas, galintis sujungti sistemą, vartotoją ir verslo apribojimus.

## Kaip atrodo AI-native organizacijų forma
Naujo tipo startuoliai su mažomis komandomis pasiekia labai aukštą revenue per employee. Tai nebe išimtis, o vis dažnesnis šablonas: plokštesnė struktūra, mažiau koordinacinių sluoksnių, daugiau spec + evaluacijos branduolio.

Vidurinė vadybos grandis, QA rankinės peržiūros rolės ir „grynai koordinacinės“ funkcijos bus spaudžiamos transformuotis.

## Ateinantis persitvarkymas
Atotrūkis tarp frontiero ir vidurio nėra įrankio atotrūkis. Tai žmonių, kultūros ir organizacijos atotrūkis. Jo neuždarys vienas vendoris ar nauja versija.

Laimės organizacijos, kurios:
- sąžiningai dokumentuos, ką jų sistemos realiai daro,
- pertvarkys org chart pagal sprendimo kokybę, ne pagal koordinavimo inerciją,
- investuos į žmones, kurie giliai supranta sistemas ir klientus.

## Programinės įrangos paklausa niekada neprisisotina
Istoriškai, kai skaičiavimas pinga, programinės įrangos paklausa ne mažėja, o sprogsta. Taip buvo nuo mainframe iki cloud ir serverless. Tas pats vyksta ir dabar.

Kai kūrimo kaina krenta, ekonomiškai įmanomomis tampa rinkos, kurios anksčiau buvo per mažos arba per brangios aptarnauti. Todėl bendra programinės įrangos rinka plečiasi, o ribojantis veiksnys persikelia į „ką verta statyti ir kam“.

## Pabaiga
„Dark factory“ yra realu ir jau veikia. Tačiau dauguma įmonių dar toli. Vienu metu tiesa yra dvi: frontieras jau labai toli priekyje, o vidurys dar įstrigęs.

Šį atstumą užpildys ne vien AI modeliai. Jį užpildys organizacinis persitvarkymas, žmonių ugdymas ir gebėjimas aiškiai mąstyti apie tai, kas turi būti sukurta.

Būtent tai ir tampa nauju programinės inžinerijos branduoliu.
