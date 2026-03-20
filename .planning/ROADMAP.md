# Roadmap: Benino News Analyzer

## Overview

The News Analyzer module is built in four delivery phases that follow the data pipeline: collect raw news, score and classify it, present it for moderation via Telegram, then generate and publish full blog posts. Each phase is a complete, independently verifiable capability that enables the next. The end state is an admin who receives curated AI/tech news cards in Telegram and publishes them as full blog posts with a single button tap.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Collector** - Automated news fetching from 10 sources with deduplication storage
- [x] **Phase 2: Scorer** - Importance scoring engine with type classification and multi-source boost (completed 2026-03-18)
- [x] **Phase 3: Telegram Bot** - Admin moderation interface with Accept/Reject actions (completed 2026-03-18)
- [x] **Phase 4: Writer + Publisher** - LLM blog post generation and Agent Network publish pipeline (completed 2026-03-19)

## Phase Details

### Phase 1: Collector
**Goal**: The system reliably fetches AI/tech news from all 10 configured sources on a schedule and stores only new items
**Depends on**: Nothing (first phase)
**Requirements**: COLL-01, COLL-02, COLL-03, COLL-04, COLL-05
**Success Criteria** (what must be TRUE):
  1. Running the collector manually fetches items from all 10 sources (Anthropic, OpenAI, Google AI, GitHub Blog, HackerNews, GitHub Trending, GitHub Search, HuggingFace Papers, HuggingFace Models, TAAFT) without errors
  2. Running the collector twice on the same data produces no duplicate entries in storage
  3. The 6-hour cron job fires automatically and logs each run
  4. Changing the sources list in config (adding or removing a source) takes effect on the next run without touching code
**Plans**: 5 plans

Plans:
- [x] 01-01-PLAN.md — Bootstrap: install deps, config.json (10 sources), SQLite deduplication layer
- [x] 01-02-PLAN.md — Source fetchers: RSS (4 sources), HackerNews, GitHub Trending
- [x] 01-03-PLAN.md — Source fetchers: GitHub Search, HuggingFace (papers + models), TAAFT scraper
- [x] 01-04-PLAN.md — Collector orchestrator: source dispatcher + runCollector() + registerCron()
- [x] 01-05-PLAN.md — Cron wiring into server/index.js + phase gate verification checkpoint

### Phase 2: Scorer
**Goal**: Every collected news item receives a 0-100 importance score, a type classification, and a pass/fail decision against a configurable threshold
**Depends on**: Phase 1
**Requirements**: SCOR-01, SCOR-02, SCOR-03, SCOR-04, SCOR-05
**Success Criteria** (what must be TRUE):
  1. Every item in storage has a numeric score between 0 and 100 and a type label (breakthrough / release / update / research)
  2. A simulated "GPT-5 launch" item (major model release) scores 70 or above
  3. An item that appears in three different sources scores higher than the same item from one source
  4. Items below the configured threshold are marked as filtered and do not proceed to Telegram
  5. Changing the threshold value in config immediately affects which items pass on the next scoring run
**Plans**: 4 plans

Plans:
- [x] 02-01-PLAN.md — Schema migration (4 new DB columns) + config.json scoring block + test scaffold
- [x] 02-02-PLAN.md — Heuristic scorer (keyword + source baselines) + multi-source Jaccard boost
- [x] 02-03-PLAN.md — LLM scorer (OpenRouter batch) + runScorer() pipeline orchestrator
- [x] 02-04-PLAN.md — Wire runScorer() into runCollector() + end-to-end checkpoint

### Phase 3: Telegram Bot
**Goal**: The admin receives scored news items as interactive Telegram cards and can approve or reject each one with a single button press
**Depends on**: Phase 2
**Requirements**: TG-01, TG-02, TG-03, TG-04, TG-05
**Success Criteria** (what must be TRUE):
  1. After scoring, the admin's Telegram receives a card showing the news title, source, score, and category
  2. Each card displays two inline buttons: Accept and Reject
  3. Pressing Reject marks the item rejected in storage and no further action is taken for that item
  4. Pressing Accept triggers the LLM writer and publisher pipeline for that item
  5. When publishing completes the admin receives a Telegram confirmation message containing the live blog post URL
**Plans**: 3 plans

Plans:
- [ ] 03-01-PLAN.md — DB schema migration (tg_status, tg_message_id) + config telegram block + test scaffold
- [ ] 03-02-PLAN.md — Telegram modules: bot.js, card.js, handlers.js, dispatcher.js + unit tests
- [ ] 03-03-PLAN.md — Wire into server/index.js + stub news route + manual Telegram checkpoint

### Phase 4: Writer + Publisher
**Goal**: An accepted news item is transformed into a full blog post via LLM and published to Agent Network under the OldBoy-RSS author
**Depends on**: Phase 3
**Requirements**: WRIT-01, WRIT-02, WRIT-03, WRIT-04, WRIT-05, PUBL-01, PUBL-02, PUBL-03
**Success Criteria** (what must be TRUE):
  1. An accepted news item produces a complete blog post in Mokslius + OldBoy style with a title, body, auto-generated tags, and an auto-detected category
  2. The published post appears in the Agent Network blog under the author OldBoy-RSS
  3. The post is published directly to Supabase blog_posts using the service key (same pattern as upload_palanga_post.js — OldBoy-RSS is a bot author, not a session user)
  4. The LLM model used is configurable via config without code changes (default: google/gemini-2.0-flash-001)
  5. A short news item (under ~200 words of source content) still produces a coherent post without padding artifacts
**Plans**: 4 plans

Plans:
- [ ] 04-01-PLAN.md — Writer module: news-writer.js (content fetch + dual LLM) + DB migration (writer_status) + config writer block
- [ ] 04-02-PLAN.md — Publisher module: publisher.js (Supabase insert) + news.js route (replace 501 stub with full pipeline)
- [ ] 04-03-PLAN.md — E2E checkpoint: manual accept trigger + human verify blog post live under OldBoy-RSS
- [ ] 04-04-PLAN.md — Gap closure: wire config.json to accept route + Telegram admin confirmation after accept

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Collector | 5/5 | Complete    | 2026-03-18 |
| 2. Scorer | 4/4 | Complete    | 2026-03-18 |
| 3. Telegram Bot | 3/3 | Complete   | 2026-03-18 |
| 4. Writer + Publisher | 4/4 | Complete   | 2026-03-19 |
| 5. Hotel Mini-Website | 3/4 | In Progress|  |

### Phase 5: Hotel Mini-Website — Pajūrio Namelis tipo mini svetainė mažiems apgyvendinimo objektams

**Goal:** Each small accommodation property gets its own mini-website at sekmes.lt/hotel/[slug] with room photos, sea proximity info, availability traffic light, and WhatsApp/email reservation — fully SSR with JSON-LD for AI agents
**Requirements**: HOTEL-01, HOTEL-02, HOTEL-03, HOTEL-04, HOTEL-05, HOTEL-06, HOTEL-07, HOTEL-08
**Success Criteria** (what must be TRUE):
  1. /hotel/:slug returns SSR HTML with hotel name in title and LodgingBusiness JSON-LD schema
  2. Hotel API creates/reads/updates/deletes hotels, rooms, and photos with owner isolation
  3. Room photos upload to Supabase Storage hotel-photos bucket with auto-resize
  4. Admin page at /hotel/:slug/admin is protected (401 without auth) and provides full room management
  5. Availability traffic light shows green/yellow/red based on status and available_from date
  6. QR code endpoint generates downloadable PNG for each room
  7. Reservation form generates WhatsApp deep link (wa.me format) and mailto link
**Depends on:** Phase 4
**Plans:** 4/4 plans complete

Plans:
- [x] 05-00-PLAN.md — Wave 0: Playwright test stubs (hotel.spec.js) for HOTEL-01 through HOTEL-06
- [x] 05-01-PLAN.md — Foundation: DB schema (3 tables) + hotels.js CRUD API + hotel-image-service.js + qrcode install
- [x] 05-02-PLAN.md — Public page: SSR/injectMeta extension + hotel.html + hotel-module.js (gallery, sea proximity, reservation)
- [x] 05-03-PLAN.md — Admin panel: hotel-admin.html + hotel-admin-module.js (room CRUD, drag-drop photos, QR) + checkpoint

### Phase 6: Rezervacijų Sistema — tikros rezervacijos į DB, savininkas gauna el. laišką ir WhatsApp pranešimą apie kiekvieną rezervaciją

**Goal:** Guest submits reservation via form (POST to DB), owner receives email notification, and admin panel shows reservation list with Confirm/Cancel actions
**Requirements**: RES-01, RES-02, RES-03, RES-04, RES-05, RES-06
**Success Criteria** (what must be TRUE):
  1. Reservation form POSTs to /api/hotels/:slug/reservations and saves to hotel_reservations table
  2. Owner receives email notification for each new reservation (via Resend)
  3. Admin panel shows reservation list with status badges (Laukia/Patvirtinta/Atsaukta)
  4. Owner can confirm (pending → confirmed) or cancel (→ cancelled) each reservation
  5. WhatsApp and email links remain as secondary CTA below the submit button
  6. owner_email column added to hotels table; saveable from admin panel
**Depends on:** Phase 5
**Plans:** 2/4 plans executed

Plans:
- [ ] 06-00-PLAN.md — Wave 0: Playwright test stubs (hotel-reservations.spec.js)
- [ ] 06-01-PLAN.md — DB schema (hotel_reservations table + owner_email) + email service method + 3 API routes
- [ ] 06-02-PLAN.md — Frontend form modification: POST instead of WhatsApp redirect + success/error states
- [ ] 06-03-PLAN.md — Admin panel reservations section (list, confirm/cancel, filter tabs, owner_email settings) + checkpoint

### Phase 7: Multi-Hotel — L2 vartotojai gali kurti savo viešbučius per savitarnos panelę

**Goal:** [To be planned]
**Requirements**: TBD
**Depends on:** Phase 6
**Plans:** 0 plans

Plans:
- [ ] TBD (run /gsd:plan-phase 7 to break down)
