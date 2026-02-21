---
title: "Laikas domėtis robotukais"
date: 2026-01-23T09:49:07.172+00:00
category: Tech
tags:
 - robotai
 - technika
 - inteligentas
 - jutikliai
 - duomenys
original_slug: laikas-dometis-robotukais
---

### **GenRobot RealOmni-OpenData: „Embodied AI“ duomenų rinkinio atnaujinimas**
[**RealOmni**](https://huggingface.co/datasets/genrobot2025/10Kh-RealOmin-OpenData) – tai ne šiaip vaizdo įrašų katalogas, kuriame roboto ranka griebia kubelį ant balto stalo. Tai multimodalinis „pasaulis“ su trajektorijomis, anotacijomis ir sąnarių judesių duomenimis.

🟡 **Jutikliai** Vaizdas iš *Fisheye* (žuvies akies) kamerų, IMU (inercinių jutiklių) duomenys, enkoderiai ir taktilinių (lytėjimo) jutiklių parodymai su 1 mm raiška.

🟡 **Scenarijai** Filmuota 3000 realių namų ūkių, jokių sterilių laboratorijų: drabužių lankstymas, batų raištelių užrišimas, indų tvarkymas ir visokio šlamšto rūšiavimas.

🟡 **Bimanual manipulation (Dvirankis valdymas)** Beveik visos užduotys atliekamos dviem rankomis.

🟡 **Long-horizon (Ilgos sekos)** Mediana vaizdo klipo trukmė ~210 sekundžių. Tai reiškia, kad tai nėra tiesiog „paimk-padėk“ veiksmas, o pilnaverčiai procesai: „ištraukti, sulankstyti, padėti į stalčių“.

Naujausiame atnaujinime pridėta 35 tūkst. klipų, orientuotų į įvairiausių daiktų krūvų tvarkymą. Tai būtent ta užduotis, ties kuria „sulužta“ dauguma modelių.

**Šiek tiek skaičių apie visą duomenų rinkinį:**

🟢 **Apimtis (deklaruojama):** 95 TB (plačiau apie tai žemiau). 🟢 **Klipų kiekis:** 1M+ (planuojama). 🟢 **Raiška:** 1600x1296 @ 30fps. 🟢 **Formatas:** .mcap (ROS standartas, viduje suspaustas H.264).

Visas projektas suplanuotas 95 TB apimties ir 10 000 valandų trukmės. Tačiau suskaičiavus tai, kas jau įkelta (Stage 1 + Stage 2), iš viso turime apie 5,4 TB ir ~1600 valandų. Likusią dalį žadama įkelti kaip įmanoma greičiau (*as soon as possible*).

🟡 **Svarbu žinoti:**

**Geležies specifika:** Duomenys surinkti specifiniu *GenDAS* griebtuvu, tad jei jūsų jutiklių masyvas kitoks (arba jo visai nėra), *transfer learning* (mokymosi perkėlimas) gali tapti galvos skausmu. Turtas pritaikytas būtent *GenRobot* techninei įrangai.**Teleoperacija:** Tai vis dar yra teleoperacija. Tai reiškia, kad mes mokome robotą kopijuoti žmogaus-operatoriaus judesius, ir jei operatorius dvejojo ar jam drebėjo rankos – tinklas tai taip pat išmoks.Nepaisant to, tai labai stiprus leidinys tiems, kurie kuria namų robotus. Atvirojo kodo duomenys apie batų raištelių rišimą ir daiktų rūšiavimą yra retenybė.

📌 **Licencija:** CC-BY-NC-SA-4.0 License.

🟡 **Duomenų rinkinys (HuggingFace):** [RealOmni-OpenData](https://huggingface.co/datasets/genrobot2025/10Kh-RealOmin-OpenData) 🖥 **GitHub:** [das-datakit](https://github.com/genrobot-ai/das-datakit)
