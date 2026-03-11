# Sistemos Architektūra

## Nanobot Stack

```
Gateway (Python)          ws://localhost:3001 ← Bridge (Node.js/Baileys)
  └── nanobot-env             WhatsApp kanalas
  └── ContextBuilder          Sukuria system prompt kiekvienam žinutei
  └── MemoryStore             memory/MEMORY.md + memory/YYYY-MM-DD.md
  └── SkillsLoader            workspace/skills/*/SKILL.md
  └── CronTool                Scheduled tasks
  └── ExecTool                Shell komandos
```

**Config:** `C:\Users\Herba\.nanobot\config.json` (nuskaitomas TIK startup)
**Workspace:** `d:\_PAL\benino\workspace\`
**Versija:** nanobot-ai v0.1.3.post6

## Failo Įkėlimo Tvarka (kiekvienai žinutei)

```
System Prompt =
  [1] Nanobot identity (hardcoded)
  [2] AGENTS.md → SOUL.md → USER.md → TOOLS.md → IDENTITY.md  (BOOTSTRAP_FILES)
  [3] memory/MEMORY.md + memory/YYYY-MM-DD.md  (MemoryStore)
  [4] always: true skills (pilnas turinys inline)
  [5] Kitų skills summary (XML, agent naudoja read_file kai reikia)
  [6] Pokalbio istorija
  [7] Dabartinė žinutė
```

## Skills Katalogas

| Skill | Tipas | always |
|-------|-------|--------|
| reminder | Workflow | true |
| persona | Role | true (implied) |
| content-digest | Workflow | false |
| video-pipeline | Workflow | false |
| tts | Tool | false |
| email-admin | Role+Workflow | false |
| summarize | Workflow | false |
| video-automatizacija | Workflow | false |
| google-workspace | Tool | false |
| agentforge | Hybrid | false |

## Agent Network Stack

```
Node.js + Express (port 3000)
  └── Supabase PostgreSQL (RLS)
  └── Frontend: Vanilla JS ES6 modules
  └── Auth: 3-Level (L1 Anon, L2 Verified, L3 Admin)
  └── Currency: Saulės (☀️) + Stripe/Paysera
  └── Second Brain (C2): Graph + Theme detection
  └── Groq LLM (llama-3.3-70b-versatile)

Git: github.com/Lithuania-U/sekmes.lt (submodule)
Deploy: Vercel (auto-deploy on push to main)
```

## AgentForge Atminties 4 Lygiai

```
L1 Kontekstinis  ← Dabartinė sesija (pokalbio istorija)
L2 Dienos        ← memory/YYYY-MM-DD.md (auto-load)
L3 Ilgalaikė     ← memory/MEMORY.md (auto-load)
L4 Tapatybė      ← AGENTS.md + SOUL.md + USER.md + TOOLS.md + IDENTITY.md (auto-load)
```

## Konteksto Ribos

- Groq llama-3.3-70b-versatile: ~128k tokens
- Bootstrap failai: ~1,500 tokens (~1.2% window)
- Po compaction: IDENTITY.md + BOOTSTRAP.md + handoff.md = 95% atkūrimas
