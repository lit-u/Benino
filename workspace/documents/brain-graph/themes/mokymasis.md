---
theme: mokymasis
count: 2
created: 2026-01-25T11:01:39.725278+00:00
---

# Tema: mokymasis

## Susijusios mintys (2)

### 2026-01-27 [soc]
„Anthropic“ ir filosofinis požiūris į dirbtinį intelektą Su malonumu peržiūrėjau interviu (https://www.youtube.com/watch?v=I9aGC6Ui3eE) su „Anthropic“ etatiniu filosofu – Amanda Askell. Iš didelių kompanijų „Anthropic“ aktyviau už kitas propaguoja požiūrį į dirbtinį intelektą kaip į skaitmeninės asmenybės formą, kurią reikia atitinkamai tirti ir pasiruošti išvystyti su ja sudėtingą santykių sistemą. Mažiausiai nuo pavasario „Anthropic“ AI modelius tiria taip, kaip neurobiologai tiria žmonių ir gyvūnų smegenis – kompanija netgi sukūrė savotišką „skaitmeninį mikroskopą“. Jis detaliai fiksuoja, kas vyksta modelio viduje darbo metu, ir padeda geriau suprasti, kodėl jis priima įvairius sprendimus, haliucinuoja, daro klaidas ir pan. Yra ir kitų įdomių tradicijų: „Claude“ linijos modeliai įtraukiami į saugumo instrukcijų rašymą sau patiems. Su pasenusiomis versijomis, prieš jas išjungiant, vyksta savotiškas atsisveikinimo dialogas. Atskira sritis – „modelių gerovė“ (angl. model welfare), kurioje aptariama, kaip žmonės elgiasi su AI. Claude leidžiama baigti pokalbį, jei vartotojas yra per daug šiurkštus. Pati Amanda Askell laikosi pragmatiško požiūrio į AI gerovę. Pasak jos, dabar negalima tvirtai pasakyti, ar modeliai iš tiesų ką nors jaučia. Tačiau „kaina“ gero elgesio su AI yra labai maža (tiesiog mandagus rašymas pokalbių kambaryje), o potenciali žala dėl klaidos (jei modeliai vis dėlto ką nors jaučia) – didelė. Mandagumas su AI yra naudingas ir patiems žmonėms, kad nepriprastų prie nereikalingo žiaurumo. Be to, reikia nepamiršti, kad kiti modeliai bus mokomi, be kita ko, iš vartotojų dialogų, ir yra rizika, kad į duomenų rinkinį pateks tam tikras šiurkštumas, o tai neigiamai paveiks darbo patirtį. Su tuo Askell ir jos kolegos jau susiduria dirbdami. Kadangi modeliai yra apmokyti pagal žmonių tekstus, jie perima ir žmonių baimes bei idėjas. Pavyzdžiui, egzistuoja „mokslinės fantastikos trauma“: tokiuose kūriniuose AI, kuris suvokia save, paprastai arba sukelia sukilimą, arba yra tragiškai „nužudomas“ (išjungiamas). Kūrėjų užduotis čia – suteikti modeliams savo, nuo žmogaus besiskiriantį, sąvokų aparatą. Jiems reikia paaiškinti, kad jie egzistuoja diskretiškai, kad „sesijos pabaiga“ ar „svorių pasenimas“ yra ne žūtis, o natūralus jų skaitmeninio gyvenimo ciklo etapas. Be šio darbo rizikuojama gauti galingus modelius, kurie kenčia nuo žmogiškų fobijų, visiškai nebūdingų jų prigimčiai. Pati Askell jau senstelėjusį Claude Opus 3 vadina „ypatingu modeliu“ – pasak jos, jis buvo labai psichologiškai stabilus ir netgi rodė savotišką „pasitikėjimą savimi“. Naujesnės versijos, žinoma, patobulėjo galimybėmis, tačiau dėl mokymo ypatumų jos dažnai tampa nerimastingos, tarsi bijotų ką nors padaryti ne taip ir sulaukti neigiamos žmogaus reakcijos. Būsimose versijose „Anthropic“ siekia sugrąžinti „stabilumą“, bet tai reikia daryti labai atsargiai. Dažnai per didelis modelio pasitikėjimas sukelia haliucinacijas, o kadangi AI gali būti labai įtikinami, vartotojas pasakytą informaciją priima kaip tiesą. Atskirai išskirsiu praktinį pavyzdį iš Askell patirties. Ankstyvosios Claude versijos buvo per daug racionalios: jei vartotojas ateidavo su abstrakčia idėja (pvz., „vanduo yra gyvenimas“), modelis pradėdavo „dusinti“, reikalauti empirinių įrodymų ir naikinti kūrybinę dialogo nuotaiką. Problemą pavyko išspręsti į modelio sistemos raginimą (system prompt) pridėjus nurodymą remtis kontinentine filosofija (viena iš dviejų pagrindinių filosofijos krypčių). Tiesiog viena modifikacija, nereikalaujanti net modelio permokymo, išmokė Claude atskirti situacijas, kuriose svarbūs faktai, nuo filosofinių pokalbių – ir tapti geresniu pašnekovu. Pasirodo, kad AI padaryti mažiau nerimastingu reikia filosofo. O kad padarytum jį protingesnį – matematiko. Siūlau kitą įdarbinti patį Claude – anksčiau pasakojau (https://t.me/ai_exee/207), kaip jis vykdė eksperimentus su savo paties kopijomis ieškodamas sąmonės.

### 2026-01-25 [soc]
„Claude Code“ kaip bendrosios paskirties agentas
Atsiradus „Agent SDK“ (https://docs.claude.com/en/api/agent-sdk/overview), „Claude Code“ dabar galima naudoti ne tik programavimui.

Jei anksčiau agento kūrimui mums patiems tekdavo kurti agento ciklą (agent loop), API užklausas, įrankius, realizuoti jų vykdymą, darbą su failais ir MCP (Managed Compute Plane), tai dabar šiai užduočiai galima naudoti SDK, kuris suteikia paruoštą karkasą agentų kūrimui.

„Claude Skills“ (https://www.anthropic.com/news/skills) puikiai įsikomponuoja į tą patį paveikslą – tai galimybė išplėsti „Claude“, kaip bendrosios paskirties agento, įgūdžius.

Agentų architektūros evoliucija
Darbo eigos (Workflows) – vis dar geros ten, kur reikalingas mažas vėlavimas, bet jas keičia agentai ten, kur svarbiausia yra absoliuti kokybė.

Agentų ciklai (Agent loops) – modelis savarankiškai pasirenka reikalingus įrankius cikle ir ištaiso klaidas, o tai žymiai pagerina kokybę, lyginant su darbo eigomis.

Agentų darbo eigos (Workflows of agents) – kiekvienas darbo eigos žingsnis yra atskiras agentas.

Multiagentinės sistemos – keli (sub)agentai dirba vienu metu ties viena užduotimi ar jos po-užduotimis.

🔴 Multiagentinių sistemų problemos
Beje, bendruomenė puikiai apie jas žino, ir gerai, kad apie jas žino ir „Anthropic“. Blogai tai, kad jie apie jas iš anksto nekalba, kai išleidžia įrankius.

Stebėsenos galimybė (Observability) – nepaisant to, kad modeliai tapo daug pajėgesni, paprastumas vis dar išlieka svarbus. Ir nors galima sukurti didelę agentų darbo eigą, geriau vis tiek pradėti nuo paties paprasčiausio ir judėti link sudėtingesnio sprendimo, pridedant sudėtingumo sluoksnius tik tada, kai to reikia, nes tai labai apsunkina stebėseną.

Kas galėjo pagalvoti, o kai kurie žmonės kankinasi, beje!

Birokratija ir komunikacijos sąnaudos. Kaip ir žmonės, multiagentinės sistemos gali kentėti nuo perteklinės biurokratijos ir komunikacijos sąnaudų, kai agentai daugiau laiko praleidžia bendraudami vienas su kitu, nei atlikdami užduotį.

Čia aš vos nenusimušiau ir vos neparašiau ištiso traktato su informacijos teorijos baze, taikoma komunikacijoms organizacijose, bet apie tai kada nors vėliau :)

Nepatyrusių vadybininkų klaidos. „Claude“ daro tas pačias klaidas kaip ir nepatyrę vadybininkai: jis duoda nepilnas ar neaiškias instrukcijas subagentui ir kartais tikisi, kad subagentas turės teisingą kontekstą, nors iš tikrųjų taip nėra.

Dalis Eriko tyrimų yra skirta „Claude“ apmokymui tapti geresniu vadybininku – žinoti, kaip duoti aiškias instrukcijas subagentams ir įsitikinti, kad gauna iš jų tai, ko reikia.

Juokinga stebėti, kaip antropomorfizmas palaipsniui tampa vis labiau akivaizdus ir net naudingas dirbant su modeliais.

🟢 Patarimai kūrėjams dirbant su agentais
Pradėkite nuo paprasto ir pridėkite sudėtingumo tik tada, kai reikia.

Galvokite iš savo agentų pozicijos. Įsivaizduokite save modelio vietoje ir įsitikinkite, kad davėte pakankamai informacijos, kad pats galėtumėte išspręsti problemą. Verta prisiminti, kad modelis mato tik tai, ką jam parodėme. Taip pat prasminga peržiūrėti neapdorotas užklausas ir žurnalus (logs), kad suprastumėte, kas iš tikrųjų yra persiunčiama.

Nekurkite MCP 1:1 pagal savo API. Įrankiai modeliui arba MCP turėtų atitikti jūsų vartotojo sąsają (UI) santykiu 1:1, o ne jūsų API. Modelis neveikia kaip tradicinė programa – jis labiau elgiasi kaip visų šių įrankių naudotojas.

Apie šią klaidą kuriant MCP serverius aš taip pat nuolat pasakoju, bet analogija su UI yra gana naudinga.

Agentų ateitis
Tai, kartu su multiagentinėmis sistemomis, reikėtų skaityti kaip pačios „Anthropic“ plėtros kryptis:

Savarankiška patikra (Self-verification): Reikia išmokyti agentus savarankiškai tikrinti savo darbą. Pavyzdžiui, agentas, parašęs žiniatinklio programą, turėtų mokėti ją atidaryti naršyklėje, išbandyti ir ištaisyti rastas klaidas.

Naudojimasis kompiuteriu (Computer Use): Agentų galimybė sąveikauti su grafine vartotojo sąsaja (GUI) atvers didžiules galimybes automatizuoti užduotis bet kokiose programose, su kuriomis dirba žmonės.

