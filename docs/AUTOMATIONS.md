# AUTOMATIONS.md - Benino Automated Workflows

## 🎯 Vizija: "sutvarkyk [URL]" → Viskas Automatiškai

**Tikslas:** Viena komanda, pilnas pipeline:
1. Analizė (Mokslius + OldBoy)
2. Blog publikacija
3. Teminė ekstraktacija
4. RSS feed
5. Nanobot integracija

---

## 📋 AUTOMATION-1: Initial Analysis & Blog Publishing

### Trigger
```
sutvarkyk [URL]
```

### Input
- YouTube video URL
- arXiv paper URL
- Podcast link
- Article URL
- Any analyzable content source

### Pipeline Steps

#### 1.1 Source Analysis
```javascript
// Detect source type
if (url.includes('youtube.com')) {
    method = 'youtube_transcript';
} else if (url.includes('arxiv.org')) {
    method = 'arxiv_paper';
} else {
    method = 'web_content';
}
```

#### 1.2 Content Extraction
**YouTube:**
- Extract video metadata (title, author, date, thumbnail)
- Download subtitles via yt-dlp
- Parse transcript

**arXiv:**
- Fetch paper metadata
- Extract abstract, sections
- Parse authors, date, categories

**Web:**
- Fetch HTML content
- Extract main content (readability)
- Parse metadata

#### 1.3 Generate Analyses
**Create Mokslius Analysis:**
```
Output: workspace/blog/YYYY-MM-DD_mokslius_[slug]_palanga.md

Style:
- Chronological structure with timestamps
- Technical Lithuanian terminology
- Implementation details
- Academic rigor
- Performance metrics
```

**Create OldBoy Analysis:**
```
Output: workspace/blog/YYYY-MM-DD_oldboy_[slug]_palanga.md

Style:
- Start: "Sėdžiu Palangoje, pušys kvepia, jūra ošia..."
- Storytelling with atmosphere
- Metaphors and narrative
- Blockquotes for brilliant insights
- Maximalism approach
```

#### 1.4 Auto-Generate Tags
**AI analyzes content and generates relevant tags:**
```javascript
// Extract key concepts
const tags = await analyzeContentForTags(content);
// Examples: ['AI_Governance', 'Graph_Networks', 'Congressional_Trading']
```

**Tag categories:**
- Technology: `Vibe_Coding`, `AI_Tools`, `Graph_Learning`, `Temporal_Networks`
- Domain: `Congressional_Trading`, `Healthcare`, `Finance`, `Education`
- Format: `Palanga_Edition`, `OldBoy_Extracts`, `Mokslius_Protocol`

#### 1.5 Auto-Detect Category
**From tags → Blog category:**
```javascript
function detectCategory(tags) {
    if (tags.some(t => ['Vibe_Coding', 'AI_Tools', 'Programming'].includes(t))) {
        return 'Tech';
    } else if (tags.some(t => ['AI_Governance', 'Policy'].includes(t))) {
        return 'AI Valdymas';
    } else if (tags.some(t => ['Career', 'Ethics', 'Leadership'].includes(t))) {
        return 'Karjera';
    } else if (tags.some(t => ['Philosophy', 'Meaning'].includes(t))) {
        return 'Filosofija';
    } else {
        return 'Tendencijos'; // Default
    }
}
```

#### 1.6 Upload to Blog
```bash
node upload_palanga_post.js "workspace/blog/YYYY-MM-DD_oldboy_[slug]_palanga.md"

Automatic:
- Convert Markdown → Clean HTML (Quill compatible)
- Add source link (top right, italic)
- Add cover image (from video thumbnail or Unsplash)
- Generate interactive tag buttons
- Create clean excerpt (160 chars, no markdown syntax)
- Insert into Supabase blog_posts table
  - author_name: "OldBoy-RSS"
  - status: "published"
  - published_at: NOW()
```

#### 1.7 Update RSS Feed
```javascript
// Generate/update RSS feed
const rss = generateRSS({
    title: postTitle,
    link: `https://agent-network.com/blog/${slug}`,
    description: excerpt,
    author: 'OldBoy-RSS',
    pubDate: new Date(),
    categories: [category, ...tags]
});

// Save to public/rss.xml
fs.writeFileSync('public/rss.xml', rss);
```

#### 1.8 Create Dedicated RSS Page
```
URL: /blog/rss-posts
Filter: author_name = 'OldBoy-RSS'
Display: Chronological list of automated posts
Features:
- Subscribe button
- RSS icon
- Auto-updates
```

### Output Summary (AUTOMATION-1)
✅ `workspace/blog/YYYY-MM-DD_mokslius_[slug]_palanga.md` (archyvas)
✅ `workspace/blog/YYYY-MM-DD_oldboy_[slug]_palanga.md` (blog source)
✅ Blog post published (author: OldBoy-RSS)
✅ RSS feed updated
✅ Tags auto-generated
✅ Category auto-detected

---

## 📋 AUTOMATION-2: Theme Extraction & Distribution

### Trigger
**Automatically after AUTOMATION-1 completes**
OR
```
suskaidyk workspace/blog/YYYY-MM-DD_oldboy_[slug]_palanga.md
```

### Pipeline Steps

#### 2.1 Read Full OldBoy Article
```javascript
const fullArticle = fs.readFileSync(
    'workspace/blog/YYYY-MM-DD_oldboy_[slug]_palanga.md',
    'utf-8'
);
```

#### 2.2 AI Theme Identification
**Prompt to LLM (Gemini/Groq):**
```
Analyze this OldBoy article and identify distinct themes/topics.

For each theme:
1. Theme name (Lithuanian, 1-3 words)
2. Category (Technologijos, Karjera, AI_Valdymas, Filosofija, Tendencijos, or NEW)
3. Relevant sections/paragraphs
4. Key insights
5. Standalone value (can it be a separate article?)

Return JSON:
{
  "themes": [
    {
      "name": "AI Priežiūra Valdžioje",
      "category": "AI_Valdymas",
      "sections": ["## Kai AI Seka Kongreso Ranką", "## Grafai Kaip Tinklas"],
      "insights": ["Temporal graphs for oversight", "Multi-modal data integration"],
      "standalone": true
    },
    ...
  ]
}
```

#### 2.3 Extract Fragments
**For each identified theme:**
```javascript
for (const theme of themes) {
    // Extract relevant content
    const fragment = extractSections(fullArticle, theme.sections);

    // Add theme-specific intro/outro
    const thematicArticle = `
---
tags:
  - ${theme.category}
  - ${generateThemeTags(theme)}
  - Palanga_Edition
  - OldBoy_Extracts
date: ${new Date().toISOString().split('T')[0]}
author: OldBoy Alchemist
source: ${originalSource}
parent_article: ${parentSlug}
---

# ${theme.name}

*Ištrauka iš "${originalTitle}"*

${fragment}

---

**OldBoy pastaba:** Ši tema išskirta iš pilnos analizės. Skaityti pilną straipsnį: [link]
`;

    // Save to appropriate folder
    const filename = `${date}_${slugify(theme.name)}.md`;
    saveThematicExtract(theme.category, filename, thematicArticle);
}
```

#### 2.4 Dynamic Folder Creation
```javascript
function saveThematicExtract(category, filename, content) {
    const folderPath = `workspace/oldboy/${category}/`;

    // Create folder if doesn't exist
    if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, { recursive: true });
        console.log(`📁 Created new category folder: ${category}`);
    }

    // Save extract
    fs.writeFileSync(path.join(folderPath, filename), content);
    console.log(`✅ Saved: ${folderPath}${filename}`);
}
```

**Supported categories:**
- Existing: `Technologijos`, `Tendencijos`, `Karjera`, `Filozofija`, `AI_Valdymas`, `Agentai`
- NEW: Any category identified by AI (e.g., `Medicina`, `Robotika`, `Kosmosas`)

#### 2.5 Upload Theme Extracts to Blog
```javascript
for (const extract of extractedThemes) {
    await uploadToBlog(extract.filepath);
    console.log(`✅ Published theme: ${extract.theme.name}`);
}
```

**Each extract gets:**
- Own blog post
- Category from folder name
- Tags from frontmatter
- Link back to parent article
- Author: "OldBoy-RSS" (or "OldBoy-Extracts"?)

#### 2.6 Create Cross-Category Links
**If theme appears in multiple categories:**
```javascript
// Same theme, different perspectives
const theme = "AI Ethics in Healthcare";

// Save to multiple folders
saveThematicExtract('AI_Valdymas', filename, content_governance_perspective);
saveThematicExtract('Medicina', filename, content_healthcare_perspective);
```

#### 2.7 Generate Theme Index
```javascript
// workspace/oldboy/THEME_INDEX.md
# Teminių Ištraukų Indeksas

## AI Valdymas
- [2026-02-08] Congressional Trading Detection (iš arXiv paper)
- [2026-02-08] Temporal Graphs for Oversight (iš arXiv paper)

## Karjera
- [2026-02-08] Ethics in Trading (iš arXiv paper)
- [2026-02-07] Claude Komandiniai Įgūdžiai (iš Vibe Coding)

...
```

#### 2.8 Nanobot Integration
```javascript
// Check if Nanobot is running
const nanobotRunning = await checkProcess('nanobot');

if (!nanobotRunning) {
    console.log('🤖 Starting Nanobot...');
    await startNanobot();
}

// Notify Nanobot about new content
await nanobotNotify({
    type: 'new_blog_post',
    title: postTitle,
    url: postUrl,
    category: category,
    tags: tags,
    excerpt: excerpt
});
```

**Nanobot actions:**
- Post to configured WhatsApp groups/contacts
- Update knowledge base
- Add to available content for chat responses

#### 2.9 Update MEMORY.md
```javascript
// Auto-update memory with patterns learned
const memoryUpdate = `
## ${new Date().toISOString().split('T')[0]} - ${source}

**Source:** ${url}
**Themes identified:** ${themes.map(t => t.name).join(', ')}
**New categories created:** ${newCategories.join(', ') || 'None'}
**Insights:**
- ${keyInsights.join('\n- ')}
`;

appendToMemory(memoryUpdate);
```

### Output Summary (AUTOMATION-2)
✅ Themes identified (AI analysis)
✅ Fragments extracted
✅ Folders created dynamically (if needed)
✅ Theme extracts saved to `workspace/oldboy/[TEMA]/`
✅ Each extract uploaded to blog
✅ Theme index updated
✅ Nanobot started (if needed)
✅ Nanobot notified
✅ Memory updated

---

## 🔄 Complete Automation Flow

### Single Command
```
sutvarkyk https://youtube.com/watch?v=xxx
```

### Execution Timeline
```
[00:00] 🎬 AUTOMATION-1 Start
[00:01] 📥 Fetch video metadata & transcript
[00:02] 🧠 Generate Mokslius analysis
[00:05] 📝 Generate OldBoy narrative
[00:06] 🏷️  Auto-generate tags
[00:06] 📁 Auto-detect category
[00:07] 🚀 Upload to blog (OldBoy-RSS)
[00:08] 📡 Update RSS feed
[00:08] ✅ AUTOMATION-1 Complete

[00:09] 🎬 AUTOMATION-2 Start
[00:10] 🔍 AI identifies themes (3 found)
[00:12] ✂️  Extract fragments
[00:13] 📁 Create folders (Medicina - NEW)
[00:14] 💾 Save theme extracts
[00:15] 🚀 Upload theme 1 to blog
[00:16] 🚀 Upload theme 2 to blog
[00:17] 🚀 Upload theme 3 to blog
[00:18] 📊 Update theme index
[00:19] 🤖 Check Nanobot status
[00:20] 📢 Notify Nanobot
[00:21] 💭 Update MEMORY.md
[00:22] ✅ AUTOMATION-2 Complete

[00:22] 🎉 DONE: 1 full article + 3 theme extracts published
```

---

## 🛠️ Implementation Plan

### Phase 1: AUTOMATION-1 Foundation
- [ ] Create `automate_analysis.js` script
- [ ] Integrate yt-dlp for YouTube
- [ ] Integrate arXiv API
- [ ] Implement Mokslius template generator
- [ ] Implement OldBoy template generator
- [ ] Auto-tag generation (LLM-based)
- [ ] Auto-category detection logic
- [ ] RSS feed generator
- [ ] Create RSS page frontend

### Phase 2: AUTOMATION-2 Foundation
- [ ] Create `automate_themes.js` script
- [ ] Implement AI theme identification (Gemini/Groq)
- [ ] Fragment extraction logic
- [ ] Dynamic folder creation
- [ ] Batch upload functionality
- [ ] Theme index generator

### Phase 3: Nanobot Integration
- [ ] Nanobot status checker
- [ ] Nanobot starter script
- [ ] Notification system (WhatsApp API)
- [ ] Knowledge base sync
- [ ] Auto-posting to groups

### Phase 4: Orchestration
- [ ] Create `sutvarkyk.js` master script
- [ ] Chain AUTOMATION-1 → AUTOMATION-2
- [ ] Error handling & recovery
- [ ] Progress logging
- [ ] Success notifications

### Phase 5: Monitoring & Optimization
- [ ] Dashboard for automation status
- [ ] Success rate tracking
- [ ] Theme quality metrics
- [ ] User feedback loop

---

## 📊 Success Metrics

### AUTOMATION-1
- ✅ Time to publish: < 30 seconds
- ✅ Tag accuracy: > 90%
- ✅ Category accuracy: > 85%
- ✅ RSS feed valid: 100%
- ✅ Blog formatting correct: 100%

### AUTOMATION-2
- ✅ Theme identification recall: > 80% (finds most themes)
- ✅ Theme identification precision: > 90% (themes are valid)
- ✅ Fragment quality: Human-readable, standalone
- ✅ Folder creation: Works for any category
- ✅ Nanobot notification: < 5 seconds

---

## 🚨 Error Handling

### AUTOMATION-1 Failures
**Video unavailable:**
- Fallback: Try alternative extraction methods
- Notify: "Video not accessible, provide transcript manually?"

**LLM timeout:**
- Retry: 3 attempts with exponential backoff
- Fallback: Use template-based generation

**Upload failure:**
- Retry: 2 attempts
- Save to queue: Manual review needed

### AUTOMATION-2 Failures
**No themes identified:**
- Fallback: Treat entire article as single theme "Tendencijos"
- Notify: "No distinct themes found, published as-is"

**Fragment too short:**
- Skip: Don't create extract if < 500 chars
- Log: "Theme identified but fragment too small"

**Nanobot unreachable:**
- Queue: Save notification for later
- Continue: Don't block on Nanobot

---

## 🎯 Future Enhancements

### Smart Features
- **Duplicate detection:** Check if similar content already analyzed
- **Multi-language:** Support English sources → Lithuanian output
- **Voice synthesis:** Generate audio versions via TTS
- **Social media:** Auto-post to Twitter/LinkedIn
- **Analytics:** Track which themes get most engagement

### AI Improvements
- **Better theme detection:** Fine-tune LLM on our corpus
- **Quality scoring:** AI rates extract quality before publishing
- **Style consistency:** Ensure fragments maintain Palanga voice
- **Cross-references:** Auto-link related themes

---

## 📝 Configuration

### automation_config.json
```json
{
  "automation_1": {
    "enabled": true,
    "llm_provider": "gemini",
    "model": "gemini-2.5-flash",
    "auto_publish": true,
    "rss_enabled": true
  },
  "automation_2": {
    "enabled": true,
    "auto_trigger": true,
    "min_themes": 1,
    "max_themes": 5,
    "min_fragment_length": 500,
    "nanobot_notify": true
  },
  "categories": {
    "allow_new": true,
    "map": {
      "Technologijos": "Tech",
      "Tendencijos": "Tendencijos",
      "Karjera": "Karjera",
      "Filozofija": "Filosofija",
      "AI_Valdymas": "AI Valdymas"
    }
  },
  "notifications": {
    "nanobot_groups": ["Pajūrio Tinklas Komanda"],
    "admin_alerts": true
  }
}
```

---

## 🎓 Usage Examples

### Example 1: YouTube Video
```bash
$ sutvarkyk https://youtube.com/watch?v=dQw4w9WgXcQ

🎬 Starting AUTOMATION-1...
📥 Fetching: "Rick Astley - Never Gonna Give You Up"
🧠 Generating analyses...
✅ Published: "Kai Muzika Virsta Memu: Rick Astley Fenomenas"
📡 RSS updated

🎬 Starting AUTOMATION-2...
🔍 Themes identified: 3
  1. Virality Psychology (Tendencijos)
  2. 80s Music Revival (Kultūra)
  3. Internet Culture (Technologijos)
✅ All extracts published
🤖 Nanobot notified

🎉 DONE in 22 seconds
```

### Example 2: arXiv Paper
```bash
$ sutvarkyk https://arxiv.org/abs/2602.05514

🎬 Starting AUTOMATION-1...
📥 Fetching: "Detecting Information Channels in Congressional Trading"
🧠 Generating analyses...
✅ Published: "Kai AI Seka Kongreso Ranką"
📡 RSS updated

🎬 Starting AUTOMATION-2...
🔍 Themes identified: 4
  1. Temporal Graph Networks (Tech)
  2. AI Governance (AI Valdymas)
  3. Congressional Ethics (Karjera)
  4. Oversight Systems (Tendencijos)
📁 Created new folder: Medicina (identified healthcare angle)
✅ All extracts published
🤖 Nanobot notified

🎉 DONE in 28 seconds
```

---

**OldBoy 🤞**
*Automation edition - nes laikas brangesnis už viską*
