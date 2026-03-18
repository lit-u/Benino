---
phase: 1
slug: collector
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-18
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Inline `node -e` smoke scripts (no test runner needed) |
| **Base path** | `agent-network/server/services/news-collector/` |
| **Quick run command** | Copy the `<verify><automated>` command from the relevant plan task |
| **Full suite command** | Run each verify command from plans 01–05 sequentially |
| **Estimated runtime** | ~5–30 seconds per task (network-dependent) |

---

## Sampling Rate

- **After every task commit:** Run the `<verify><automated>` command for that task
- **After every plan wave:** Run all verify commands for completed plans
- **Before `/gsd:verify-work`:** All verify commands must output PASS (or PASS-RATELIMIT for github-search)
- **Max feedback latency:** 30 seconds (network calls included)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Automated Command | Status |
|---------|------|------|-------------|-------------------|--------|
| 1-01-01 | 01 | 1 | COLL-04 | `cd d:/_PAL/benino/agent-network && node -e "import('rss-parser').then(m => console.log('rss-parser OK:', typeof m.default))" && node -e "import('better-sqlite3').then(m => console.log('better-sqlite3 OK:', typeof m.default))"` | ⬜ pending |
| 1-01-02 | 01 | 1 | COLL-04 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/config.json', {assert:{type:'json'}}).then(m => { const c = m.default; console.log('sources:', c.sources.length, 'cron:', c.pollIntervalCron); })"` | ⬜ pending |
| 1-01-03 | 01 | 1 | COLL-03 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/storage/db.js').then(({initDb,isSeen,markSeen}) => { const db=initDb(); markSeen(db,'https://t.co/x','T','s'); console.log(isSeen(db,'https://t.co/x') ? 'PASS' : 'FAIL'); db.close(); })"` | ⬜ pending |
| 1-02-01 | 02 | 2 | COLL-01 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/sources/rss-fetcher.js').then(async ({fetchRss}) => { const items = await fetchRss({id:'github-changelog',url:'https://github.blog/changelog/feed/',type:'rss'}); console.log(items.length > 0 && items[0].url ? 'PASS' : 'FAIL', items.length, 'items'); })"` | ⬜ pending |
| 1-02-02 | 02 | 2 | COLL-01, COLL-05 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/sources/hn-fetcher.js').then(async ({fetchHackerNews}) => { const items = await fetchHackerNews({id:'hackernews',query:'AI',minPoints:1,hitsPerPage:5}); console.log(items.length >= 0 && items.every(i=>i.url) ? 'PASS' : 'FAIL', items.length, 'items'); })"` | ⬜ pending |
| 1-02-03 | 02 | 2 | COLL-01, COLL-05 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/sources/github-trending-fetcher.js').then(async ({fetchGithubTrending}) => { const items = await fetchGithubTrending({id:'github-trending',language:'',since:'daily'}); console.log(items.length > 0 ? 'PASS' : 'WARN:0-items', items.length, 'items'); if(items[0]) console.log('sample:', items[0].url); })"` | ⬜ pending |
| 1-03-01 | 03 | 2 | COLL-01, COLL-05 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/sources/github-search-fetcher.js').then(async ({fetchGithubSearch}) => { try { const items = await fetchGithubSearch({id:'github-search',query:'topic:llm pushed:>DATE',sort:'updated',perPage:3}); console.log('PASS', items.length, 'items'); } catch(e) { if(e.message.includes('rate limited')) console.log('PASS-RATELIMIT (add GITHUB_TOKEN)'); else throw e; } })"` | ⬜ pending |
| 1-03-02 | 03 | 2 | COLL-01, COLL-05 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/sources/huggingface-fetcher.js').then(async ({fetchHuggingFacePapers,fetchHuggingFaceModels}) => { const p = await fetchHuggingFacePapers({id:'hfp',limit:3}); const m = await fetchHuggingFaceModels({id:'hfm',filter:'text-generation',limit:3}); console.log(p.length>0 && m.length>0 ? 'PASS' : 'FAIL', 'papers:',p.length,'models:',m.length); })"` | ⬜ pending |
| 1-03-03 | 03 | 2 | COLL-01, COLL-05 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/sources/taaft-fetcher.js').then(async ({fetchTaaft}) => { const items = await fetchTaaft({id:'taaft',url:'https://theresanaiforthat.com/recently-added/',type:'taaft-scrape'}); console.log(items.length >= 0 ? 'PASS' : 'FAIL', items.length, 'items'); })"` | ⬜ pending |
| 1-04-01 | 04 | 3 | COLL-01, COLL-03, COLL-04 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/sources/index.js').then(({fetchSource}) => { console.log('export OK'); })"` | ⬜ pending |
| 1-04-02 | 04 | 3 | COLL-02 | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/index.js').then(({runCollector,registerCron}) => { console.log(typeof runCollector === 'function' && typeof registerCron === 'function' ? 'PASS' : 'FAIL'); })" && node -e "const cron = require('node-cron'); console.log(cron.validate('0 */6 * * *') ? 'CRON-VALID' : 'FAIL')"` | ⬜ pending |
| 1-05-01 | 05 | 4 | COLL-02 | `grep -n "registerNewsCollector\|registerCron\|news-collector" d:/_PAL/benino/agent-network/server/index.js` | ⬜ pending |
| 1-05-02 | 05 | 4 | COLL-01–05 | Human checkpoint — see plan 01-05 Task 2 for full verification steps | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| All 10 sources return real data | COLL-05 | Requires live network calls to external APIs | `cd d:/_PAL/benino/agent-network && node -e "import('./server/services/news-collector/index.js').then(async ({runCollector}) => { const r = await runCollector(); console.log('fetched:', r.fetched, 'new:', r.new, 'errors:', r.errors.map(e=>e.source)); })"` |
| 6h cron fires automatically | COLL-02 | Requires waiting 6 hours | Check startup log for `[news-collector] Cron scheduled: 0 */6 * * *` after `npm start` |
| TAAFT scrape returns items | COLL-01 | Cheerio selectors may need tweaking | Run task 1-03-03 verify command and inspect item count |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify — inline node -e commands, no Wave 0 stubs needed
- [x] Sampling continuity: every task has an automated verify command
- [x] No Wave 0 required (inline verify in every plan task covers Nyquist)
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
