# Benino Monorepo 🦞

**AI asistentas "Benino" + Pajūrio Tinklas web platforma**

---

## 📁 Projekto struktūra

```
benino/
├── nanobot/                # WhatsApp Nanobot (Python + Baileys bridge)
├── agent-network/          # Pajūrio Tinklas - web platforma (Node.js + Express)
│   ├── server/             # Backend API
│   ├── public/             # Frontend (Vanilla JS)
│   └── sutvarkyk.js        # Content automation pipeline
├── workspace/              # Shared Brain (blog drafts, skills, personas)
│   ├── blog/               # Generated content
│   ├── skills/             # Nanobot skills
│   └── oldboy/             # Prompt templates
├── docs/                   # Benino dokumentacija
├── scripts/                # Admin ir utility skriptai
├── CLAUDE.md               # Pagrindinis projekto vadovas
└── README.md               # Šis failas
```

---

## ⚡ Paleidimas

### Nanobot (WhatsApp botas)
```bash
# 1. Bridge (WhatsApp Baileys)
cd nanobot/src/bridge && npm start

# 2. Gateway (Python - atskiras terminalas)
cd nanobot
NO_COLOR=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python -m nanobot gateway
```

### Agent Network (web platforma)
```bash
cd agent-network
npm start
# http://localhost:3000
```

### Sutvarkyk automation
```bash
cd agent-network
node sutvarkyk.js https://www.youtube.com/watch?v=...
```

---

## 🤖 LLM Konfigūracija

- **Pagrindinis:** Groq (`llama-3.3-70b-versatile`)
- **Atsarginis:** Gemini (`gemini-2.0-flash` su billing)
- **Konfigūracija:** `agent-network/.env` → `GROQ_API_KEY`, `GEMINI_API_KEY`

---

## 📚 Dokumentacija

- [CLAUDE.md](CLAUDE.md) - Pilnas projekto ir admin vadovas
- [docs/AUTOMATIONS.md](docs/AUTOMATIONS.md) - Automation sistema
- [docs/PALANGA_WORKFLOW.md](docs/PALANGA_WORKFLOW.md) - Palanga workflow