# nanobot / CLAUDE.md
> WhatsApp AI botas (Benino ekosistemos dalis)

## Stack
- **Engine:** Python (`nanobot-env` virtualenv)
- **Framework:** nanobot-ai v0.1.4.post4 (`HKUDS/nanobot`)
- **WhatsApp bridge:** Node.js/TypeScript (`src/bridge/`, Baileys)
- **LLM:** OpenRouter `google/gemini-2.0-flash-001` (mokamas, ~6€ kredito)

## Paleidimas (Windows)
```bash
# 1. Bridge pirmas
cd nanobot/src/bridge
npm start

# 2. Gateway (atskirame terminale)
cd nanobot
NO_COLOR=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python -m nanobot gateway
```
**Svarbu:** `&&` PowerShell'e neveikia — naudoti atskirus terminalus.

## Konfigūracija
- **Realus config:** `C:\Users\Herba\.nanobot\config.json` (tai ką `gateway` nuskaito)
- **Projekto config:** `nanobot/config.json` (šablonas, neveikia runtime)
- Modelį keisti: `.nanobot/config.json` → `agents.defaults.model`
- Po modelio keitimo: restart + ištrinti `C:\Users\Herba\.nanobot\sessions\*`

## LLM taisyklės
- **Groq llama** — XML tool call bug, NETINKA agentams. Groq tik Whisper STT.
- **Gemini direct** — key ištrintas (90€ sąskaita)
- **Anthropic** — key yra, bet nėra kreditų
- **OpenRouter** — aktyvus, stabilus

## WhatsApp bridge
- Buildinamas: `cd src/bridge && npm run build`
- Voice transcription: Groq Whisper → 3s debounce → patvirtinimas "ok"/"ne"
- Botas veikia ant atskiro prepaid SIM

## Workspace / Skills
- **Soul:** `workspace/SOUL.md` — boto asmenybė (dinamiškai kraunama)
- **Skills:** `workspace/skills/` — Nanobot skills (NE Claude Code skills)
  - `persona/`, `tts/`, `gtts/`, `reminder/`, `content-digest/` ir kt.
- **Memory:** `workspace/memory/` — Nanobot atminimas

## Struktūra
```
nanobot/
├── nanobot-env/          # Python virtualenv
├── config.json           # Šablonas (ne runtime)
└── src/
    └── bridge/           # WhatsApp Node.js bridge
        ├── src/
        │   └── whatsapp.ts   # Voice transcription čia
        └── package.json
```
