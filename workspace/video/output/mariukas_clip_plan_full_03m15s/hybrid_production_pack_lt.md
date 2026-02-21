# Mariukas - Hybrid (B) gamybos paketas

## 1. Tikslas
- Sukurti 03:15 klipą su realiu aktorinių scenų pagrindu.
- AI naudoti fonams, perėjimams ir stilistiniams intarpams.
- Išlaikyti 7 personažus ir daugialokacinį miesto siurrealizmą.

## 2. Gamybos modelis B (Hybrid)
- Realiai filmuojama: 65-75% kadro laiko.
- AI generuojama / compositing: 25-35% (transitionai, fonų plėtiniai, solo montažo intarpai).
- Galutinis montažas: Adobe Premiere (rankinis ritmas + spalva + subtitrai).

## 3. Komanda ir personažai
- Aktoriai: Matas, Ema, Bilietininkė, Mergaitė su aitvaru, Senas laikrodininkas.
- Performance: Būgnininkas Nojus.
- Epizodinis: Naktinis vairuotojas.
- Minimali komanda: Režisierius, operatorius, 1AC, gaffer, garso operatorius, grimeris/stilius, DIT.

## 4. Lokacijų planas (optimizuota)
Filmavimui pakanka 8 realių bazinių lokacijų; likusios gaunamos AI/compositing.
1. Skalbykla (intro)
2. Troleibusas arba autobuso interjeras
3. Tuščias kino teatras
4. Baseino persirengimo kambarys
5. Laikrodininko dirbtuvė
6. Repeticijų kambarys (Nojus)
7. Terminalo tipo erdvė (oro uostas/keltai/degalinė - galima fake'inti viena vieta)
8. Observatorija arba stogas (pabaiga)

## 5. Filmavimo grafikas
### Diena 1 (naratyvas)
- 00:00-00:46 (Intro + I posmelis)
- 00:46-01:25 (Priedainis A)
- 2 kameros setup'ai: CU/MCU ir WS/EWS

### Diena 2 (naratyvas + finale)
- 01:25-02:32 (II posmelis + Priedainis B)
- 02:57-03:15 (Pabaiga)

### Diena 3 (performance + AI plates)
- 02:32-02:57 solo
- Nojaus performance clean background + elementai VFX (aitvaras, bilietas, laikrodžiai, neonai)

## 6. Kadruotės matrica pagal dainą
- 00:00-00:13: EWS, statinis, lėtas startas
- 00:13-00:46: CU/OTS/ECU, trumpesni pjūviai, auganti įtampa
- 00:46-01:25: MCU/CU/WS, aiškūs emociniai akcentai priedainiui
- 01:25-01:54: OTS/CU/MS, nestabilumo jausmas
- 01:54-02:32: WS/EWS + simboliniai intarpai
- 02:32-02:57: montage/tracking, didesnis pjūvio tempas
- 02:57-03:15: WS lock-off, fade out

## 7. AI/VFX sluoksnis
- Background extensions: terminalas, miesto horizontas, observatorijos aplinka.
- Transitionai: reflective match cuts (veidrodis -> langas -> ekranas).
- Solo dalis: 4-6 AI intarpai po 2-4 s.
- Stabilumo taisyklė: tie patys personažų drabužiai/rekvizitai visame klipe.

## 8. Postprodukcijos seka
1. Offline sync ir rough cut (pagal laikus).
2. Performance linijos įpynimas.
3. AI/VFX plates render + compositing.
4. Color grade (vėsi bazė, šiltesnė pabaiga).
5. Tekstai/subtitrai (jei reikalinga).
6. Final master: 4K ir social crop (9:16, 1:1, 16:9).

## 9. Failų struktūra
```text
workspace/video/output/mariukas_hybrid/
  01_prepro/
  02_shoot_day1/
  03_shoot_day2/
  04_performance_day3/
  05_ai_vfx/
  06_edit_premiere/
  07_exports/
```

## 10. Pirmas praktinis veiksmas
- Patvirtink 8 realias lokacijas ir aktorių laiką.
- Po to iš karto galima generuoti konkretų call sheet kiekvienai dienai.
