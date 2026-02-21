# CLAUDE.md - Benino & Agent Network Project Guide

## 🌍 Overview
**Benino** is an AI-driven ecosystem combining a WhatsApp bot (**Nanobot**) and a Web Platform (**Agent Network**).
- **Root:** `d:\_PAL\benino`
- **Nanobot:** `d:\_PAL\benino\nanobot` (Python/Baileys)
- **Web App:** `d:\_PAL\benino\agent-network` (Node.js/Express)
- **Workspace:** `d:\_PAL\benino\workspace` (Shared Brain)

## 🏗️ Architecture

### Nanobot (The Interface)
- **Engine:** Python (`nanobot-env`)
- **Bridge:** Node.js (`src/bridge`) for WhatsApp (Baileys)
- **Brain:** Loads `SOUL.md` dynamically from `workspace/`.
- **Skills:** `workspace/skills/` (e.g., `persona`).
- **Modelis:** Google Gemini (with billing) + Groq fallback

### Agent Network (The Platform)
Project Context: "Pajūrio Tinklas" web app
- **Stack:** Node.js, Express, Supabase (PostgreSQL with RLS).
- **Frontend:** Vanilla JS (ES6 modules).
- **Currency:** "Saulės" (☀️) system with Stripe/Paysera integration.
- **Marketplace:** Hybrid system (Real Listings + Mock Data).
- **Auth:** 3-Level Session-based (L1 Anonymous, L2 Verified, L3 Admin).
- **Second Brain (C2):** Graph-based theme detection (thoughts, notes, themes).

## 💻 Commands

### Nanobot
```bash
# Start Bot (Gateway)
cd nanobot
.\nanobot-env\Scripts\nanobot gateway

# Start WhatsApp Bridge (Required for WhatsApp)
cd nanobot/src/bridge
npm start
```

### Agent Network
```bash
# Start Web Server
cd agent-network
npm start
# Server available at http://localhost:3000

# Automation System (NEW!)
cd agent-network
node sutvarkyk.js [URL]  # Full automation: Analysis → Blog → Themes
```

## 🔄 Git Workflow
The entire `benino` folder is a **Single Monorepo**.
- **Commit:** Stages changes for both Nanobot and Agent Network.
- **Push:** Syncs the whole ecosystem.

## 📝 Key Files & Structure

### Root
- `nanobot/config.json`: API keys and defaults.
- `workspace/personas/*.md`: Personality definitions.

### Agent Network Structure
```
server/
├── agents/           # 9 specialized agents
├── routes/           # API endpoints (auth, listings, blog, soc, brain)
├── services/         # Services (brain-graph, theme-detector)
├── scripts/          # Utility & Admin scripts (admin-helpers.js)
public/
├── modules/          # Frontend modules (ES6 classes)
│   ├── soc-module.js            # SOC feed (Key file)
│   ├── blog-display-module.js   # Blog forms (Key file)
│   └── ...
```

## 🧠 Core Features (Agent Network)

### Authentication
- **L1 (Anonymous):** Basic queries, create listings.
- **L2 (Verified):** Profile, DM, Favorites, Comments.
- **L3 (Admin):** Full control, Pin posts, Brain insights.

### Second Brain (C2 - Graph Awakening)
- **Concept:** Passive graph-based system creating thought nodes from Admin's interactions.
- **Sources:** DM (Full), SOC (Minimal), Blog (Notes).
- **Tech:** Graph service with nodes/edges, theme detection via Lithuanian keywords.
- **Cogni-Vault:** Knowledge structuring via Groq LLM (`/brain.html`).

### Administration
- **Via Claude Code:** CLI based admin operations using `server/scripts/admin-helpers.js`.
- **Natural Language:** "Sukurk blog post'ą...", "Ištrink..."

## ⚙️ Environment Variables
```bash
# Database
SUPABASE_URL=...
SUPABASE_KEY=...

# LLM
GROQ_API_KEY=...
OPENAI_API_KEY=...
GEMINI_API_KEY=...

# External
GOOGLE_PLACES_API_KEY=...
```

## 🛠️ Admin Operations Manual (Claude Code CLI)

Since the visual admin panel was removed, all admin operations for **Agent Network** are performed via natural language commands to Claude. All scripts are located in `server/scripts/admin-helpers.js`.

### Core Commands

#### 📋 Content Management
| Action          | Command Example                                                    |
| --------------- | ------------------------------------------------------------------ |
| **View Blog**   | "Parodyk naujausius 10 blog post'ų"                                |
| **Create Blog** | "Sukurk blog post'ą: Title 'X', Category 'Miestai', Content '...'" |
| **Edit/Tag**    | "Redaguok blog post'ą 'slug': pridėk tagą #renginiai"              |
| **Delete**      | "Ištrink blog post'ą su slug 'senas-postas'"                       |
| **Listings**    | "Parodyk visus aktyvius darbo skelbimus Klaipėdoje"                |
| **Clean Up**    | "Ištrink visus pasibaigusius renginius (expires_at < NOW())"       |

#### 👥 User Management
| Action           | Command Example                           |
| ---------------- | ----------------------------------------- |
| **View Users**   | "Parodyk visus L2+ vartotojus"            |
| **Update Level** | "Pakeisk vartotojo 'Jonas123' level į L3" |
| **Currency**     | "Pridėk 50 Saulių vartotojui 'Maryte'"    |
| **Stats**        | "Parodyk vartotojų augimą per 30 dienų"   |

#### 🛡️ Moderation
| Action      | Command Example                         |
| ----------- | --------------------------------------- |
| **Queue**   | "Parodyk laukiančius moderavimo įrašus" |
| **Approve** | "Patvirtink moderavimo įrašus 123, 125" |
| **Reject**  | "Reject 130 (spam)"                     |

#### 📱 Social Feed (SOC)
| Action       | Command Example                      |
| ------------ | ------------------------------------ |
| **View**     | "Parodyk naujausius 20 SOC post'ų"   |
| **Pin**      | "Pin SOC post ID 789" (Yellow badge) |
| **Channels** | "Sukurk naują channel 'Palanga'"     |

### 📊 Reporting
Instead of console output, ask for HTML reports:
> "Generate HTML report of all users with their stats"

### ⚡ Tips
1. **Be Specific:** "Parodyk naujausius 10..." instead of "Parodyk visus..."
2. **Use Batch:** "Ištrink visus su tag #outdated" instead of one by one.
3. **Verify:** "Show me expired events" -> "Ok, delete them".

## 🧪 E2E Testing (Playwright)

**Location:** `agent-network/tests/`
**Config:** `agent-network/playwright.config.cjs`
**Browsers:** Chrome, Firefox, Safari (all 3)

### Existing Tests
| Test | What it checks |
|------|---------------|
| `example.spec.js` | Homepage loads, title "Pajūrio Portalas" |
| `blog.spec.js` | Blog list opens, posts load |
| `create-listing.spec.js` | Listing creation via form |
| `watchdog/auth.spec.js` | Authentication flow |

### Commands
```bash
cd agent-network
npx playwright test                    # Run all tests
npx playwright test --ui               # Visual UI mode
npx playwright test blog.spec.js       # Single test
npx playwright show-report             # View last HTML report
```

**Note:** Server must be running on `localhost:3000` (auto-starts if not).

## 📚 Related Documentation
- `workspace/MEMORY.md`: System memory and Cogni-Vault docs.
- `docs/`: Benino documentation (automations, workflows).

## 🤖 Automation System (NEW!)

### Full Pipeline: "sutvarkyk [URL]"
**One command** → Complete content analysis & publishing

**Location:** `agent-network/sutvarkyk.js`

**Workflow:**
1. **AUTOMATION-1:** Source Analysis + Blog Publishing (~10s)
   - Extract content (YouTube/arXiv/Web)
   - Generate Mokslius (technical) + OldBoy (narrative)
   - Auto-generate tags
   - Auto-detect category
   - Publish to blog (author: OldBoy-RSS)

2. **AUTOMATION-2:** Theme Extraction + Distribution (~15s)
   - AI identifies 2-5 themes
   - Extracts fragments
   - Creates folders dynamically
   - Publishes each theme to blog
   - Updates theme index

**LLM Provider:** Groq (llama-3.3-70b-versatile) - fast & free tier

**Example:**
```bash
cd agent-network
node sutvarkyk.js https://arxiv.org/abs/2602.05514

# Result (27s):
# ✅ 2 full articles (Mokslius + OldBoy)
# ✅ 3 theme extracts
# ✅ 4 blog posts published
# ✅ Categories: AI Valdymas, Technologijos
```

**View Results:**
- RSS Feed: http://localhost:3000/user/@OldBoy-RSS
- Blog: http://localhost:3000/blog

**Documentation:**
- Full guide: `docs/AUTOMATIONS.md`
- Workflow: `docs/PALANGA_WORKFLOW.md`
