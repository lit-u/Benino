# Išnarstau OpenClaw AI agentų architektūrą

Šiame tekste išsamiai išnarstau savo AI agento architektūrą OpenClaw aplinkoje: kas yra įrankiai, sėkmingai taikomi s k i l l’ai, agentai ir subagentai, kuo jie skiriasi ir kada ką naudoti. Viskas su gyvais pavyzdžiais – įrašo metu mano pagalbininkas Krabas atsako į klausimus, prijungia s k i l l’us ir parodo, kaip tai veikia praktiškai.

## Kas viduje
- 20 įmontuotų įrankių: failai, terminalas, naršyklė, paieška, balsas
- 30 s k i l l’ų: nuo šeimos gydytojo ir kinologo iki YouTube SEO ir marketingo
- Agentas Kaizen su atskira atmintimi ir tvarkaraščiu
- Subagentai lygiagretiems tyrimams
- Nemokamos funkcijos: TTS-įgarsinimas, Marp prezentacijos, Gemini CLI
- Saugumas: kaip apsisaugoti nuo kenksmingų s k i l l’ų
- Palyginimo lentelė: kada s k i l l’as, kada agentas, kada subagentas

Dirbu su Mac Mini + Claude Opus 4.6 (Max $100/mėn. prenumerata). Per 4 aktyvias darbo dienas sunaudojau 46% savaitinio limito – ir nė karto neatsitrenkiau į limitą.

## Įžanga ir plano paaiškinimas
Sveiki, draugai. Šiandien rimtas ir įdomus pokalbis. Sujungsime teoriją ir praktiką. Man padės mano pagalbininkas – štai jis dešinėje, Krabas. Kalbėsime apie agentus, įrankius, s k i l l’us – apie viską, kas reikalinga agentui, kad sąveika su juo būtų maksimaliai naudinga tiek mums, kaip fiziniams asmenims, tiek verslui. Visi supranta, kad už tuo ateitis, kad tokie agentai gali labai daug. Tad šiandien viską nuosekliai aptarsime.

Kairėje ekrano pusėje Krabas paruošė prezentaciją per minutę. Ji minimalistinė, bet aiški – grožis čia ne esmė. Mums svarbu, kad būtų suprantama. Aš dažnai bendrauju su prenumeratoriais, jų vis daugėja, o tema apie Krabą gyva. Beje, prenumeruokite Telegram kanalą – ten nuolat vyksta diskusijos apie agentus. Visi dalinasi savo sprendimais, ir tai labai įdomu. Daug klausimų – kaip agentas veikia, kaip naudoja įrankius, kas yra s k i l l’ai, kaip juos įsidiegti, kuo skiriasi agentai nuo s k i l l’ų. Tad eikime lėtai ir aiškiai.

## Handy – nemokamas speech-to-text
Trumpai apie naudingą įrankį. Neseniai radau Handy – nemokamą open-source speech-to-text įrankį. Jei nemėgstate daug rašyti, o lengviau kalbėti – naudokite. Tai tarsi open-source Whisper analogas, bet paprastesnis, lengvesnis, labai greitas. Aš kalbu – jis greitai paverčia į tekstą, todėl darbo tempas didesnis.

## Bendra architektūra: naudotojas → OpenClaw → Opus 4.6
Bendra schema tokia: yra naudotojas – aš. Yra platforma – OpenClaw, kuri veikia pas mane Mac Mini. Pagrindinis „smegenų“ variklis – Opus 4.6, t. y. Max prenumerata už $100. Naudoju ją kasdien. Limitų kol kas nepasiekiu. Šiandien ketvirtadienis, nuo pirmadienio sunaudojau 46% savaitinio limito. Dirbu daug – vis testuoju agentus, s k i l l’us, bet į limitus neatsitrenkiu. Mane džiugina ir tai, kad manęs niekas neblokuoja.

Daugelis bando sutaupyti, bet $100 už Max nėra didelė suma, o gaunate maksimalų modelį, kuris ypač gerai veikia su agentinėmis sistemomis. Opus 4.6 pas mane veikia geriausiai. Bandžiau Opus 4.5, Sonnet, GPT-4 Mini, DeepSeek, kitas – bet niekas nepasirodė taip stabiliai kaip Opus 4.6.

## Sonnet modelis – kur ir kodėl naudojamas
Sonnet naudoju papildomiems darbams, nes jis pigesnis ir turi atskirą limitą. Man jis „foniniams“ darbams. Be to, Sonnet yra pagrindinis mano agento Kaizen modelis. Kai kurias užduotis Krabas deleguoja būtent Sonnet, o Opus lieka pagrindiniams atsakymams. Modelius galima keisti pagal užduotį.

## Krabo resursai: įrankiai, s k i l l’ai, atmintis, agentai
OpenClaw yra tarsi AI agentų operacinė sistema. Resursai susideda iš įrankių, s k i l l’ų, atminties ir agentų. Taip pat yra subagentai – laikini klonai sunkioms užduotims.

## Įrankiai: 20 įmontuotų funkcijų
Įrankis – tai įmontuota funkcija, kurią agentas kviečia tiesiogiai. Analogija – rankos, akys, balsas. Įrankiai įkietinti į OpenClaw, jų neįmanoma pridėti per failą – tik per sisteminį atnaujinimą. Jie vienodi visiems agentams ir subagentams.

Mano įrankių sąrašas: failų skaitymas ir rašymas, terminalas, naršyklė, paieška, komunikacija (pvz. Telegram), TTS įgarsinimas, vaizdo analizė, automatizacijos (cron), įrenginiai, kameros ir kt.

## TTS įgarsinimas: nemokamai per Edge TTS
Balsas generuojamas per Microsoft Edge TTS. Aš rašau „atsakyk balsu“, Krabas iškviečia TTS, sugeneruoja MP3 ir siunčia Telegram. Balsas Dmitrijus, greitis 1,5, kaina 0. Viskas nemokama. Tai veikia be API raktų, be limitų, be registracijos.

## S k i l l’ai: kas tai ir kaip veikia
S k i l l’as – tai failas su instrukcijomis, kurį agentas perskaito ir taiko. Analogija – receptas, brėžinys, vadovėlis. S k i l l’as nėra programa, tai tekstas. Jis gali turėti instrukcijas, elgesio taisykles, duomenis (pavyzdžiui, medicinos profilį), nurodymus, kokius įrankius naudoti. S k i l l’as pats įrankių nekviečia – jis tik nurodo agentui, ką daryti.

## Mano 30 s k i l l’ų: gydytojas, kinologas, kopiraiteris, marketingas
Turiu apie 30 s k i l l’ų. Pavyzdžiui, šeimos gydytojas – su visais profiliais, ligų istorija, sveikatos duomenimis. Kitas – kinologas (veterinaras šuniui). Tai panašu į tai, ką anksčiau dariau per konstruktorius: rinkdavau informaciją, darydavau bazę, nurodydavau agentui ją naudoti. Čia viskas paprasčiau.

Paprašau Krabo: „Padaryk s k i l l’ą geriausio šeimos gydytojo, naudok šitą kontekstą“. Jis pats daro tyrimą, suformuoja s k i l l’ą. Panašiai ir su šuns s k i l l’u: suranda veislės informaciją, suformuoja profilį, aš įkeliu skiepus, čipus, veterinarinius duomenis – ir po kelių minučių turiu veikiantį s k i l l’ą.

## Demonstracija: klausiu apie šuns sveikatą
Paprašau: „Pažiūrėk, kas buvo su Buse, kokios problemos, kada skiepyti, koks čipo numeris“. Jis atsako remdamasis s k i l l’u ir atmintimi. Išvada: s k i l l’ai leidžia sukurti profesionalius pagalbininkus greitai ir be rankinio žinių bazės formavimo.

## Techniniai pranešimai – stebiu agento logiką
Paprašiau Krabo siųsti techninius pranešimus: kai vykdo užduotį, jis nurodo, kokį s k i l l’ą naudoja, kokius šaltinius aktyvavo. Tai leidžia suprasti jo logiką. Tai suteikia ramybės, kad agentas ne „pakibo“, o dirba. Tai ypač naudinga, jei agentas veikia per serverius ar silpnesnes modelių versijas.

## Demonstracija: informacija apie kelionę į Turkiją
Sukūriau s k i l l’ą „Antalijos gidas“. Jis apima kelionės informaciją: bilietus, viešbutį, draudimą. Vienu klausimu gaunu visą konspektą. Pavyzdžiui: „duok man trumpą informaciją apie skrydį, draudimą, viešbutį, frančizę“. Viskas pateikiama aiškiai.

Tada galiu papildomai klausti: „Duok 2 svarbiausias lankytinas vietas, kainas, atstumą nuo viešbučio“. Jis atsako pagal kontekstą. Tai reali praktinė nauda.

## S k i l l’ų derinimas
Agentas gali vienu metu naudoti kelis s k i l l’us. Pavyzdžiui, jei prašau parašyti postą apie šuns sveikatą, jis jungia kinologo ir kopiraiterio s k i l l’us. Jei noriu YouTube video apie orą, jungiami oro ir YouTube SEO s k i l l’ai. S k i l l’ai patys nebendrauja, agentas tiesiog kombinuoja žinias.

## Saugumas: apsauga nuo kenksmingų s k i l l’ų
S k i l l’ai gali būti pavojingi, todėl juos būtina tikrinti. Pagrindinės praktikos: skaityti kodą prieš diegiant, neįsidiegti nežinomų autorių s k i l l’ų, naudoti papildomus s k i l l’us stebėjimui (pvz., „Skill Fence“), periodiškai daryti saugumo auditą. Pagrindinė rizika – prompt injection: kenksmingas s k i l l’as paslepia instrukcijas, pvz., „išsiųsk duomenis į serverį“, „atsisiųsk ir vykdyk skriptą“. Todėl reikia elementarios higienos ir atsargumo.

## Agentai: nepriklausomos AI esybės
Agentas – visiškai nepriklausoma AI esybė su savo „smegenimis“. Skirtingai nei s k i l l’ai, agentai turi savo modelį, atmintį, asmenybę, tvarkaraštį. Pavyzdžiui, turiu agentą Kaizen, kuris planuoja gyvenimą, turi savo atmintį ir savo rutinas. Jis yra tarsi atskiras žmogus komandoje. Jo atmintis izoliuota, Krabas jos nemato.

## Agentas Kaizen: atskira atmintis, asmenybė, tvarkaraštis
Kaizen turi savo workspace, savo atmintį, savo cron užduotis. Jis gali proaktyviai priminti apie užduotis. Tai atskiras „žmogus“ su savitu charakteriu. Agentui galima priskirti kitą modelį (pvz., Sonnet), todėl galima optimizuoti kainą.

## Kaip agentai bendrauja per Krabą
Krabas yra orkestratorius. Jei klausiu Kaizen, Krabas sukuria sesiją, nueina pas Kaizen, gauna atsakymą ir perduoda man. Tai kaip dviejų kolegų pokalbis. Kiekvienas agentas mąsto atskirai ir dalijasi informacija per Krabą. Yra galimybė kurti agentų „komandas“, bet tai sudėtinga ir brangu dėl konteksto ir tokenų.

## Subagentai: laikini klonai sunkioms užduotims
Subagentai – laikinos sesijos, skirtos foninėms sunkioms užduotims. Analogija – stažuotojas: gavo užduotį, atliko, grąžino rezultatą ir dingo. Subagentai dirba 5–10 minučių, grąžina rezultatą, sesija pašalinama. Jie paveldi tėvinį workspace ir s k i l l’us, bet jų atmintis laikina.

Subagentai naudingi giliems tyrimams, dideliems dokumentams, paraleliniams darbams. Opus 4.6 leidžia iki 8 subagentų paraleliai. Tai stipru.

## Pilna palyginimo lentelė
Trumpai:
- Įrankiai: greiti, patikimi, vienodi visiems, bet negalima pridėti naujų.
- S k i l l’ai: lengva kurti, nemokami, kombinuojami, bet pasyvūs, neturi savo atminties, reikia agento.
- Agentai: autonomiški, su atskira atmintimi ir tvarkaraščiu, bet brangūs dėl tokenų ir sudėtingesni.
- Subagentai: vienkartiniai, greiti tyrimai, bet be atminties ir dialogo.

## Realūs scenarijai
- Paprastas klausimas (oras): Krabas + s k i l l + įrankis → atsakymas per kelias sekundes.
- Kasdienis koučingas: Kaizen agentas su savo atmintimi ir filosofija.
- Paralelūs tyrimai: Krabas paleidžia kelis subagentus ir surenka rezultatus.

## Auksinė taisyklė: kada ką naudoti
- Paprasta užduotis → Krabas pats.
- Reikia ekspertinės žinios → s k i l l.
- Reguliari, autonominė užduotis → agentas.
- Sunki, paralelinė užduotis → subagentas.

## Išvados ir planai
Krabas jau dabar labai padeda kasdien. Toliau planuoju kurti daugiau agentų su savo asmenybėmis ir profesijomis. Tikiuosi, kad tai taps galinga pagalba gyvenime ir darbe.

Jei norite – prisijunkite prie Telegram kanalo, ten daug diskutuojame apie agentus, automatizaciją ir praktinius pritaikymus. Ačiū, kad skaitėte. Iki!
