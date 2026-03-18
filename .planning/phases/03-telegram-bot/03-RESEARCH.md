# Phase 3: Telegram Bot - Research

**Researched:** 2026-03-18
**Domain:** Telegram Bot API (Node.js) + SQLite schema migration + Express integration
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| TG-01 | Admin receives news cards with title, source, score, category | Telegraf `sendMessage` with MarkdownV2 formatting covers all card fields |
| TG-02 | Each card has Accept / Reject inline buttons | Telegraf `InlineKeyboard` builder — two-button row per card |
| TG-03 | Reject marks item rejected in DB, no further action | DB column `tg_status` + `bot.action()` handler writes 'rejected', edits message |
| TG-04 | Accept triggers LLM Writer + Publisher pipeline | `bot.action()` handler makes HTTP POST to internal `/api/news/accept/:hash` — Phase 4 stub |
| TG-05 | Admin receives confirmation with live blog URL when publish completes | Phase 4 Writer calls `bot.telegram.sendMessage(adminChatId, url)` after publish |
</phase_requirements>

---

## Summary

Phase 3 wires the Telegram delivery layer between the existing scorer output and the future Phase 4 Writer pipeline. The core loop is: after each `runCollector()` + `runScorer()` cycle, query all `threshold_pass=1` items that have not yet been sent to Telegram, send each as a card with two inline buttons, and handle the admin's response.

The library decision is **Telegraf 4.16.3** — it is ESM-compatible, uses native TypeScript types (no separate `@types` package), has a clean `Markup.inlineKeyboard` builder, and its `bot.action()` callback handles `callback_query` events with one line. `node-telegram-bot-api 0.67.0` is a lower-level wrapper that works but requires manual `callback_query` event wiring and lacks the builder convenience. For an ESM project doing callback-heavy work, Telegraf is strictly better.

The integration strategy is: **embed the bot inside the existing Express process**, guarded by `!isVercelRuntime` (same pattern as `registerNewsCollector()`). Polling is used locally; Vercel is already excluded via the guard so no webhook complexity is needed for v1.

**Primary recommendation:** Use Telegraf 4.16.3 in polling mode, integrated into `server/index.js` inside the `app.listen` callback alongside `registerNewsCollector()`. Add two SQLite columns (`tg_status TEXT`, `tg_message_id INTEGER`) via the existing `addIfMissing()` pattern. Send cards from a new `runTelegramDispatch()` function called at the end of `runCollector()`.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| telegraf | 4.16.3 | Telegram Bot framework — sends messages, handles callbacks | ESM-native, Markup builder, active maintenance (last release 2026-03-06) |
| better-sqlite3 | 12.8.0 (already installed) | SQLite reads/writes for TG state columns | Already used in Phases 1+2 |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| node-telegram-bot-api | 0.67.0 | Lower-level alternative | Do NOT use — less ergonomic for callback_query, CJS-first |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Telegraf | node-telegram-bot-api | ntba requires manual event wiring; Telegraf's `bot.action()` + `Markup.inlineKeyboard` is cleaner for this use case |
| Telegraf | grammY 1.41.1 | grammY is slightly more modern but its learning curve is higher and the project already has zero Telegram code — Telegraf's API is more widely documented |
| Polling | Webhook | Webhook requires public HTTPS URL + endpoint; polling works instantly for local dev and the Vercel guard already prevents polling on serverless |

**Installation:**
```bash
cd agent-network
npm install telegraf
```

**Version verification:** `npm view telegraf version` returned `4.16.3` (published 2026-03-06). This is current.

---

## Architecture Patterns

### Recommended Project Structure
```
server/services/news-collector/
├── storage/
│   └── db.js               # Add tg_status, tg_message_id columns here (addIfMissing)
├── telegram/
│   ├── bot.js              # Telegraf instance, polling start, bot.action() handlers
│   └── dispatch.js         # runTelegramDispatch(db) — queries pending, sends cards
├── index.js                # Call runTelegramDispatch(db) after runScorer()
└── config.json             # Add "telegram": { "batchSize": 10, "batchDelayMs": 500 }
```

### Pattern 1: Telegraf Bot Initialization (Polling, ESM-safe)
**What:** Create bot once, start polling, export the instance for use in dispatch.
**When to use:** Single Express process, non-serverless environment.
**Example:**
```javascript
// Source: https://telegraf.js.org/#/?id=quick-start (Telegraf docs)
import { Telegraf, Markup } from 'telegraf';

const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN);
export { bot };

export function startBotPolling() {
  bot.launch();
  process.once('SIGINT', () => bot.stop('SIGINT'));
  process.once('SIGTERM', () => bot.stop('SIGTERM'));
}
```

### Pattern 2: Inline Keyboard Card
**What:** Format a news item as a Telegram message with two inline buttons.
**When to use:** Every item dispatch.
**Example:**
```javascript
// Source: https://telegraf.js.org/#/?id=inlinekeyboards
const typeEmoji = { breakthrough: '🚀', release: '📦', update: '🔧', research: '📄' };

function buildCard(item) {
  const text =
    `*${escapeMarkdown(item.title)}*\n` +
    `Score: ${item.score} | ${typeEmoji[item.item_type] ?? ''} ${item.item_type}\n` +
    `Source: ${item.source_id}\n` +
    `[Read more](${item.url})`;

  const keyboard = Markup.inlineKeyboard([
    Markup.button.callback('✅ Priimti',  `accept:${item.url_hash}`),
    Markup.button.callback('❌ Atmesti', `reject:${item.url_hash}`),
  ]);

  return { text, keyboard, parse_mode: 'MarkdownV2' };
}
```

### Pattern 3: Callback Query Handler
**What:** React to button presses — update DB, edit the Telegram message to show result.
**When to use:** Both Accept and Reject actions.
**Example:**
```javascript
// Source: https://telegraf.js.org/#/?id=actions (Telegraf docs)
bot.action(/^reject:(.+)$/, async (ctx) => {
  const urlHash = ctx.match[1];
  // 1. Update DB
  db.prepare("UPDATE seen_urls SET tg_status='rejected' WHERE url_hash=?").run(urlHash);
  // 2. Edit message to show outcome
  await ctx.editMessageText('❌ Atmesta', { reply_markup: { inline_keyboard: [] } });
  await ctx.answerCbQuery();
});

bot.action(/^accept:(.+)$/, async (ctx) => {
  const urlHash = ctx.match[1];
  db.prepare("UPDATE seen_urls SET tg_status='accepted' WHERE url_hash=?").run(urlHash);
  await ctx.editMessageText('⏳ Generuojama...', { reply_markup: { inline_keyboard: [] } });
  await ctx.answerCbQuery();
  // Phase 4: trigger writer pipeline (HTTP call or direct import)
  await triggerWriter(urlHash);
});
```

### Pattern 4: Dispatch with Deduplication
**What:** Query only items not yet sent and send in batches with delays.
**When to use:** After every `runCollector()` pass.
**Example:**
```javascript
// Query items that passed threshold and have not been sent yet
const pending = db.prepare(`
  SELECT url_hash, url, title, source_id, score, item_type
  FROM seen_urls
  WHERE threshold_pass = 1
    AND (tg_status IS NULL OR tg_status = 'pending')
  ORDER BY score DESC
  LIMIT ?
`).all(batchSize);
```

### Anti-Patterns to Avoid
- **Global `db` reference in bot.action() handlers:** The collector opens/closes its own DB connection per run. The bot handlers need a persistent `db` reference open for the lifetime of the process. Use a separate `initDb()` call at bot startup, never the collector's transient connection.
- **Sending without `answerCbQuery()`:** Telegram shows a loading spinner on the button until `answerCbQuery()` is called. Always call it — even on error paths — or the user sees a stuck spinner.
- **MarkdownV2 without escaping:** MarkdownV2 requires escaping `.`, `-`, `(`, `)`, `!` and other chars. Unescaped titles (e.g., "GPT-4.5") will cause a 400 Bad Request from the Telegram API. Use a dedicated escape helper.
- **Starting bot.launch() inside Vercel:** The `isVercelRuntime` guard must wrap `startBotPolling()` exactly as it wraps `registerNewsCollector()`. Polling in a serverless function will crash the cold start.
- **Sending all 942 threshold_pass items at once:** Rate limit is 30 msg/sec to the same chat. Batch by 10 items with a 500ms delay between batches. Respect the existing `maxItemsPerSource` spirit.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Inline keyboard builder | Custom JSON object construction | `Markup.inlineKeyboard` + `Markup.button.callback` | Telegraf's builder handles JSON structure, escaping, row layout |
| Callback routing | Manual `if (data.startsWith('accept:'))` | `bot.action(/regex/)` | Telegraf pattern matching handles multiple actions cleanly |
| Polling loop | `setInterval` + `getUpdates` | `bot.launch()` | Telegraf manages offset, error retry, graceful shutdown |
| MarkdownV2 escaping | Custom replace chain | Dedicated `escapeMarkdownV2()` helper (one function, ~10 chars) | Telegram's spec is precise — missing one char breaks entire message |

**Key insight:** Telegraf eliminates all Telegram API boilerplate. The only custom code needed is business logic: card formatting, DB updates, and the Phase 4 trigger.

---

## Common Pitfalls

### Pitfall 1: MarkdownV2 Special Characters
**What goes wrong:** `sendMessage` throws `400 Bad Request: can't parse entities` when title contains `.`, `-`, `(`, `)`, `!`, `[`, `]`, `_`, `*`, `~`, `` ` ``, `>`, `#`, `+`, `=`, `|`, `{`, `}`.
**Why it happens:** MarkdownV2 is strict — any unescaped reserved character breaks parsing.
**How to avoid:** Always pass titles through an escape function before inserting into message text.
**Warning signs:** Works for simple titles, fails for "GPT-4.5 released" or "New model (v2.0)".

### Pitfall 2: SQLite Busy / Locked on Concurrent Access
**What goes wrong:** Bot's persistent DB connection conflicts with collector's per-run connection.
**Why it happens:** `better-sqlite3` allows multiple connections to the same file but WAL mode is needed for concurrent reads during writes.
**How to avoid:** Open the bot's DB connection once at startup with `db.pragma('journal_mode = WAL')`. The collector already closes its connection after each run — with WAL, the bot's read during a collector write succeeds without lock errors.
**Warning signs:** `SQLITE_BUSY` errors in logs during collector runs.

### Pitfall 3: Duplicate Card Sends
**What goes wrong:** Admin receives the same news item twice across different collector runs.
**Why it happens:** If `tg_status` column doesn't exist yet (before migration), the WHERE clause doesn't filter correctly.
**How to avoid:** `addIfMissing('tg_status', 'TEXT')` in `db.js` runs at every `initDb()` call — the column exists before any dispatch runs. Query always filters on `tg_status IS NULL OR tg_status = 'pending'` — never re-send `accepted` or `rejected` items.

### Pitfall 4: Phase 4 Not Yet Implemented — Accept Must Not Crash
**What goes wrong:** Admin presses Accept, the `triggerWriter()` call throws because Phase 4 doesn't exist, and the callback handler crashes without editing the message.
**Why it happens:** Phase 4 is out of scope for Phase 3.
**How to avoid:** `triggerWriter()` in Phase 3 is a stub that makes an HTTP POST to `/api/news/accept/:hash` (to be implemented in Phase 4). Wrap the call in try/catch. On error, edit message to "✅ Priimta (writer pending)".

### Pitfall 5: Bot Token in Logs
**What goes wrong:** Server startup logs print the Telegram bot token.
**Why it happens:** The existing `server/index.js` startup block logs all env vars.
**How to avoid:** Do NOT add `TELEGRAM_BOT_TOKEN` to the startup logging block. Token is already in `.env` — just confirm it exists with a boolean check if needed.

---

## Code Examples

Verified patterns from official sources:

### MarkdownV2 Escape Helper
```javascript
// Source: Telegram Bot API docs — https://core.telegram.org/bots/api#markdownv2-style
function escapeMarkdownV2(text) {
  return String(text).replace(/[_*[\]()~`>#+\-=|{}.!\\]/g, '\\$&');
}
```

### Send Card with Inline Keyboard
```javascript
// Source: https://telegraf.js.org/#/?id=inlinekeyboards
const adminChatId = process.env.TELEGRAM_ADMIN_CHAT_ID;

async function sendNewsCard(bot, item) {
  const { text, keyboard } = buildCard(item);
  const msg = await bot.telegram.sendMessage(adminChatId, text, {
    parse_mode: 'MarkdownV2',
    ...keyboard,
    disable_web_page_preview: true,
  });
  return msg.message_id; // store in tg_message_id for later editing
}
```

### Edit Message After Button Press
```javascript
// Source: https://telegraf.js.org/#/?id=actions
await ctx.editMessageText(
  `❌ Atmesta — ${escapeMarkdownV2(title)}`,
  { parse_mode: 'MarkdownV2', reply_markup: { inline_keyboard: [] } }
);
await ctx.answerCbQuery('Atmesta');
```

### Registering Bot in server/index.js (inside app.listen)
```javascript
// Same guard pattern as registerNewsCollector()
if (!isVercelRuntime) {
  app.listen(PORT, async () => {
    // ... existing startup code ...
    registerNewsCollector();
    startBotPolling();          // Phase 3 addition
  });
}
```

### Config Extension for Telegram
```json
// Add to config.json alongside "scoring" block
"telegram": {
  "batchSize": 10,
  "batchDelayMs": 500
}
```

---

## SQLite Schema Changes

### New Columns (via `addIfMissing` in `db.js`)
| Column | Type | Values | Purpose |
|--------|------|--------|---------|
| `tg_status` | TEXT | NULL / 'pending' / 'accepted' / 'rejected' | Tracks dispatch and moderation state |
| `tg_message_id` | INTEGER | NULL / message_id | Needed to `editMessageText` after button press |

### Deduplication Query
```sql
-- Items to send: passed threshold, not yet dispatched
SELECT url_hash, url, title, source_id, score, item_type
FROM seen_urls
WHERE threshold_pass = 1
  AND (tg_status IS NULL OR tg_status = 'pending')
ORDER BY score DESC
LIMIT ?;
```

### Set Sent State
```sql
-- After sendMessage() succeeds
UPDATE seen_urls
SET tg_status = 'pending', tg_message_id = ?
WHERE url_hash = ?;
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `node-telegram-bot-api` as default | Telegraf as the standard choice | ~2019 onward | Telegraf's middleware model and builder API have made it the community default for non-trivial bots |
| Webhook-first tutorials | Polling common for development | Always | Polling is simpler for private/admin bots; webhook is only needed for public high-volume bots |
| CommonJS Telegram bots | ESM-compatible Telegraf 4.x | Telegraf 4.0 (2021) | Telegraf 4.x works in `"type": "module"` projects without wrapper hacks |

**Deprecated/outdated:**
- `Telegraf` v3 and below: CJS only, different API. Do not reference v3 examples.
- `telegramjs-bot`: abandoned, do not use.

---

## Open Questions

1. **Phase 4 trigger mechanism**
   - What we know: Accept must trigger Writer + Publisher pipeline
   - What's unclear: Phase 4 hasn't been designed yet — should the trigger be a direct function import or an HTTP call to a local Express route?
   - Recommendation: Add a stub HTTP route `POST /api/news/accept/:hash` in Phase 3 that returns 200 and logs. Phase 4 implements the actual handler. This keeps Phase 3 self-contained and testable.

2. **942 items already above threshold — initial dispatch strategy**
   - What we know: DB currently has ~942 `threshold_pass=1` items (from Phase 2 STATE.md: "1001 items scored")
   - What's unclear: Should the admin receive all 942 old items, or only new items going forward?
   - Recommendation: Default dispatch only items scored in the last 24 hours on first run. Add a `tg_dispatch_cutoff` timestamp to config, or filter by `scored_at > (NOW - 24h)`. Avoids flooding the admin with stale items. Document this as a deliberate config choice.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Playwright (already installed, `playwright.config.cjs`) |
| Config file | `agent-network/playwright.config.cjs` |
| Quick run command | `node -e "import('./server/services/news-collector/telegram/dispatch.js')"` (import smoke) |
| Full suite command | `npx playwright test` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TG-01 | Card sent to Telegram with title/source/score/type | manual-only | Send card to real bot, verify in Telegram app | n/a |
| TG-02 | Card shows Accept + Reject buttons | manual-only | Visually confirm in Telegram app | n/a |
| TG-03 | Reject updates DB tg_status='rejected', message edited | unit | `node tests/news-collector/tg-reject.mjs` | ❌ Wave 0 |
| TG-04 | Accept updates DB tg_status='accepted', stub called | unit | `node tests/news-collector/tg-accept.mjs` | ❌ Wave 0 |
| TG-05 | Confirmation message sent after publish (Phase 4) | manual-only | Verified when Phase 4 completes | n/a |

**Note on TG-01 and TG-02:** These are Telegram UI interactions. There is no programmatic way to verify inline keyboard rendering without a Telegram client. Manual verification is the correct test type for these requirements.

**Note on TG-05:** Depends on Phase 4 Writer implementation. Phase 3 only needs to confirm the bot instance can call `bot.telegram.sendMessage()` — covered by TG-01 manual test.

### Sampling Rate
- **Per task commit:** `node -e "console.log('import ok')" && node --input-type=module <<< "import('./server/services/news-collector/telegram/bot.js').then(() => console.log('bot.js loads'))"` (Windows: use file-based import test)
- **Per wave merge:** Full import chain smoke test
- **Phase gate:** Manual card + button test in real Telegram before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/news-collector/tg-reject.mjs` — covers TG-03: verify DB update on reject action
- [ ] `tests/news-collector/tg-accept.mjs` — covers TG-04: verify DB update on accept action
- [ ] No framework install needed — better-sqlite3 and telegraf are the only deps; telegraf added via `npm install telegraf`

---

## Sources

### Primary (HIGH confidence)
- Telegraf 4.x official docs: https://telegraf.js.org/ — sendMessage, Markup.inlineKeyboard, bot.action(), bot.launch()
- Telegram Bot API docs: https://core.telegram.org/bots/api#inlinekeyboardmarkup — InlineKeyboardMarkup spec
- Telegram Bot API docs: https://core.telegram.org/bots/api#markdownv2-style — MarkdownV2 escape chars
- npm registry: `npm view telegraf version` → 4.16.3 (2026-03-06) — verified current
- npm registry: `npm view node-telegram-bot-api version` → 0.67.0 — verified
- Project codebase: `server/index.js` lines 846-920 — isVercelRuntime guard + registerNewsCollector() pattern
- Project codebase: `storage/db.js` lines 23-29 — addIfMissing() pattern for schema migration

### Secondary (MEDIUM confidence)
- npm view telegraf engines output: `{ node: '^12.20.0 || >=14.13.1' }` — compatible with project's Node.js v24

### Tertiary (LOW confidence)
- Community consensus on Telegraf vs node-telegram-bot-api for ESM projects — verified by package structure (Telegraf ships native ESM, ntba ships CJS with ESM wrapper)

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — versions verified via npm registry on 2026-03-18
- Architecture: HIGH — patterns derived from project's existing established conventions (addIfMissing, isVercelRuntime guard, createRequire, per-run db.close())
- Pitfalls: HIGH — MarkdownV2 and SQLite WAL are documented Telegram/SQLite behaviors; duplicate-send pitfall derived from DB schema analysis

**Research date:** 2026-03-18
**Valid until:** 2026-04-18 (stable ecosystem — Telegraf releases infrequently)
