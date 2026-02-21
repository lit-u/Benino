# Pasaulinė AI inferencijos krizė: kas iš tikrųjų vyksta su skaičiavimo infrastruktūra

Kas iš tikrųjų vyksta su AI skaičiavimo infrastruktūra? Dažniausia istorija teigia, kad pasiūla pasivys paklausą, bet realybė kur kas sudėtingesnė, kai DRAM kainos šoka 50–60 % per ketvirtį, o kiekvienas hiperskaleris kaupia pajėgumus savo reikmėms.

Šiame tekste pateikiu „vidinį vaizdą“, kodėl pasaulinė inferencijos krizė nėra prognozė, o dabartinių sąlygų stebėjimas:

- Kodėl įmonėse žetonų (token) suvartojimas vienam darbuotojui juda nuo 1 mlrd. link 100 mlrd. per metus
- Kaip atminties, puslaidininkių ir GPU „kamščiai“ susideda, o palengvėjimo tikėtis iki 2028 m. nerealu
- Ką reiškia tai, kad hiperskaleriai renkasi savo produktus, o ne klientus, ir kaip tai keičia resursų paskirstymą
- Kur dabar labiausiai įžvalgūs CTO rezervuoja pajėgumus ir kuria nukreipimo (routing) sluoksnį

Įmonių vadovams, planuojantiems artimiausius 24 mėn., įprastos planavimo schemos nebeveikia, o veikimo langas sparčiai užsidaro.

## Skyriai

- 00:00 Pasaulinė inferencijos krizė
- 02:52 Žetonų suvartojimas sprogsta
- 04:50 Agentinės sistemos keičia viską
- 07:09 Atminties butelio kakliukas
- 08:58 DRAM kainos kyla 50–60 % per ketvirtį
- 11:10 Puslaidininkių gamyklų apribojimai
- 12:08 GPU paskirstymo krizė
- 14:15 Hiperskaleriai yra konkurentai, ne partneriai
- 17:38 Kurie verslo modeliai labiausiai pažeidžiami
- 19:24 Kodėl tradicinės planavimo schemos žlunga
- 22:16 Debesijos įsipareigojimai gali tapti spąstais
- 24:11 Ką dabar daro aštriausi CTO

## 00:00 Pasaulinė inferencijos krizė

Mes sukūrėme ekonomiką, kuri remiasi AI, ir dabar tam ekonomikos modeliui paprasčiausiai nepakanka skaičiavimo. Globalioje technologijų infrastruktūroje formuojasi struktūrinė krizė. Per pastaruosius trejus metus pasaulio ekonomika persitvarkė aplink AI galimybes – tai didžiausias kapitalo projektas žmonijos istorijoje. Šios galimybės visiškai priklauso nuo inferencijos skaičiavimo, o jis jau yra fiziškai ribojamas, ir jokio realaus atokvėpio nesimato iki mažiausiai 2028 m.

Svarbiausi dalykai, kuriuos matau gilindamasis į šią temą:

Pirma, paklausa išlieka eksponentinė ir neribota. Įmonių AI vartojimas auga mažiausiai 10 kartų per metus, nes didėja per darbuotoją tenkanti apimtis ir plinta agentinės sistemos. Čia nėra lubų.

Antra, pasiūla fiziškai ribota bent iki 2028 m. DRAM gamyba užtrunka 3–4 metus, puslaidininkių gamybos pajėgumai pilnai išdalinti, o HBM (high‑bandwidth memory) išpirkta. Naujos talpos tiesiog negali atsirasti pakankamai greitai.

Trečia, visi hiperskaleriai kaupia pajėgumus. Google, Microsoft, Amazon, Meta – jie užsitikrino skaičiavimo rezervus metams į priekį. Tas pats galioja OpenAI ir Anthropic. Jie šiuos resursus naudoja savo produktams, o įmonės konkuruoja dėl to, kas lieka.

Ketvirta, kainos kils šuoliais. Kai paklausa struktūriškai ir stipriai viršija pasiūlą, rinkos neatsistato švelniai. TrendForce prognozuoja, kad vien atminties kaštai 2026 m. pirmoje pusėje padidins inferencijos infrastruktūros kainą 40–60 %. Efektyvios inferencijos sąnaudos per 18 mėn. gali padvigubėti ar patrigubėti.

Penkta, tradicinės planavimo schemos nebeveikia. CAPEX modeliai, nusidėvėjimo grafikai ir kelių metų pirkimų ciklai daro prielaidą apie prognozuojamą paklausą ir prieinamą pasiūlą. Nei viena, nei kita prielaida AI amžiuje nebegalioja.

Ir galiausiai – langas užsitikrinti pajėgumus užsidaro. Įmonės, kurios veikia dabar, gali „užrakinti“ resursus prieš krizės piką. Laukiantys atsidurs konkurso dėl likučių situacijoje arba bus išvis atkirsti.

Tai nėra technologinė problema. Tai ekonominė transformacija, kuri pakeis konkurencinę dinamiką beveik visose industrijose. Pradėkime nuo to, kas yra vartojama. Žinių darbuotojas, aktyviai naudojantis AI įrankius (kodo užbaigimas, dokumentų analizė, tyrimai, susitikimų santraukos), per metus nesunkiai pasiekia apie 1 mlrd. žetonų. Tai dabartinis „sunkusis“ bazinis lygis AI‑pirmose organizacijose. O lubos daug aukščiau – 25 mlrd. žetonų ar daugiau per metus.

## 02:52 Žetonų suvartojimas sprogsta

1 mlrd. žetonų skamba daug, bet realiai tai nėra tiek jau daug. Viena sudėtinga analizės užduotis („peržiūrėk 50 dokumentų ir apibendrinki“) gali suvalgyti apie 0,5 mln. žetonų. Aktyvi kodo rašymo diena gali siekti milijonus. Viena tyrimų sesija su keliomis iteracijomis – iki 10 mln. žetonų. Vartojimas auga, nes mes dar neradome ribos, ką norime daryti su dirbtiniu intelektu. Inteligencijos paklausai ribų nėra.

Šį augimą stumia trys dinamikos. Pirma, galimybės atrakina vartojimą. Modeliams gerėjant, orkestravimo kokybei kylant, vartotojai randa naujų panaudojimų, kurie prieš metus neveikė – pavyzdžiui, sudėtingas samprotavimas. Kiekvienas šuolis generuoja nelinijinę paklausą. Pavyzdys: nuo vieno agento pereiti prie dešimties – tai 10 kartų daugiau paklausos.

Antra, integracijos daugina sąlyčio taškus. AI nebėra atskiras įrankis, kurį atsidarai tik prireikus. Jis integruotas į el. paštą, dokumentų redaktorius, kūrimo aplinkas, CRM ir pan. Kiekviena integracija sukuria „portalą“ nuolatiniam vartojimui.

Trečia, agentai stiprina viską iš viršaus. Perėjimas nuo „žmogus kilpoje“ prie agentinių sistemų, kur AI kviečia AI vis labiau automatizuotais ciklais, nėra paprastas žingsnis. Tai keliais dydžio laipsniais didesnis vartojimas. Vienas agentinis workflow per valandą gali suvalgyti daugiau žetonų, nei žmogus sukuria per mėnesį. Nėra neįprasta prognozuoti, kad vidutinis darbuotojas per artimiausius 12–18 mėn. pasieks 10 mlrd. žetonų per metus, o top vartotojai – 100 mlrd. Tai nėra agresyvi projekcija, tai tiesiog augimo, matomo AI‑pirmose organizacijose, tąsa.

## 04:50 Agentinės sistemos keičia viską

Pažiūrėkime, ką tai reiškia įmonės mastu. Tarkime, turite 10 000 darbuotojų. 1 mlrd. žetonų vienam darbuotojui reiškia 10 trilijonų žetonų per metus. Su mišriu 2 USD už milijoną žetonų tarifu tai yra 20 mln. USD per metus. Brangu, bet „suvalgyta“ Fortune 500 lygiu. Kai vienam darbuotojui tenka 10 mlrd. žetonų, organizacija pasiekia 100 trilijonų per metus, o kaina – 200 mln. USD. Jei agentinės sistemos per 18 mėn. atveda iki 100 mlrd. per darbuotoją, sąskaita tampa 2 mlrd. USD per metus.

Ir šie skaičiavimai daro prielaidą apie stabilias kainas bei prieinamą pajėgumą. Realybėje nei viena prielaida nebegalioja.

Agentinis poslinkis keičia vartojimo modelius iš esmės. Žmogus turi natūralius greičio limitus: jis rašo, ilsisi, dalyvauja susitikimuose, išeina namo. Intensyviai dirbantis žmogus vargiai peržengs ~50 mln. žetonų per dieną. Agentai tokio limito neturi. Agentinė sistema gali veikti nuolat – stebėti, analizuoti, atsakinėti, planuoti. Visai realu, kad vienas darbuotojas, valdantis tokią sistemą, sukels milijardus žetonų per dieną. Agentų „flotas“, dirbantis paraleliai, gali generuoti trilijonus. Tai ne hipotezė – įmonės jau diegia agentines sistemas kodo peržiūrai, saugumo stebėsenai, klientų aptarnavimui, dokumentų apdorojimui. Kiekvienas diegimas kuria nuolatinę 24/7 inferencijos paklausą, kuri gerokai viršija žmogaus vartojimą.

Planuoti 1 mlrd. žetonų vienam darbuotojui reiškia planuoti neteisingą kreivę. Reikia skaičiuoti darbuotojus, jų agentus ir centriniai diegiamus agentus. Bendra vartojimo trajektorija gali būti 10–100 kartų didesnė nei „per žmogų“ skaičiuojant.

## 07:09 Atminties butelio kakliukas

Vienas skaičius puikiai iliustruoja šią trajektoriją: Google viešai deklaravo, kad per mėnesį apdoroja 1,3 kvadrilijono žetonų. Per kiek daugiau nei metus tai yra 130 kartų augimas. Google – pats pažangiausias AI infrastruktūros operatorius ir turi geriausią matomumą į paklausą. Jų vartojimo kreivė – jūsų ankstyvas indikatorius. Jei didžiausias operatorius mato X augimą, įmonių planavimas „tik“ 10x gali būti per konservatyvus.

Ir vis dėlto mes gyvename atminties butelio kakliuke. AI inferencija yra „memory‑bound“. Koks modelis telpa, kokiu greičiu bėga ir kiek vartotojų aptarnaujama – viskas priklauso nuo atminties. Ypač nuo HBM duomenų centrams ir DDR5 visiems kitiems.

Atminties rinka yra sulūžusi. Serverinė DRAM kaina 2025 m. pakilo mažiausiai 50 %, o TrendForce prognozuoja dar 55–60 % augimą per ketvirtį Q1 2026. Kalbame apie triženklius procentinius augimus. DDR5 64 GB RDIMM moduliai, kurie yra „darbinis arkliukas“ įmonių diegimams, gali kainuoti dvigubai daugiau 2026 m. pabaigoje nei 2025 m. pradžioje. Counterpoint Research prognozuoja ~47 % DRAM augimą 2026 m. dėl reikšmingo pasiūlos trūkumo. Nesvarbu, ar renkatės 47 %, ar 55 % – tokie šuoliai nėra ciklinis trūkumas. Čia veikia struktūriniai veiksniai.

## 08:58 DRAM kainos kyla 50–60 % per ketvirtį

Pirma, trys žaidėjai, kontroliuojantys ~95 % pasaulinės atminties gamybos, perskirsto pajėgumus iš vartotojų segmento į enterprise ir AI duomenų centrus. Samsung, SK Hynix ir Micron gamina ne mažiau – jie gamina kitokią atmintį, o hiperskaleriai superka viską.

Antra, HBM koncentracija. HBM yra būtina didelių modelių inferencijai. Tai specializuotas produktas, kurį dominuoja SK Hynix, o jų gamyba paskirstyta Nvidia, AMD ir hiperskaleriais. HBM praktiškai neįmanoma gauti jokiu kiekiu.

Trečia, nauji pajėgumai neatsiranda greitai. Nauja DRAM gamykla kainuoja apie 20 mlrd. USD ir statoma 3–4 metus. Sprendimai, priimti šiandien, realią grąžą duos tik apie 2030 m. Trumpalaikio pasiūlos atsako nėra. Samsung prezidentas viešai sakė, kad atminties trūkumas darys įtaką kainoms per 2026 m. ir vėliau. Tai didžiausias atminties gamintojas tiesiai sako, kad paklausos patenkinti negali.

Po atminties sluoksniu yra dar viena kliūtis – puslaidininkių gamybos pajėgumai. Čia „butelio kakliukas“ dar siauresnis. TSMC gamina pažangiausius čipus, įskaitant Nvidia duomenų centrų GPU. 5 nm, 4 nm ir 3 nm pajėgumai pilnai užpildyti. Nvidia yra didžiausias klientas, Apple – antras, hiperskaleriai užpildo likusią dalį. TSMC plėtra vyksta lėtai: Arizonos FAB nepasieks pilnos gamybos iki 2028 m., Japonija ir Vokietija juda panašiais terminais.

Intel 18A procesas, pademonstruotas CES 2026, yra pirmas rimtesnis JAV alternatyvos signalas. Bet Intel foundry paslaugos dar neįrodytos masto prasme, pajėgumai riboti, o pirmieji didieji klientai (tarp jų Microsoft) „suvalgo“ visą pradinį paskirstymą. Samsung foundry turi problemų su pažangių mazgų išeigomis, todėl yra mažiau patikima alternatyva. Rezultatas nuspėjamas: beveik visa pažangi AI lustų gamyba eina per TSMC Taivane. Rezervinės talpos nėra. Greito sprendimo nėra.

## 12:08 GPU paskirstymo krizė

Dar turime GPU paskirstymo krizę. Nvidia dominuoja AI mokymo ir inferencijos lustuose su ~80 % rinkos dalimi. H100 ir naujosios Blackwell GPU yra duomenų centrų standartas. Abi linijos išpirktos. Didelių GPU užsakymų laukimo laikas viršija 6 mėn. Hiperskaleriai yra užsitikrinę paskirstymą daugiamečiais susitarimais, vertais dešimčių milijardų dolerių. Microsoft, Google, Amazon, Meta, Oracle kartu įsipareigojo šimtais milijardų Nvidia pirkimų per artimiausius metus. Įmonėms lieka tik tai, kas liko, ir to vis mažiau.

Nvidia H200 ir Blackwell, kurie suteikia didelį našumo šuolį, dar labiau riboti. Pradiniai kiekiai pilnai „suvalgyti“ hiperskaleriais. Įmonių prieinamumas neaiškus, o alternatyvos silpnos. AMD Instinct MI300X pagal specifikacijas konkurencingas ir prieinamas didesniais kiekiais, bet programinės ekosistemos branda gerokai atsilieka nuo Nvidia. Intel Gaudi lustai sunkiai susirenka rinkos dalį – programinė ekosistema yra kliūtis. Individualūs sprendimai (Google TPU, Amazon Trainium) įmonėms neprieinami, nebent turite labai specifines sutartis.

Šie variantai nepakeičia bazinės realybės: GPU, kurių reikia įmonėms, priklauso įmonėms, kurios turi paskatą juos naudoti pačios, o ne parduoti.

## 14:15 Hiperskaleriai yra konkurentai, ne partneriai

Tai yra ta vieta, kurią daug analizės praleidžia. AWS, Azure ir Google Cloud nėra neutralūs. Tai AI produktų kompanijos, kurios tiesiog parduoda infrastruktūrą. Jos konkuruoja su savo enterprise klientais. Google savo pajėgumus naudoja Gemini, kuris konkuruoja su bet kokiu enterprise AI diegimu. Microsoft naudoja savo pajėgumus Copilot, konkuruojantį su enterprise produktyvumo AI. Amazon – su AWS AI paslaugomis. Kai skaičiavimas gausus, konfliktas valdomas. Kai skaičiavimas ribotas, konfliktas tampa nulinės sumos.

Kiekvienas GPU, atiduotas enterprise klientui, yra GPU, kuris negali maitinti Gemini, Copilot ar Alexa. Hiperskaleriai privalo rinktis tarp savo produktų ir klientų. Tas pats galioja OpenAI ir Anthropic. Jei GPU nėra OpenAI duomenų centre, OpenAI negali aptarnauti ChatGPT. Kai kyla abejonių, hiperskaleriai rinksis savo produktus. Tai jau vyksta: API kainos mažėjo, bet limitai griežtėjo. Įmonės vis dažniau skundžiasi, kad gauti didelio masto paskirstymą tampa labai sunku.

Šie žaidėjai nėra „blogiečiai“ – jie elgiasi racionaliai. Jų AI produktai yra strateginės prioritetinės kryptys. O infrastruktūros pardavimas enterprise klientams – tik verslas, ne jų pagrindinė „misija“. CTO turi suprasti: debesijos tiekėjai šioje krizėje nėra patikimi partneriai. Jie yra konkurentai, kontroliuojantys ribotą resursą.

Kai rinka funkcionuoja sklandžiai, kainos kyla palaipsniui, paklausa „atsileidžia“, balansas grįžta. Bet šiandien paklausa negali būti atidėta, o pasiūla negali sureaguoti – todėl kainos kils šuoliais. Pirkėjai varžysis, mokės premijas, o pardavėjai kels kainas dėl ekstrakcijos, ne dėl balanso. DRAM kainos 2016 m. buvo šokusios 300 %, GPU kainos per kripto bumą – dvigubai. Atminties kainos svyruoja, nes pasiūlos elastingumas minimalus.

Dabartinė situacija turi visus ingredientus stipriam kainų šuoliui: pasiūla neelastinga, paklausa neelastinga, informacija asimetriška (hiperskaleriai žino daugiau nei įmonės), o koordinacija įmanoma dėl kelių didelių tiekėjų. Tacitinė koordinacija gali vykti net nepažeidžiant antimonopolinių taisyklių.

## 17:38 Kurie verslo modeliai labiausiai pažeidžiami

Kainų šuolio poveikis priklauso nuo verslo modelio. AI‑native startuoliai yra ypač pažeidžiami. Kai kurios kompanijos viešai pripažįsta, kad AI kaštai „suvalgo“ 10 procentinių punktų buvusios 90 % bendrosios maržos. Jei AI jau dabar mažina maržą, o inferencijos kaštai padvigubėja, dalis verslo modelių tampa nebegyvybingi.

Enterprise programinės įrangos įmonės, diegiančios AI funkcijas, patiria panašų spaudimą. AI tampa konkurencine būtinybe, bet kiekviena funkcija mažina maržą. Įmonės turi rinktis tarp konkurencinės būtinybės ir finansinio tvarumo.

Įmonės, naudojančios AI viduje, turi daugiau lankstumo. Jei AI kuria neproporcingą vertę, kainos augimą galima pateisinti, bet per artimiausius dvejus metus biudžeto kontrolė stiprės. Projektai, patvirtinti vienu kaštų lygiu, gali būti atšaukti, kai kaštai padvigubės.

Hiperskaleriai patys kažkiek izoliuoti – jie turi infrastruktūrą, kuri tampa reta. Tačiau net jie susidurs su apribojimais. Google, Microsoft ir Amazon jau perspėja investuotojus apie augančius AI infra kaštus. Didžiausia rizika – „viduryje“ esančioms įmonėms: jos per daug priklausomos nuo AI, kad atsitrauktų, bet per mažos, kad gautų dedikuotą paskirstymą. Tuo pat metu jos konkuruoja rinkose, kur kainų perkėlimas klientams yra sudėtingas.

## 19:24 Kodėl tradicinės planavimo schemos žlunga

Kaip planuoti šioje situacijoje? Tradicinės enterprise IT schemos buvo sukurtos visai kitam laikotarpiui: prognozuojama paklausa, stabili technologija, prieinama pasiūla. Dabar paklausa neprognozuojama ir eksponentiška, technologija kinta greitai, o pasiūla ribota.

CTO, kurie taiko senąsias schemas, sistemingai priims neteisingus sprendimus: per daug įsipareigos ilgalaikiams pirkimams, kurie taps „užstrigę“ aktyvai, per mažai investuos į lankstumą, ir darys prielaidą apie pasiūlą, kurios realiai nėra.

Pavyzdys: įmonė perka 1 000 AI darbo stočių su NPU po 5 000 USD. Tai 5 mln. USD investicija. Finansai nustato 4 metų nusidėvėjimą, tikisi po 1,25 mln. USD vertės per metus. Po dvejų metų tos pačios stotys nebesusitvarko su darbo krūviu, nes vartojimas per darbuotoją išaugo 10 kartų. NPU, kurie pakako kodo užbaigimui ir santraukoms, nebegali aptarnauti agentinių workflow, kurie „suvalgo“ milijardus žetonų. Įranga ne „sugedo“, ji paseno.

Ką daryti? Variantai:

A) tęsti darbą su neadekvačia įranga – darbuotojai lėtėja, konkurentai lenkia, „sutaupymas“ kainuoja produktyvumą.

B) pirkti naują įrangą – tenka nurašyti dalį investicijos, finansai nepatenkinti.

C) nuomoti vietoje pirkimo – mokamas priedas, bet perkeliama nusidėvėjimo rizika. Dažnai tai racionaliausias pasirinkimas, bet didelio masto nuoma įmonėse realiai retai įgyvendinama.

Dažnai „sprendimas“ tampa dideli įsipareigojimai debesijai, taip atidedant realius kaštus. Gali būti, kad įmonių darbo stotys taps „kvailesnės“, o retas debesijos pajėgumas bus perkamas su nuolaidomis, kas hiperskaleriams ir naudinga. Įsipareigojus keliems metams, galima sumažinti kainą 30–50 % palyginus su „on‑demand“. Bet esant 10x metiniam augimui, šie įsipareigojimai virsta spąstais.

## 22:16 Debesijos įsipareigojimai gali tapti spąstais

Scenarijus 1: neįvertini, „parduodi“ per mažai. Prognozuoji 10 trilijonų žetonų, realiai vartoji 30. Už viršijimą moki „on‑demand“, biudžetas sprogsta.

Scenarijus 2: pervertini, per daug įsipareigoji. Prognozuoji 30, realiai vartoji 15. Sumoki už 30 ir pusė išlaidų tampa švaistymu.

Scenarijus 3: pataikai tiksliai. Tai reikalauja preciziškai prognozuoti AI vartojimą, modelių pažangą, efektyvumo augimą ir t. t. Dinaminėje realybėje tikslus spėjimas praktiškai neįmanomas.

Todėl daug įmonių renkasi scenarijų 1 – minimalų įsipareigojimą kaip „grindis“, o tada eina per viršijimus. Būtent čia išryškėja strateginiai svertai, kuriuos naudoja aštriausi CTO.

Principas 1: pajėgumus reikia rezervuoti prieš to prireikiant. Didžiausias poveikis – gauti sutartinius pralaidumo garantus ir SLA prieinamumą. Pokalbiai su tiekėjais turi persikelti nuo „kaina už milijoną žetonų“ prie „ar galite garantuoti X mlrd. per dieną su 99,9 % prieinamumu“. Jei tiekėjas negali garantuoti apimties, kaina tampa antraeilė.

Principas 2: reikia kurti routing sluoksnį. Ilgalaikis konkurencinis pranašumas bus intelektinis sluoksnis, kuris sprendžia, kur vykdyti darbo krūvius. Išmanus „routeris“ optimizuos kaštus, valdys pajėgumus, išlaikys pasirinkimo laisvę, leis derėtis. Bet tai nėra trivialu: reikia architektūros, modelių vertinimo realiu laiku, observability, komandos, kuri tai palaiko. Enterprise mastu šio sluoksnio „outsourcinti“ negalima – tai turi būti „slaptas padažas“.

Principas 3: įrangą reikia traktuoti kaip vartojamą. Bet kokią AI infrastruktūrai pirktą įrangą reikia mentališkai nudėvėti per 2 metus, net jei apskaita sako kitaip. Darbo stotims ir edge įrenginiams verta nuoma, jei įmanoma. Jei perkate – taikykite pagreitintą nusidėvėjimą ir planuokite atnaujinimus kas 18–24 mėn., nes GPU kartos ateina su dideliais šuoliais.

Principas 4: efektyvumas tampa konkurenciniu pranašumu. Kiekvienas nesuvartotas žetonas – tai pajėgumas papildomam darbui. Jei įmonė tą patį pasiekia su 50 % mažiau žetonų, ji turi dvigubą efektyvų pajėgumą. Būtent todėl tokie darbai, kaip DeepSeek „engram“ (faktinių užklausų pigus aptarnavimas), yra įdomūs. Bet tai ne tik „rinkis mažiausią modelį“. Gerai suformuotos užklausos, caching, retrieval‑augmented sprendimai su embedding paieška, kvantizacija – visi šie metodai mažina kaštus ir tampa kritiški, kai pasiūla ribota.

## 24:11 Ką dabar daro aštriausi CTO

Pasaulinė inferencijos krizė nėra prognozė – tai esamų sąlygų stebėjimas ir tai, kas jau „ant slenksčio“. Paklausos kreivė yra eksponentinė, pasiūlos kreivė plokščia, o atotrūkis artimiausius kelerius metus tik didės. Veiksmų planas gana aiškus:

- užsitikrinti pajėgumus dabar
- kurti routing sluoksnį, leidžiantį skirstyti darbo krūvius ir pasirinkti modelius
- įrangą traktuoti kaip vartojamą
- investuoti į efektyvumą kaip į konkurencinį pranašumą
- diversifikuoti visą technologinį stack’ą, kad sumažintumėte priklausomybę nuo vieno žaidėjo

Įmonės, kurios šį planą įgyvendins, galės išgyventi krizę ir konkuruoti, kai pasiūla galiausiai stabilizuosis. Tos, kurios dels, bus pajėgumų ribojamos, spaudžiamos kaštų ir pradės atsilikti didžiausiose technologijų lenktynėse istorijoje.

Tai nėra technologinė problema – tai ekonominė transformacija. Ji atskirs laimėtojus nuo pralaimėtojų pagal sprendimus, kuriuos CTO priims per artimiausius 6 mėn. Langas veikti atviras, bet jis greitai užsidarys. Veikti reikia dabar.
