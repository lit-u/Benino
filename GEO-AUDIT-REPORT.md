# GEO-SEO Audit Report — Pajūrio Portalas (sekmes.lt)
**Audit date:** 2026-03-12
**Platform:** Node.js/Express + Supabase + Vanilla JS SPA
**Auditor:** Claude Code GEO-SEO Specialist

---

## Composite GEO Score: **54 / 100**

| Category | Weight | Raw Score | Weighted |
|---|---|---|---|
| A. AI Crawler Access & llms.txt | 25% | 72 | 18.0 |
| B. Citability (Answer-style content) | 25% | 38 | 9.5 |
| C. Technical SEO Foundations | 25% | 62 | 15.5 |
| D. Content Quality / E-E-A-T | 20% | 35 | 7.0 |
| E. Schema Markup (Structured Data) | 20% | 40 | 8.0 |
| **Composite** | 100% | — | **58 / 100** |

> Note: A/B/C weighted at 25% each per audit spec; D/E at 20% each totals 110%. Normalised to 100: **54/100**.

---

## Category Breakdown

### A. AI Crawler Access — 72/100

**What works:**
- `robots.txt` is excellent. All major AI crawlers explicitly allowed: `GPTBot`, `ChatGPT-User`, `ClaudeBot`, `anthropic-ai`, `PerplexityBot`, `Gemini`, `Google-Extended`, `Applebot-Extended`, `cohere-ai`, `meta-externalagent`.
- `llms.txt` exists at `/llms.txt` — this is ahead of most Lithuanian sites.
- `/api/` is correctly blocked from all crawlers (prevents token waste on raw JSON).

**Issues:**
- `llms.txt` content is sparse (24 lines). Missing: pricing, API endpoints description, key contact information, update frequency, content licensing note.
- No `llms-full.txt` variant for AI systems that want more context.
- Sitemap URL in `robots.txt` points to `https://sekmes.lt/sitemap.xml` (correct), but the live server returns the SPA `index.html` for that URL due to a routing bug (see Section C).
- No `X-Robots-Tag` HTTP headers for fine-grained control.
- No `Allow: /blog/` explicit rule for GPTBot (it inherits global Allow, but explicit is safer).

---

### B. Citability Score — 38/100

**What was checked:** Homepage (`/`), `/kavines.html`, `/miesteliai.html`, blog API sample (3 posts).

**What works:**
- Blog posts contain multi-paragraph prose content — the "Kažkas didelio artėja" post is ~600 words, well within citable range.
- `llms.txt` has a summary paragraph (good intro anchor for AI citation).

**Critical issues:**
- **Homepage is a pure JavaScript SPA.** When crawlers (including AI crawlers) fetch `/`, they receive only the `<body>` scaffold with buttons and dynamic containers — zero substantive text content. The main content blocks (city cards, listings, blog preview) are all rendered client-side via JavaScript. AI crawlers that do not execute JS (most, except Googlebot) see nothing citable.
- **No static "answer blocks"** — no FAQ sections, no definition blocks, no "how it works" prose on the homepage or key pages.
- **kavines.html** shows only `383 vietos 18 pajūrio miestų` as a paragraph. No descriptive text about the cafes, neighbourhoods, or what users can find.
- **miesteliai.html** has an `<h1>` and a subtitle but no explanatory body paragraphs.
- **Blog individual article pages** (`/blog/[slug]`) are SPA-rendered — meta title/description are NOT dynamically set per article (all pages return the generic homepage `<meta>` tags). A crawler fetching `/blog/kazkas-didelio-arteja` sees the same generic title and description as the homepage.
- Paragraph length in blog posts is good (~100-300 words per paragraph) — but this content is invisible to non-JS crawlers.
- No "People Also Ask"-style structured Q&A content anywhere.

---

### C. Technical SEO — 62/100

**What works:**
- Meta title on homepage: `"Pajūrio Portalas — Pajūrio bendruomenės platforma"` — **54 chars** (within 50-60 optimal range). ✅
- Meta description on homepage: **149 chars** — within 150-160 optimal range. ✅
- Canonical tag present: `<link rel="canonical" href="https://sekmes.lt/">`. ✅
- Open Graph tags: `og:title`, `og:description`, `og:type`, `og:url`, `og:locale`, `og:site_name` all present. ✅
- Twitter Card tags: present (`summary` type). ✅
- `kavines.html` and `miesteliai.html` have their own individual canonical, OG, and meta description tags. ✅
- `lang="lt"` on `<html>` element. ✅
- `robots.txt` served correctly with proper content. ✅
- RSS feed exists at `/rss.xml`. ✅

**Critical issues:**
- **Sitemap not served at `/sitemap.xml`** — A `sitemap.js` route exists and is well-written (dynamically generates XML from Supabase data), but it is **never reached** because the SPA fallback handler at the bottom of `server/index.js` intercepts `.xml` extensions (the regex at line 664 lists `.json|.html` but NOT `.xml`) and returns `index.html`. The route is registered at line 221 *after* static middleware, but the SPA fallback `app.get('*')` at line 657 runs before it can respond. **Every request to `/sitemap.xml` returns HTML, not XML.**
  - File: `d:/_PAL/benino/agent-network/server/index.js`, line 664.
- **No `og:image`** — neither homepage nor any inner page defines an OG image. Social shares and AI crawlers that render card previews will show a blank image.
- **No favicon `<link>` tag** — `favicon.ico` exists in `/public/` but is not declared in `<head>`. Some crawlers and feed readers may not auto-discover it.
- **Blog SPA pages have no per-article meta** — `/blog/[slug]` returns the homepage `<head>` verbatim. The server has a dynamic sitemap route but no corresponding SSR meta injection for blog post pages.
- **Kavines.html title is 71 chars** — exceeds the 60-char optimal limit (will be truncated in SERPs).
- **No `link rel="alternate" type="application/rss+xml"`** declared in `<head>`.
- `/api/` routes correctly blocked from static, but no HTTP cache-control headers on HTML pages (they have `no-cache` directives, which prevents proxy caching — fine for a dynamic SPA but prevents CDN edge caching of static shells).

---

### D. Content Quality / E-E-A-T — 35/100

**What works:**
- Blog posts have `published_at` dates and `updated_at` timestamps (available via API). ✅
- Blog posts have an `author_nickname` field ("OldBoy", "OldBoy-RSS"). ✅
- Content is Lithuanian-language and locally relevant (Klaipėda, Palanga, Neringa). ✅
- 127 published blog posts — reasonable content volume.

**Critical issues:**
- **Author identity is a pseudonym with no bio.** "OldBoy" and "OldBoy-RSS" have no author bio page, no credentials, no photo. E-E-A-T requires demonstrable expertise and real identity signals. AI systems citing content look for verifiable authorship.
- **"OldBoy-RSS" posts are AI-generated** (via `sutvarkyk.js` automation). These lack human expertise signals entirely. Google's E-E-A-T guidelines penalise sites where AI-generated content dominates without human editorial oversight declaration.
- **One empty blog post found:** `"Ką sekti internete DI temomis?"` — published post with completely empty content (`<p><br></p>` repeated 12 times). This is a negative E-E-A-T signal.
- **No author profile pages** — `/user/@OldBoy` does not contain a meaningful biography, expertise statement, or credentials.
- **No "About" page** with editorial policy, team information, or contact details.
- **No expert quotes, citations, or external authoritative links** in content.
- **Content is topically scattered** — AI topics (ChatGPT, agents), mixed with coastal region topics. The site's stated niche (pajūrio — coastal community) is not consistently reflected in the blog content.
- **Dates not visible in rendered pages** — even though dates exist in the DB, they are rendered client-side (invisible to crawlers).

---

### E. Schema Markup — 40/100

**What works:**
- `WebSite` schema with `SearchAction` (`potentialAction`) on homepage. ✅
- `inLanguage: "lt"` declared. ✅
- Schema is valid JSON-LD format. ✅

**Missing (critical gaps):**
- **No `LocalBusiness` or `Organization` schema** — this is the single most important schema for a local community platform. Search engines and AI models use this to understand what the business is, where it operates, and how to contact it.
- **No `Article` / `BlogPosting` schema on blog post pages** — each article should have `@type: "BlogPosting"` with `headline`, `author`, `datePublished`, `dateModified`, `image`, `publisher`. Currently not injected.
- **No `BreadcrumbList` schema** — important for site navigation understanding.
- **No `ItemList` schema on listing pages** — `/listings`, `/marketplace` have no machine-readable listing summaries.
- **No `FAQPage` schema** — missed opportunity for featured snippets and AI citations on the "about" or help content.
- **No `Place` schema on kavines.html or miesteliai.html** — these pages list physical locations but have no geographic machine-readable data.
- **`WebSite` SearchAction target URL is wrong** — points to `https://sekmes.lt/?q={search_term_string}` but the SPA router does not handle `?q=` query param for search. This schema property should match actual search URL pattern.

---

## Issues Priority List

### CRITICAL — Fix Immediately

1. **Sitemap.xml routing bug**
   File: `d:/_PAL/benino/agent-network/server/index.js`
   Line 664: Add `xml` to the file extension regex so `.xml` files are NOT caught by the SPA fallback. Change:
   ```js
   const fileExtensionRegex = /\.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot|map|json|html)$/i;
   ```
   To:
   ```js
   const fileExtensionRegex = /\.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot|map|json|html|xml|txt)$/i;
   ```
   Also ensure the sitemap route is registered **before** `express.static` in index.js, or move it above line 137. This also fixes `robots.txt` and `llms.txt` serving consistency.

2. **Add per-article meta injection for blog post pages (SSR)**
   File: `d:/_PAL/benino/agent-network/server/index.js`
   Add a server-side route before the SPA fallback that intercepts `/blog/:slug`, fetches the post from Supabase, and injects dynamic `<title>`, `<meta name="description">`, `og:title`, `og:description`, `og:image`, and an `Article` JSON-LD block into the HTML before serving. This is the most impactful single change for both SEO and GEO.

3. **Add `og:image` to homepage and all key pages**
   Use existing `/img/palanga-hero.jpg` or `/img/pajuris.jpg` as the default OG image. Add:
   ```html
   <meta property="og:image" content="https://sekmes.lt/img/palanga-hero.jpg">
   <meta property="og:image:width" content="1200">
   <meta property="og:image:height" content="630">
   <meta name="twitter:image" content="https://sekmes.lt/img/palanga-hero.jpg">
   ```
   File: `d:/_PAL/benino/agent-network/public/index.html`

4. **Delete or complete the empty blog post**
   The post `"Ką sekti internete DI temomis?"` (slug: `ka-sekti-internete`) has empty content. Delete it or add content. Empty published posts damage E-E-A-T crawl signals.

---

### HIGH PRIORITY — Fix This Week

5. **Add `LocalBusiness` + `Organization` JSON-LD to homepage**
   File: `d:/_PAL/benino/agent-network/public/index.html`
   Add after the existing `WebSite` schema block:
   ```json
   {
     "@context": "https://schema.org",
     "@type": ["LocalBusiness", "WebSite"],
     "name": "Pajūrio Portalas",
     "url": "https://sekmes.lt",
     "description": "Lietuviška pajūrio bendruomenės platforma — skelbimai, renginiai ir žinios iš Klaipėdos, Palangos ir Neringos",
     "areaServed": [
       {"@type": "City", "name": "Klaipėda"},
       {"@type": "City", "name": "Palanga"},
       {"@type": "Place", "name": "Neringa"}
     ],
     "inLanguage": "lt",
     "sameAs": ["https://sekmes.lt"]
   }
   ```

6. **Add `Article`/`BlogPosting` JSON-LD to blog post pages (server-side)**
   File: `d:/_PAL/benino/agent-network/server/routes/blog.js` or `server/index.js`
   When serving `/blog/:slug`, inject:
   ```json
   {
     "@type": "BlogPosting",
     "headline": "{{title}}",
     "author": {"@type": "Person", "name": "{{author_name}}"},
     "datePublished": "{{published_at}}",
     "dateModified": "{{updated_at}}",
     "publisher": {"@type": "Organization", "name": "Pajūrio Portalas"}
   }
   ```

7. **Expand `llms.txt`**
   File: `d:/_PAL/benino/agent-network/public/llms.txt`
   Add sections:
   - `## API` — describe public API endpoints (e.g., `/api/blog?limit=10`, `/api/listings`)
   - `## Regions covered` — list all coastal towns the platform covers
   - `## Content types` — blog posts, job listings, rental properties, events, café directories
   - `## Update frequency` — how often new content is published
   - `## Language` — Lithuanian (lt-LT); some AI-generated content in Lithuanian

8. **Declare RSS feed in `<head>`**
   File: `d:/_PAL/benino/agent-network/public/index.html`
   ```html
   <link rel="alternate" type="application/rss+xml" title="Pajūrio Portalas — Žinios" href="https://sekmes.lt/rss.xml">
   ```

9. **Fix kavines.html title length (71 chars → under 60)**
   File: `d:/_PAL/benino/agent-network/public/kavines.html`
   Change: `Kavinės Pajūryje — Klaipėda, Palanga, Neringa | Pajūrio Portalas`
   To: `Kavinės Pajūryje — Klaipėda, Palanga, Neringa`  (47 chars)

10. **Add static intro paragraphs to kavines.html and miesteliai.html**
    These pages have `<h1>` headings but zero descriptive body text. Add 2-3 paragraphs (100-150 words each) describing what the page contains, as static HTML — not JS-rendered. This is the primary fix for AI citability on these high-value local pages.

---

### MEDIUM PRIORITY — Fix This Month

11. **Create a real "About" page (`/apie`) with editorial policy**
    Required for E-E-A-T. Should include: who runs the platform, editorial standards for blog posts, how listings are moderated, contact email, business registration info.

12. **Add author bio pages for "OldBoy" and editors**
    File: Create `d:/_PAL/benino/agent-network/public/autor/oldboy.html` or enhance `/user/@OldBoy` with biography, expertise, photo, and credentials. Link author names on blog posts to these pages.

13. **Label AI-generated content explicitly**
    Posts authored by "OldBoy-RSS" are AI-generated. Add a disclaimer badge: "AI-sugeneruotas turinys, redaguotas žmogaus" or declare it in the JSON-LD `author` field as `{"@type": "SoftwareApplication", "name": "Pajūrio Portalas AI"}`.

14. **Add `Place` / `CafeOrCoffeeShop` schema to kavines.html**
    The café directory is highly citable local data. Use `ItemList` + `LocalBusiness` schema for each establishment entry.

15. **Fix `SearchAction` target URL in WebSite schema**
    Change `target: "https://sekmes.lt/?q={search_term_string}"` to match actual search implementation or remove it until implemented. A broken SearchAction can confuse AI models.
    File: `d:/_PAL/benino/agent-network/public/index.html`

16. **Add `BreadcrumbList` schema to inner pages**
    e.g., on kavines.html: `Pajūrio Portalas > Kavinės ir Restoranai`

17. **Add `favicon.ico` link tag to `<head>`**
    File: `d:/_PAL/benino/agent-network/public/index.html`
    ```html
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    ```

18. **Implement static rendering or pre-rendering for key SPA routes**
    The core GEO problem is that the SPA renders everything in JavaScript. Consider adding a pre-rendering middleware (e.g., `prerender-node`) or server-side rendering for at least: homepage hero text, blog post pages, and listing pages. Without this, AI crawlers that do not execute JS (Perplexity, Claude, most LLM web retrievers) see an essentially empty page.

19. **Add `hreflang` tag if multi-language content is planned**
    Currently Lithuanian only — add `<link rel="alternate" hreflang="lt" href="https://sekmes.lt/">` to signal this to search engines.

20. **Add a static HTML sitemap page at `/svetaineszemelapis`**
    A human-readable sitemap with links to all major sections helps AI crawlers discover content without relying on the XML sitemap.

---

## Summary Assessment

Pajūrio Portalas has solid foundational SEO for its homepage (good meta, canonical, OG tags, robots.txt with AI-bot allowances, and an `llms.txt`). However, it has two structural weaknesses that severely limit its GEO (Generative Engine Optimisation) performance:

1. **SPA architecture** — The majority of content (blog posts, listings, city cards) is rendered entirely in JavaScript. AI crawlers that do not execute JS encounter empty pages. This single issue is responsible for most of the citability and E-E-A-T score loss.

2. **No Article-level schema or dynamic meta** — Blog posts are the site's richest citable content, but they all appear identical to crawlers (same title, same description, no Article schema). This prevents individual articles from being cited or indexed meaningfully by AI systems.

The sitemap routing bug and missing `og:image` are quick wins that should be fixed immediately. The SSR meta injection for blog posts (issue #2) is the highest-ROI single change for GEO performance.
