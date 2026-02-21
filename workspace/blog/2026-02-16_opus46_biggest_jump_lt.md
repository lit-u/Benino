# Claude Opus 4.6: didžiausias AI šuolis, kurį teko analizuoti

**Šaltinis (YouTube):** [https://www.youtube.com/watch?v=JKk77rzOL34](https://www.youtube.com/watch?v=JKk77rzOL34)

Po Claude Opus 4.6 išleidimo AI agentų pajėgumai pasikeitė ne „šiek tiek“, o struktūriškai. Populiari istorija dažnai skamba kaip nuoseklus, nedidelis autonominio kodavimo gerėjimas, tačiau realybė kitokia: 16 agentų dvi savaites be pertraukos kūrė kodą ir pristatė veikiantį C kompiliatorių. Tai jau ne tendencijos linija, o fazinis pokytis.

## 16 agentų per dvi savaites sukūrė C kompiliatorių
Claude Opus 4.6 vėl perrašė agentinio programavimo ribas. Šešiolika Opus 4.6 agentų autonomiškai kodavo dvi savaites iš eilės, be žmogaus, rašančio kodą ranka, ir pateikė pilnai funkcinį C kompiliatorių. Projektas apėmė daugiau nei 100 000 Rust kodo eilučių, geba kompiliuoti Linux branduolį trijose architektūrose, praeina 99% specialaus „torture test“ rinkinio kompiliatoriams, kompiliuoja PostgreSQL ir kitus didelius projektus. Kaina apie 20 000 USD atrodo reikšminga individualiam kūrėjui, bet palyginus su tokio masto žmonių darbo sąnaudomis tai yra labai mažai.

Svarbiausia dinamika: prieš metus autonominis AI kodavimas dažnai sustodavo ties maždaug 30 minučių riba. Dabar turime dvi savaites nepertraukiamo darbo. Dar praėjusią vasarą 7 valandos atrodė įspūdingai. Šuolis nuo 30 minučių iki 2 savaičių per 12 mėnesių nėra „normalus progresas“.

## Nuo 30 minučių iki 2 savaičių per 12 mėnesių
Opus 4.5 pasirodė 2025 m. lapkritį ir tuo metu buvo vienas stipriausių modelių. Po kelių mėnesių išėjo Opus 4.6 su penkis kartus didesniu konteksto langu: nuo 200 000 iki 1 000 000 tokenų. Praktiniu lygiu tai reiškia, kad vienoje sesijoje modelis gali laikyti apie 50 000 kodo eilučių vietoje ankstesnių maždaug 10 000.

Tačiau vien konteksto dydis dar nepaaiškina kokybinio šuolio. Esminė naujovė yra ne tai, kad galima „sukrauti“ daugiau informacijos, o tai, kad modelis daug geriau randa ir panaudoja tai, kas sukrauta.

## Opus 4.6: 5x konteksto lango plėtra
Penkiskart išaugęs kontekstas yra matomiausias skaičius, bet ne svarbiausias. Didesnis langas be gero informacijos „ištraukimo“ duoda ribotą naudą. Jei modelis negali patikimai rasti reikiamos detalės didžiuliame kontekste, realus laimėjimas mažas.

## Tikrasis skaičius: „needle-in-haystack“ atgavimo kokybė
Lūžio tašką geriau nusako „needle-in-haystack“ tipo metrika: kiek patikimai modelis randa tikslinę informaciją dideliame kontekste. Ankstesnės kartos modeliai galėjo priimti didelius kontekstus, bet prastai iš jų išgaudavo tikslų turinį. Opus 4.6 šioje vietoje pagerėjo drastiškai: būtent todėl jis „jaučiasi“ kaip kita klasė.

Tai kritiška kodavime: skirtumas tarp modelio, kuris laiko 50 000 eilučių, ir modelio, kuris 50 000 eilučių kontekste tiksliai orientuojasi, yra milžiniškas. Tai artima tam, kaip dirba vyresnis inžinierius, turintis visos sistemos mentalinį žemėlapį.

## Holistinis kodo suvokimas kaip vyresnio inžinieriaus
Kai modelis vienu metu mato importus, priklausomybes, modulių sąveikas ir architektūrinius kompromisus, jis pereina nuo „failo redagavimo“ prie sisteminio mąstymo. Tokia darbo atmintis ir kryžminis samprotavimas leidžia mažiau „lopyti“, o daugiau projektuoti.

C kompiliatoriaus pavyzdys parodė ir ribą: 100 000 eilučių projektui vis dar reikėjo kelių agentų komandos. Bet dabartine trajektorija šiai ribai artimiausiais ciklais dar labiau traukiantis, vieno agento aprėptis didės.

## Rakuten: AI, valdantis 50 kūrėjų
Rakuten diegė Claude Code ne kaip demonstraciją, o produkcijoje. Opus 4.6 ne tik uždarė dalį užduočių autonomiškai, bet ir priskyrė darbus teisingiems žmonėms tarp 50 kūrėjų komandos per kelis repozitorijų sluoksnius. Tai jau ne vien „kodo rašymas“, o koordinavimo kompetencija: priklausomybių valdymas, maršrutizavimas, eskalavimo taškų atpažinimas.

Tai svarbu ekonomiškai: dalis inžinerinio koordinavimo darbo, kuris iki šiol buvo žmogaus vadovo laukas, tampa automatizuojama. Ne strategija ir ne žmonių ugdymas, bet operacinis triage ir paskirstymas.

## Agentų komandos: hierarchija kaip iškylanti savybė
Opus 4.6 pristatė agentų komandinį darbą kaip realią infrastruktūrą: vedantysis agentas, specialistai posistemėms, tarpusavio žinučių apsikeitimas, bendras užduočių statusas. Tai ne metafora – tai veikimo modelis, panašus į inžinerinę komandą.

Įdomiausia, kad hierarchija čia atsiranda ne kaip kultūrinis pasirinkimas, o kaip koordinavimo būtinybė. Kai daug agentų dirba su sudėtinga užduotimi, neišvengiamai reikia priklausomybių valdymo, specializacijos ir komunikacijos kanalų.

## 500 „zero-day“ pažeidžiamumų aptikta autonomiškai
Kartu su Opus 4.6 buvo parodytas ir saugumo testas: modeliui duoti įrankiai (Python, debuggeriai, fuzzeriai) ir atviro kodo bazė, be konkrečių nurodymų „ieškok pažeidžiamumų“. Rezultatas – daugiau nei 500 anksčiau nežinomų aukšto kritiškumo „zero-day“ pažeidžiamumų.

Svarbi detalė: modelis neapsiribojo vien statine analize, o pats pasirinko eiti per Git istoriją, ieškodamas rizikingų vietų evoliucijoje. Tai rodo ne tik tikrinimą pagal šabloną, bet ir strateginį tyrimo elgesį.

## Skeptikai ir Reddit reakcijos
Kiekvieną naują modelį lydi skepticizmas, ir dalis jo pagrįsta: workflow pokyčiai tikrai gali „sugadinti“ ankstesnius įpročius. Vieni naudotojai vertina 4.6 kaip geresnį kodavime, kiti mini kitokią rašymo elgseną. Tai normalu, nes keičiasi ne tik modelis, bet ir jį supanti agentinė „harness“ logika.

Tačiau skeptiškumas nepaneigia fakto: produkciniai scenarijai keičiasi realiai, o skirtumą labiausiai rodo ne benchmark grafikai, o tai, ką įmonės jau daro su nauja versija.

## Ne inžinieriai, kuriantys programinę įrangą per valandą
Ne techniniams naudotojams pagrindinė naujiena ta, kad AI gali sukurti veikiančius vidinius įrankius labai greitai. Tai nereiškia, kad per valandą atkuriamas pilnas enterprise produktas, bet reiškia, kad „asmeninės programinės įrangos“ sluoksnis tapo praktiškai pasiekiamas.

Tai perkelia darbo modelį: nebe „aš ranka operuoju įrankį“, o „aš nurodau rezultatą, agentas realizuoja“. Kuo aiškesnė intencija ir kokybės kriterijai, tuo didesnė grąža.

## „Vibe working“: aprašai rezultatą, ne procesą
Šiuolaikinis modelis vis dažniau toks: žmogus suformuluoja tikslą ir apribojimus, agentas sukonstruoja kelią. Tai galioja tiek kūrėjams, tiek marketingo, finansų ar operacijų komandoms. Esminis įgūdis slenka nuo „techninio vykdymo“ į „tikslų formulavimą ir vertinimą“.

## Pajamos vienam darbuotojui AI-native įmonėse
AI-native įmonių metrikos rodo, kad pajamos vienam darbuotojui gali būti keliskart didesnės nei tradicinių SaaS modelių. Ne todėl, kad staiga atsirado „superžmonės“, o todėl, kad žmonės orkestruoja agentus, o ne patys atlieka visą vykdymo grandinę.

Organizacinis klausimas tampa ne „ar diegti AI“, o „koks turi būti agentų ir žmonių santykis“ ir „kokiose vietose žmogaus sprendimas lieka kritinis“.

## Vieno žmogaus milijardo dolerių įmonės prognozė
Viešojoje erdvėje jau rimtai svarstoma tikimybė, kad artimiausiu metu atsiras milijardo vertės įmonė su vienu įkūrėju ir didele agentų infrastruktūra. Nepriklausomai nuo to, ar ši konkreti prognozė išsipildys tiksliai, kryptis aiški: ryšys tarp headcount ir output jau lūžęs.

## Trajektorija nuo čia
Jei dabartinė dinamika išliks, autonominis kelių savaičių agentų darbas taps rutina, o ne išimtimi. Tikėtina, kad agentai vis dažniau atliks pilnus aplikacijų ciklus su testais, dokumentacija ir saugumo peržiūromis.

Praktinė išvada:
- Kūrėjams – verta testuoti realius multi-agent scenarijus savo codebase’e.
- Ne kūrėjams – verta pradėti nuo atidėliotų užduočių ir aprašyti aiškų rezultatą.
- Vadovams – metas projektuoti AI-perėjimą kaip žmonių kompetencijų transformaciją, ne vien kaip įrankio pirkimą.

Kas laimi šiame etape? Tie, kurie kiekvieną mėnesį atnaujina savo mentalinį modelį pagal naujausią agentinę realybę, o ne pagal tai, kas veikė prieš ketvirtį.
