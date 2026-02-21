---
title: "Dvi sekundės, kurios viską pakeitė: NVIDIA išmokė robotus mąstyti prieš veikiant"
date: 2026-01-11T17:16:39.939898+00:00
category: Mokslas
tags:
 - verslas
 - technologijos
 - robotai
 - intelektas
 - inovacijos
original_slug: dvi-sekundes-kurios-viska-pakeite-nvidia-ismoke-robotus-mastyti-pries-veikiant
---

[Originalo autorius: Mohamed Abdelmenem](https://levelup.gitconnected.com/the-chatgpt-moment-for-robotics-nvidia-just-solved-physical-ai-10a0085e8cb1)

**Kol rinka užsiciklinusi ties „geležimi“, Jensenas Huangas tyliai viešai paskelbė „System 2“ mąstymo modelį, kuris išsprendžia Moraveco paradoksą.**

Roboto ranka sustingsta. Ji laiko keraminį kavos puodelį virš kietų plytelių grindų. Dvi sekundes ji nedaro absoliučiai nieko. Inžinieriai, stebintys transliaciją, sulaikė kvėpavimą. Senajame robotikos pasaulyje ši pauzė reiškė klaidą. Kodas pakibo, judesių planuotojas užstrigo cikle arba atvirkštinės kinematikos sprendiklis atsitrenkė į singuliarumą. Tai buvo „mėlynasis mirties ekranas“ techninei įrangai. Tačiau šį kartą pauzė buvo tyčinė. Mašina nepakibo. Ji **galvojo**.

Apsauginis griovys aplink autonominę robotiką išgaravo per vieną pranešimą. Kol pagrindinė žiniasklaida yra apsėsta naujųjų „NVIDIA Vera Rubin“ lustų, Jensenas Huangas tyliai viešai pateikė vienintelį dalyką, kurio realiai reikia kūrėjams: veikiančias smegenis. Štai naujojo „Alpamayo“ technologijų rinkinio analizė, kaip jį paleisti lokaliai ir kodėl kita trilijono dolerių vertės programėlė nebus pokalbių botas.

NVIDIA ką tik nemokamai išleido 1 727 valandas vairavimo duomenų ir 10 milijardų parametrų smegenis. Finansinis barjeras patekti į robotiką ką tik nukrito nuo 10 milijonų dolerių iki nulio. Perskaitykite tai dar kartą. **Apsauginis griovys išgaravo.** Jei esate kūrėjas, kuris jautėsi pavėlavęs į LLM aukso karštinę – tai jūsų antrasis šansas. Dauguma inžinierių susikoncentravo į teraflopsus ir akcijų kainas. Jie praleidžia architektūrinį lūžį, kuris leidžia mašinai atsisiųsti „sveiką protą“ iš interneto. Norint suprasti, kodėl tai svarbu, reikia pažvelgti į problemą, kuri robotikos specialistus vertė sukti galvas 40 metų.

### Smegenų problema
Mes tai vadiname **Moraveco paradoksu**. Suformuluotas Hanso Moraveco devintajame dešimtmetyje, jis teigia: aukšto lygio mąstymui reikia labai mažai skaičiavimų, tačiau žemo lygio sensomotoriniams įgūdžiams reikia milžiniškų skaičiavimo resursų. Matematinė analizė kompiuteriams – lengva. Sulankstyti rankšluostį – neįmanomai sunku.

Dešimtmečius industrija bandė tai išspręsti pasitelkdama gryną logiką. Mokslų daktarų komandos rašė milijonus eilučių C++ kodo, kad apibrėžtų kiekvieną įmanomą sąnario kampą, kolizijos zoną ir trinties koeficientą. Jie kūrė „baigtinių būsenų automatus“ – griežtas elgsenos blokschemas. *Jei jutiklis A mato objektą B, pasuk servo variklį C kampu D.*

Ar kada nors bandėte parašyti kodą, kad robotas sulankstytų marškinius? Tai ribinių atvejų košmaras. Viena klostė ant audinio keičia geometriją. Stalo trintis keičia pasipriešinimą. Jei apšvietimas pasikeis iš rytinio į dieninį, kameros slenkstis „baltiems marškiniams“ gali sugesti. Jei griežtai užprogramuojate judesį, robotas sugenda tą akimirką, kai realybė nukrypsta bent milimetru.

Štai kodėl pramoniniai robotai likdavo narvuose. Jie buvo stiprūs, tikslūs ir visiškai akli niuansams. Jie nebuvo intelektualūs agentai – jie buvo akli magnetofonai, atkartojantys iš anksto įrašytą animaciją. Iki vakar dienos mes bandėme tai spręsti logika. Jensenas ką tik pakeitė logiką **tokenais**.

### „Aha“ momentas: „System 2“ robotams
Sprendimas – nauja modelio architektūra, pavadinta **Alpamayo**. „Alpamayo“ yra **Vision-Language-Action (VLA)** modelis. Norint suprasti VLA, reikia suprasti, kuo jis skiriasi nuo LLM, kuriuos naudojate kasdien. Standartinis LLM (kaip GPT-4) priima tekstinius tokenus ir išduoda tekstinius tokenus. Jis gyvena tik simbolių pasaulyje.

VLA priima vaizdo embedding'us (vaizdo kadrus) ir tekstą, tačiau jo išvestis radikaliai skiriasi. Jis išduoda **motorinio valdymo tokenus**. Jis riešo pasukimą 5 laipsniais traktuoja lygiai taip pat, kaip žodį sakinyje. „Alpamayo“ modeliui „pajudink ranką į kairę“ yra tiesiog kitas logiškas žodis istorijoje, kurią jis rašo.

Tačiau tikrasis proveržis – ne veiksmas. Jis yra **pauzėje**. Modelis įdiegia **„System 2“** mąstymą į fizinius agentus. Ši koncepcija, kurią išpopuliarino Danielis Kahnemanas, apibūdina lėtą, sąmoningą mąstymą priešingai nei greitą, intuityvią reakciją.

Suvokimas (System 1: Greitai).**Mąstymas (System 2: Lėtai).**Veiksmas (System 1: Greitai).Remiantis technine dokumentacija, išleista kartu su modeliu, „Alpamayo“ sugeneruoja vidinę „Mąstymo grandinę“ (Chain of Thought) prieš pajudėdamas. Jis žiūri į kavos puodelį ir modeliuoja jo kritimo pasekmes priešingai nei tvarkingą padėjimą. Jis paleidžia mintinę fizikos simuliaciją prieš užfiksuodamas motorinį tokeną.

„Skirtingai nuo sistemų, apribotų tik suvokimu, Alpamayo leidžia transporto priemonėms paaiškinti, kodėl jos veikia“, – teigiama NVIDIA techniniame tinklaraštyje.Tai išsprendžia „juodosios dėžės“ problemą, kuri neleido neuroniniams tinklams patekti į saugumui kritišką įrangą. Jei robotas sustoja, galite jo paklausti – kodėl. Jis pateiks tekstą: „Pamačiau išriedantį kamuolį, prognozuoju, kad paskui jį išbėgs vaikas, todėl užleidžiu kelią“.

### Pasaulio modelis
Mokyti robotą realiame pasaulyje – lėta, brangu ir pavojinga. Negalima leisti robotui sudaužyti 10 000 kavos puodelių vien tam, kad jis išmoktų gravitaciją. Štai čia atsiranda antroji išleidimo dalis: **Cosmos Reason 2**. „Cosmos“ yra **World Foundation Model (WFM)**. Tai skaitmeninė vaizduotė, suprantanti fiziką.

„Cosmos“ nėra žaidimų variklis. Žaidimų varikliai, tokie kaip „Unity“ ar „Unreal“, naudoja aiškias formules gravitacijai ir susidūrimams skaičiuoti. Jie vykdo žmonių parašytą kodą. „Cosmos“ yra kitoks. Jis naudoja neuroninį tinklą, kad **nuspėtų** kitą vaizdo kadrą pagal fizinę intuiciją. Jis generuoja ateitį pikselis po pikselio, remdamasis tikimybe. Jis išmoko gravitaciją taip pat, kaip kūdikis: stebėdamas, kaip krenta daiktai.

### Simuliacijos kilpa
Tai mus nuveda prie **AlpaSim** – naujos atviros simuliacijos sistemos. Anksčiau robotas, veikiantis simuliacijoje, realiame gyvenime dažnai patirdavo nesėkmę (vadinamasis „Sim-to-Real“ atotrūkis). Simuliacijoje apšvietimas idealus, fizika „švari“. Realybėje – saulė akina, kilimas nelygus, jutikliai triukšmauja. NVIDIA teigia tai išsprendusi „domeno atsitiktinumų parinkimu“ (domain randomization) masišku mastu. „Cosmos“ generuoja tūkstančius chaotiškų variacijų, tad kol kodas pasiekia tikrą robotą, jo smegenys jau būna mačiusios tūkstantį „realybės“ versijų.

### Geležies realybė
Naujieji **Vera Rubin** lustai siūlo 4 kartus didesnį pralaidumą nei ankstesnė „Blackwell“ architektūra. Robotikoje delsa (latency) yra saugumas. Jei robotui reikia 500 ms apdoroti kadrą, važiuodamas 2 m/s greičiu jis nuvažiuos metrą dar prieš nuspausdamas stabdžius. „Rubin“ skirtas ne mokymui, o interferencijai (inference) su 100 ms delsa.

### „App Store“ momentas
Barjeras patekti į rinką ką tik nukrito nuo 10 mln. dolerių iki nulio. Anksčiau norint sukurti robotą-namų šeimininkę reikėjo 50 inžinierių komandos. Dabar tiesiog atsisiunčiate „Alpamayo“. Laimėtojais taps mažos komandos, kurios susikoncentruos į **duomenis**, o ne į bazinius modelius. Vertė nebe smegenyse (jos tapo preke), o duomenyse, skirtuose apmokyti konkrečioms užduotims: skalbinių lankstymui, mikroschemų surinkimui ar pagalbai ligoniams.

### Prognozė
Mes tuoj pamatysime „Stable Diffusion“ fazę robotikoje. Prognozuoju: iki 2026 m. ketvirtojo ketvirčio pirmasis „universalus namų robotas“ pasirodys ne iš „Tesla“ ar „Google“, o iš trijų žmonių komandos, naudojančios „Cosmos“ rinkinį.

**Ką galite padaryti šiandien?**

**Atsisiųskite svorius:** Hugging Face portale ieškokite nvidia/Cosmos-Reason1-7B. (14B modeliui reikia 24GB+ VRAM).**Naudokite specifinį prompt'ą:** Modelis mąsto tik tada, kai priverčiate jį naudoti formatą: [Reasoning Trace] \n [Final Action].**Nenaudokite vaizdo kaip atskirų nuotraukų:** „Cosmos“ reikia bent 17 kadrų konteksto lango, kad suprastų fiziką.Mes praleidome 50 metų bandydami išmokyti robotus judėti apibrėždami kiekvieną raumens krustelėjimą. Mums ką tik pavyko juos išmokyti **svajoti**. Klausimas ne tas, ar mašinos mąstys. O tai, ką jos nuspręs daryti, kai galės.




#verslas
