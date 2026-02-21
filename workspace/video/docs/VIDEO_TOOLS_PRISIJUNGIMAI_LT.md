# Video Tools: Info ir Prisijungimai

Data: 2026-02-13
Tikslas: greitai paleisti filmu workflow su isoriniais servisais.

## 1. Naudojami irankiai

- Vaizdo generacija: `Kling` (web)
- Dainos/muzikos generacija: `ACE Studio` (web) arba `ComfyUI + ACE-Step` (lokalus/debesis)
- Montazas: `Adobe Premiere Pro`
- Planavimas/promptai: `ChatGPT/Claude/Gemini` (pagal poreiki)

## 2. Prisijungimu tvarka (rekomenduojama)

1. Susitvarkyti `Kling` paskyra ir billing.
2. Susitvarkyti `ACE Studio` paskyra ir billing.
3. Patikrinti ar `ComfyUI` bus lokaliai ar remote GPU.
4. Tik tada pradeti generuoti shotus/dainas.

## 3. Kur laikyti prisijungimus

- Nelaikyti slaptu raktu siuose `.md` failuose.
- Laikyti password manager (1Password/Bitwarden) arba OS credential store.
- Projekte laikyti tik:
  - paskyros statusa,
  - plano tipa,
  - kreditu logika,
  - technines pastabas.

## 4. Quick setup: Kling

- URL: `https://app.klingai.com/global/`
- Reikia:
  - aktyvi paskyra,
  - mokamas planas (jei reikia didesniu batchu),
  - render quality/config presetas.
- Fiksuoti kiekvienam projektui:
  - planas,
  - kreditai menesiui,
  - kreditai uz 5s/10s renderi.

## 5. Quick setup: ACE Studio

- URL: `https://acestudio.ai/`
- Tinka:
  - AI vokalams,
  - muzikos draftams,
  - balso/personazo testams.
- Fiksuoti:
  - pasirinktas modelis,
  - licencijos/panaudojimo salygos projektui,
  - eksporto formatas (wav/stems).

## 6. Quick setup: ComfyUI + ACE-Step

- ComfyUI docs: `https://docs.comfy.org/`
- ACE-Step repo: `https://github.com/ace-step/ACE-Step`
- Pastaba del tavo laptopo:
  - su `1 GB VRAM` lokalus darbas bus labai ribotas.
  - rekomendacija: naudoti remote GPU, jei reikia rimtos gamybos.

## 7. Projekto prisijungimu sablonas (be slaptu duomenu)

```md
# Projekto prisijungimu busena

## Kling
- Account: [aktyvus/ne]
- Plan: [free/basic/pro]
- Credits/month: [skaicius]
- Credits 5s: [skaicius]
- Credits 10s: [skaicius]
- Notes:

## ACE Studio
- Account: [aktyvus/ne]
- Plan: [free/paid]
- Main voice/model:
- Export format:
- Notes:

## ComfyUI/ACE-Step
- Mode: [local/remote]
- GPU:
- VRAM:
- Workflow file:
- Notes:
```

## 8. Sprendimas dabar (pagal tavo HW)

- Lokaliai:
  - planavimas, promptai, scenarijus, montazas.
- Debesyje:
  - sunki muzikos/voice generacija ir vaizdo renderiai.
- Praktinis derinys:
  - `ACE Studio` dainai/vokalams + `Kling` vaizdui + `Premiere` finalui.
