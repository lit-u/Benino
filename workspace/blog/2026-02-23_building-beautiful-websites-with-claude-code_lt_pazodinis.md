# Building Beautiful Websites with Claude Code Is Too Easy

Šiandien parodysiu penkis paprastus triukus, kuriuos gali naudoti Claude Code, kad kuriamos svetainės neatrodytų kaip „AI vibe coded“, o jaustųsi profesionalios ir su aiškiu brandu. Ir viską pereisime taip, kad net jei Claude Code dar niekada nenaudojai, viskas bus gerai: šio video pabaigoje galėsi susikurti tikrai gerai atrodančius landing page ir svetaines.

Pirmas dalykas: parsisiųsk Visual Studio Code. Naršyklėje įvesk VS Code ir atsisiųsk savo operacinei sistemai. Čia bus IDE, kuriame naudosime Claude Code. Kai atsidarysi, kairėje eik į Extensions, įrašyk „Claude Code“ ir įdiek plėtinį. Po to tavęs paprašys prisijungti su Anthropic/Claude prenumerata, ir taip, reikia mokamos paskyros. Free plane Claude Code nėra, Pro plane yra, Max plane irgi yra. Pradžiai užtenka Pro, o jei remsiesi į limitus ir statysi svetaines visą dieną, tada verta pereiti į Max.

Kai viską įsidiegsi, pamatysi Claude Code mygtuką viršuje. Paspaudus atsidaro dešinėje agentas, su kuriuo kalbiesi, o kairėje yra failai. Tai panašu į chatą internete, tik čia agentas dirba su realiais projekto failais. Toliau reikia atsidaryti projektą. Explorer skiltyje pasirink „Open Folder“. Jei neturi aplanko, susikurk naują Desktop ar Documents vietoje ir atsidaryk jį. Nuo to taško ir dirbsi su svetaine.

## Hack #0: `claude.md` failas kaip sistemos instrukcija

Pirmas „hackas“ čia numeriuojamas kaip nulis, nes jis yra prielaida visiems kitiems. Tai `claude.md` failas. Kodėl „nulis“? Nes prie jo dažnai teks grįžti net jau padarius kitus žingsnius ir atnaujinti taisykles. `claude.md` mąstyk kaip „system prompt“: prieš darydamas bet kokį veiksmą šiame projekte Claude pirma perskaito tą failą. Todėl jame turi būti trumpos, aiškios taisyklės, kaip dirbti būtent šiame website building projekte.

Failo nereikia perpildyti kontekstu, bet reikia duoti taisykles, kurias Claude kartos kiekvieną kartą: ką daryti, ko nedaryti, koks tikslas. Jei dar nežinai galutinio proceso, gali pradėti ir be jo, bet vėliau vis tiek verta susikurti. Video autorius duoda savo `claude.md` šabloną nemokamoje bendruomenėje.

Markdown sintaksė ten reikalinga tam, kad agentas suprastų struktūrą: kas yra header, subheader, bold, bullet ir pan.

![VS Code + Claude Code diegimo etapas](/uploads/blog/claude-code-hacks/01_vscode_install.png)
![`claude.md` failo paaiškinimas](/uploads/blog/claude-code-hacks/02_claude_md_explained.png)

## Hack #1: Front-end design skill (privaloma)

Toliau eina pirmas techninis triukas: front-end design skill. `claude.md` faile tiesiogiai parašoma taisyklė: „visada invoke front-end design skill prieš rašant bet kokį front-end kodą, kiekvienoje sesijoje, be išimčių“.

Kas yra „skills“? Tai custom instrukcijos markdown formatu. Kai Claude gauna tavo užklausą, jis pirma perskaito `claude.md`, po to pats įsivertina, ar turi bibliotekoje skillą, kuris šiai užduočiai padės. Jei turi, pasiima jį ir dirba su tuo papildomu kontekstu. Jei neturi, remiasi bendromis žiniomis.

Kodėl šis skillas toks svarbus? Nes be jo dažnai gaunasi vidutiniškai atrodantis „AI vibe coded“ dizainas. Su juo išvaizda tampa daug modernesnė ir profesionalesnė. Jį įsidiegti paprasta: paleidi porą komandų, ir skillas tampa globaliai prieinamas visuose būsimuose Claude Code projektuose.

Autorius rodo pavyzdį su labai trumpu promptu „sukurk music player app su front-end design skill“, ir rezultatas jau su animacijomis, dinaminiais elementais bei tvarkingu UI.

![Front-end design skill pavyzdys](/uploads/blog/claude-code-hacks/03_frontend_skill_tweet.png)

Po to jis dar parodo bonus praktiką: susikurti `brand_assets` aplanką ir į jį įdėti logo bei brand guidelines. Tada promptas gali būti labai trumpas: „sukurk modernų, profesionalų landing page AI Automation Society, štai logo ir brand guidelines“. Failus galima pažymėti tiesiogiai su `@` mention, kad Claude tiksliai matytų, ką naudoti.

Rezultatas su vienu sakiniu buvo pilnas vieno puslapio landingas: nav, hero, marquee, stats, about, benefits, testimonials, CTA, animacijos, logo, spalvos, tipografija.

![Pirmas sugeneruotas landingo rezultatas](/uploads/blog/claude-code-hacks/04_first_landing_result.png)

## Hack #2: Screenshot loop

Antras triukas yra screenshot loop. Idėja labai paprasta: AI gerai nuveda kryptimi, bet dažnai reikia daug rankinio „steering“. Screenshot loop leidžia Claude pačiam save koreguoti. Vietoje to, kad pats ranka iteruotum dešimt kartų, Claude padaro screenshot, pamato kas blogai, pataiso, vėl screenshot, vėl pataiso.

Video autorius rodo, kad projekte atsiranda `temporary_screenshots` aplankas, kur kaupiasi kadrai. Iš TODO matyti, kad Claude ne tik parašo kodą ir paleidžia serverį, bet ir daro bent du screenshot review + polish ciklus.

Tai reiškia, kad Claude tikrina, ar jo sukurtas vaizdas realiai geras, o ne tik ar kodas kompiliuojasi.

![Screenshot loop failai projekte](/uploads/blog/claude-code-hacks/05_screenshot_loop_folder.png)

## Hack #3: Klonavimas iš kitų svetainių kaip inspiracijos

Trečias triukas: naudoti kitų svetainių dizainą kaip referenciją ir liepti Claude pastatyti „clone“. Darbo eiga:

1. Surandi referencinę svetainę (pvz. Dribbble, Godly, Awwwards ir pan.).
2. Pasidarai pilną puslapio screenshot (DevTools -> Capture full size screenshot).
3. Nukopijuoji pagrindinį stiliaus kodą iš Elements/Styles.
4. Duodi Claude: „štai screenshot + style, pastatyk kloną“.

Tada Claude su screenshot loop lygina savo rezultatą su referencija: analizuoja sekcijomis, randa neatitikimus, taiso, kartoja.

Čia ir yra momentas, kur „sunkioji“ dalis užtrunka ilgiau: kai kuri iš nulio ir dar klonuoji pagal referenciją. Bet kai jau turi veikiančią versiją, mažos korekcijos vyksta greitai.

Autorius dar paaiškina bypass permissions režimą VS Code nustatymuose (`Allow dangerously skip permissions`): jis spartina darbą, nes Claude nestoja dėl kiekvieno leidimo, bet techniškai tai rizikinga, nes agentas gali paleisti komandas be rankinio patvirtinimo. Praktikoje jis sako problemų neturėjęs, nes niekada nepalieka agento dirbti per naktį be priežiūros.

![Inspiracijos svetainės pasirinkimas](/uploads/blog/claude-code-hacks/06_clone_reference_sites.png)
![Claude TODO su clone peržiūros ciklais](/uploads/blog/claude-code-hacks/07_clone_todo_review.png)

Po clone sukūrimo autorius padaro antrą žingsnį: „perkelk mūsų brand spalvas, logo ir copy į ką tik sukurtą kloną“. Rezultatas išlieka arti referencinio layout, bet jau tampa tavo brando puslapiu.

![Klonas po brandingo pritaikymo](/uploads/blog/claude-code-hacks/08_branded_clone_result.png)

## Hack #4: Individualūs komponentai

Kai bazinė svetainė jau „jaučiasi gerai“, ketvirtas triukas yra nebeklonuoti visų puslapių, o imti atskirus komponentus iš specializuotų bibliotekų, pvz. `21st.dev`: backgroundai, mygtukai, shaderiai, hover efektai, hero elementai.

Procesas toks:

1. Išsirink komponentą (pvz. hero background).
2. Nukopijuok komponento promptą/kodą.
3. Duok Claude tikslinę instrukciją, kur įterpti komponentą.
4. Iteruok pagal rezultatą.

Svarbi detalė: su dinaminėmis animacijomis screenshot loop kartais kenkia, nes screenshotas „nepagavo“ teisingo kadro ir Claude pradeda overengineerinti begaliniuose taisymo cikluose. Tokiu atveju verta aiškiai parašyti: „šioje užduotyje screenshot compare nenaudok, tiesiog įdėk kodą, o korekcijas duosiu ranka“.

Autorius tai ir padaro: pirmas rezultatas su backgroundu pasirodo per „triukšmingas“ ir „pixelated“, tada jis padiktuoja labai konkretų feedback:

- per daug blaško;
- hero tekstą sunku skaityti;
- reikia geresnio kontrasto;
- „earn more“ spalva netinka;
- fonas turi būti švaresnis ir profesionalesnis.

Po šito Claude pataiso, ir rezultatas tampa vizualiai daug geresnis.

![Komponentų šaltinis `21st.dev`](/uploads/blog/claude-code-hacks/09_individual_components_21stdev.png)

## Deploy į GitHub + Vercel

Kai lokalus variantas tenkina, reikia perkelti į gyvą domeną. Video pateikiama paprasta schema:

- Claude Code: lokali failų sistema ir kodas.
- GitHub: versijų kontrolė ir repo cloud’e.
- Vercel: deployment į live svetainę.

Srautas: pakeitimai commit’inami/push’inami į GitHub, Vercel automatiškai pasiima naują commit ir perdeployina live versiją.

Autorius parodo rankinę eigą:

1. GitHub susikuri repo.
2. Claude paprašai pushinti projektą į tą repo (su auth).
3. Vercel importini tą GitHub repo.
4. Deploy.
5. Gauni viešą `.vercel.app` URL.
6. Vėliau prijungi savo custom domeną per Vercel Domains ir DNS instrukcijas.

![GitHub + Vercel pipeline schema](/uploads/blog/claude-code-hacks/10_github_vercel_pipeline_slide.png)
![Vercel deploy ir live adresas](/uploads/blog/claude-code-hacks/11_vercel_live_domain.png)

Labai svarbi praktika: pakeitimus pirmiau testuoti local hoste, o į GitHub pushinti tik tada, kai aiškiai patvirtini, kad rezultatas geras. Priešingu atveju automatinis Vercel deploy iškart išstumia blogą versiją į live.

Autorius parodo mini pavyzdį:

- paprašo Claude pagerinti „Join the community“ mygtuką;
- nurodo „nepushinti į GitHub, kol nepasakysiu“;
- lokaliai patikrina rezultatą;
- kai tinka, duoda komandą pushinti;
- GitHub atsiranda naujas commit;
- Vercel pagauna commit ir live svetainėje matosi naujas mygtuko efektas.

![Commit -> Vercel auto deploy rezultatas](/uploads/blog/claude-code-hacks/12_commit_and_deploy.png)

## Pabaiga

Video pabaigoje autorius susumuoja penkis triukus:

1. `claude.md` failas kaip projekto taisyklių branduolys.
2. Front-end design skill (beveik „must have“).
3. Screenshot loop su saikingu naudojimu.
4. Klonavimas iš inspiracijos svetainių.
5. Individualių komponentų įterpimas ir iteracija.

Po to lieka tik nuoseklus šlifavimas: tekstų korekcijos, nuotraukos, CTA nuorodos, smulkios animacijos ir UX detalės.

Jis dar primena, kad `claude.md` failą duoda nemokamai savo bendruomenėje, o kas nori giliau į Claude Code, AI automatizacijas ir agentūrų kūrimą, kviečia į mokamą bendruomenę su kursu ir papildomu turiniu.

Ir klasikinis uždarymas: jei video patiko ar išmokai kažką naujo, uždėk like, ačiū, kad žiūrėjai iki galo, ir iki kito video.
