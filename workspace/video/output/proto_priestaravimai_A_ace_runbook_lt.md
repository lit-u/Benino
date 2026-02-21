# Proto Prieštaravimai A - ACE paleidimo runbook

Data: 2026-02-13
Tikslas: paleisti abi versijas ACE Studio (`A_radio` ir `A_full`).

## 1. Kur registruotis

- Pagrindinis puslapis: `https://acestudio.ai/`
- Account Center (login/logout/sync): `https://acestudio.ai/app/home`
- Registracijos instrukcija: `https://support.acestudio.ai/article/28-how-to-register-for-an-ace-studio-account`

## 2. Registracija (žingsniai)

1. Atidaryk `https://acestudio.ai/app/home`.
2. Pasirink vieną metodą ir jo laikykis:
   - Email + password
   - Google
   - Phone
3. Patvirtink kodą (jei prašo) ir užbaik profilį.
4. Užsirašyk, kuriuo metodu registravaisi.

Pastaba: skirtingi login metodai gali sukurti skirtingas paskyras.

## 3. Įdiegimas (Windows)

1. Atidaryk ACE docs installation:
   - `https://docs.acestudio.ai/getting-started/installation`
2. Atsisiųsk Windows instaliatorių (`For Win`) iš ACE puslapio.
3. Paleisk installerį.
4. Prisijunk su ta pačia paskyra kaip 2 žingsnyje.

Pastabos:
- Reikia interneto ryšio (renderinimas debesyje).
- Tavo laptopui tai tinkama, nes core render vyksta cloud.

## 4. Planas ir kreditai

1. Patikrink kainas:
   - `https://acestudio.ai/pricing/`
2. Patikrink AI Credit taisykles:
   - `https://support.acestudio.ai/article/147-ace-studio-ai-credit`
3. Startui pakanka nemokamo arba žemesnio plano testams.

## 5. Paleidimas: A_radio (03:15)

Naudok failą:
- `workspace/video/output/proto_priestaravimai_A_ace_studio_prompt_lt.md`

Žingsniai:
1. Sukurk naują projektą ACE.
2. Įklijuok `A_radio` promptą (skiltis "1. Song prompt").
3. Įklijuok lyrics (skiltis "2. Lyrics insert").
4. Sugeneruok 3 versijas pagal "Greiti render nustatymai".
5. Pasižymėk geriausią (`v1`, `v2` arba `v3`).
6. Eksportuok:
   - `mix_main.wav`
   - `mix_instrumental.wav`
   - `mix_vocal_stem.wav`

## 6. Paleidimas: A_full (04:10)

Tas pats failas:
- `workspace/video/output/proto_priestaravimai_A_ace_studio_prompt_lt.md`

Žingsniai:
1. Naujas projektas arba to paties projekto kopija.
2. Įklijuok skiltį "1B. Song prompt A_full".
3. Naudok tuos pačius lyrics.
4. Generuok 2-3 versijas (main + darker + cleaner mix).
5. Atrink geriausią ir eksportuok kaip `A_full`.

## 7. Ką daryti jei prisijungė ne į tą paskyrą

1. Eik į `https://acestudio.ai/app/home`
2. Atsijunk ir prisijunk su teisingu metodu.
3. Paspausk "Launch ACE Studio", kad desktop app persisyncintų paskyrą.
4. Nuoroda:
   - `https://support.acestudio.ai/article/148-log-into-wrong-account`

## 8. Minimalus šiandienos tikslas

1. Užregistruoti paskyrą.
2. Paleisti `A_radio`.
3. Išsaugoti 1 geriausią renderį.
4. Tik tada paleisti `A_full`.
