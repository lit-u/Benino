# Phase 5: Hotel Mini-Website — Research

**Researched:** 2026-03-19
**Domain:** Node.js/Express SSR, Supabase Storage, JSON-LD Schema.org, QR code generation, Vanilla JS drag-drop
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Data model — 3 tables:**
- `hotels`: id, slug, owner_id (FK → users), name, description, address, city, phone, whatsapp, created_at
- `hotel_rooms`: id, hotel_id, number, name, price_per_night, area_m2, sea_distance_m, orientation (enum: N/NE/E/SE/S/SW/W/NW), orientation_note, noise_level (enum: quiet/moderate/lively), availability_status (enum: available/occupied), available_from (date, nullable), description
- `room_photos`: id, room_id, url, type (enum: window_view/interior), sort_order

**Photos:**
- 2 types: 1 `window_view` + up to 5 `interior`
- Supabase Storage bucket: `hotel-photos`, path: `{hotel_id}/{room_id}/{type}-{sort}.jpg`
- Auto resize: 600×400px, max 50KB (reuse existing ImageUploadService logic)
- Admin: drag-drop with order management, window_view tagged separately

**Sea proximity (room level):**
- Distance: owner enters meters → displayed as minutes (meters ÷ 80)
- Orientation: N/NE/E/SE/S/SW/W/NW dropdown + orientation_note text field
- Noise: quiet/moderate/lively dropdown
- All 3 fields are per-room, not per-hotel

**Availability traffic light:**
- green: `available` → "LAISVAS"
- red: `occupied` + available_from → "UŽIMTAS / Laisvas nuo: [date]"
- yellow: available_from within 14 days → "Laisvas netrukus"
- Manual toggle by owner in admin panel

**Reservation CTA:**
- Mini form (name, arrival, departure, message)
- Owner chooses channel: WhatsApp deep link OR mailto — no DB storage

**QR codes:**
- Per room: `sekmes.lt/hotel/{slug}#room-{number}`
- Admin panel: "Download QR (PDF)" + "Copy URL" buttons

**AI/Agents friendly:**
- SSR: `/hotel/:slug` returns full HTML from server (reuse injectMeta() pattern)
- JSON-LD: LodgingBusiness + HotelRoom with amenityFeature for sea_distance_m, orientation, noise_level
- Semantic HTML: `<article>`, `<address>`, `<time>`
- Meta tags: og:title, og:description, og:image (first room photo), canonical URL

**MVP limit:** Up to 10 rooms per hotel

**URLs:**
- Public: `/hotel/:slug`
- Admin: `/hotel/:slug/admin`

### Claude's Discretion
- Exact page design and CSS (dark theme matching rest of platform)
- QR generation library (e.g., `qrcode` npm)
- Supabase Storage bucket configuration and RLS rules
- Availability traffic light exact color codes in UI

### Deferred Ideas (OUT OF SCOPE)
- Full booking calendar with DB reservations — separate phase
- Pajūrio 2.5D map with hotels as interactive pins — long-term vision
- Room planner (furniture drag) — blueprint3d / react-planner — separate phase
- Stripe/Paysera payment integration — separate phase
- Multi-language (EN/DE) — v2
- Owner dashboard with all-objects statistics — separate phase
</user_constraints>

---

## Summary

Phase 5 builds a mini-website feature inside the existing `agent-network` Node.js/Express/Supabase application. The work is straightforward because the project already has every major pattern in production: SSR meta injection via `injectMeta()`, Supabase Storage with `ImageUploadService` (sharp, 600×400, 50KB), `requireUser`/`requireAuthLevel` middleware, and Lithuanian-aware slug generation.

The three new route files (`/hotel/:slug` SSR, `/hotel/:slug/admin` page, `/api/hotels` CRUD) follow exactly the same shape as existing listings and blog routes. The main new technical work is: (1) wiring a dedicated `hotel-photos` Storage bucket, (2) emitting LodgingBusiness + HotelRoom JSON-LD in `injectMeta()`, (3) generating QR codes server-side using the `qrcode` npm package (not yet installed), and (4) building a vanilla JS drag-drop photo reorder widget matching the platform's existing ES6 module style.

**Primary recommendation:** Create 4 new files — `server/routes/hotels.js` (CRUD API), `server/services/hotel-image-service.js` (thin wrapper over ImageUploadService with `hotel-photos` bucket), `public/hotel.html` + `public/hotel-admin.html` — and register `/hotel/:slug` SSR + `/api/hotels` routes in `server/index.js` before the `app.get('*')` SPA fallback. Use the `qrcode` package (v1.5.4) for QR generation.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| express | already installed | Route handling | Project standard |
| @supabase/supabase-js | already installed | DB + Storage CRUD | Project standard |
| sharp | already installed | Image resize/compress to 600×400, 50KB | Already used in ImageUploadService |
| multer | already installed | Multipart file upload | Already used in upload.js |
| uuid | already installed | Unique filenames | Already used |
| qrcode | 1.5.4 (not installed) | Server-side QR code generation to PNG/SVG/DataURL | Standard Node.js QR lib, 20k+ weekly downloads |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| qrcode | 1.5.4 | QR PNG buffer for admin download | In hotel admin route for QR endpoint |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| qrcode (server-side) | qrcode.js (browser) | Server-side keeps implementation in route handler, browser-side is lighter. Use server-side because admin page already calls API endpoints. |
| sharp (contain+black bg) | sharp (cover/crop) | contain preserves full image — already confirmed default in ImageUploadService |

**Installation:**
```bash
cd d:/_PAL/benino/agent-network
npm install qrcode
```

**Version verification:** `npm view qrcode version` returned `1.5.4` (verified 2026-03-19).

---

## Architecture Patterns

### File Layout
```
server/
├── routes/
│   └── hotels.js              # CRUD: GET /api/hotels/:slug, POST, PUT, DELETE
│                              # + QR endpoint: GET /api/hotels/:slug/room/:num/qr
│                              # + Photo reorder: PUT /api/hotels/:slug/rooms/:roomId/photos/order
├── services/
│   └── hotel-image-service.js # Thin wrapper: ImageUploadService with bucket='hotel-photos'
public/
├── hotel.html                 # Public mini-website (SSR-enhanced, then JS hydrates)
├── hotel-admin.html           # Owner admin panel (L2+ protected)
└── modules/
    ├── hotel-module.js        # Public page: photo gallery, sea proximity block, reservation form
    └── hotel-admin-module.js  # Admin: room CRUD, drag-drop photos, availability toggle, QR download
```

### Pattern 1: SSR Route (injectMeta + LodgingBusiness JSON-LD)

The existing `injectMeta()` signature in `server/index.js:695` is:
```javascript
function injectMeta(baseHtml, { title, description, url, schemaType, extraSchema = '' })
```

It strips the existing `<title>`, injects meta tags + canonical + OG tags, and appends `extraSchema` before `</head>`. The `extraSchema` parameter accepts a raw `<script type="application/ld+json">` string.

**Hotel SSR route wires in between the blog SSR block (line ~832) and the SPA fallback (line ~836):**

```javascript
// Source: server/index.js pattern (lines 717-744 + 775-832)
app.get('/hotel/:slug', async (req, res, next) => {
  try {
    const { slug } = req.params;
    const { data: hotel } = await supabaseSeo
      .from('hotels')
      .select(`*, hotel_rooms(*, room_photos(*))`)
      .eq('slug', slug)
      .single();

    if (!hotel) return next();

    const firstPhoto = hotel.hotel_rooms?.[0]?.room_photos
      ?.find(p => p.type === 'window_view')?.url
      || hotel.hotel_rooms?.[0]?.room_photos?.[0]?.url
      || 'https://sekmes.lt/img/palanga-hero.jpg';

    const title = `${hotel.name} | Pajūrio Portalas`;
    const description = (hotel.description || '').substring(0, 160);
    const url = `https://sekmes.lt/hotel/${slug}`;

    const lodgingSchema = buildLodgingSchema(hotel);   // see JSON-LD section
    const extraSchema = `<script type="application/ld+json">${JSON.stringify(lodgingSchema)}</script>`;

    const baseHtml = fs.readFileSync(indexHtmlPath, 'utf8');
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.send(injectMeta(baseHtml, { title, description, url, schemaType: 'LodgingBusiness', extraSchema }));
  } catch (err) {
    console.error('SSR hotel meta error:', err);
    next();
  }
});
```

The admin route does NOT need SSR — it serves `hotel-admin.html` directly (owner is logged in, no crawler access needed):
```javascript
app.get('/hotel/:slug/admin', requireUser, (req, res) => {
  res.sendFile(path.join(__dirname, '../public/hotel-admin.html'));
});
```

**Critical ordering:** Both `/hotel/:slug` and `/hotel/:slug/admin` MUST be registered BEFORE `app.get('*', ...)` on line 836. They should be added after the blog SSR block (~line 832) but before the SPA fallback.

### Pattern 2: Hotel Image Service

`ImageUploadService` already implements everything needed (sharp, 600×400, 50KB, Supabase Storage, `ensureBucketExists`). Create a thin subclass or wrapper that overrides only `bucketName` and `filePath` format:

```javascript
// server/services/hotel-image-service.js
import ImageUploadService from './image-upload-service.js';

export default class HotelImageService extends ImageUploadService {
  constructor() {
    super();
    this.bucketName = 'hotel-photos';
    // Override: no watermark for hotel photos (hotel owner content, not user-generated)
    this.watermarkPath = null; // Will gracefully skip in addWatermark()
  }

  async uploadRoomPhoto(buffer, originalName, hotelId, roomId, type, sortOrder) {
    // Override filePath: {hotelId}/{roomId}/{type}-{sort}.jpg
    // ... call super.compressImage(), then custom upload path
  }
}
```

The parent `addWatermark()` already handles missing watermark file gracefully (returns imageBuffer unchanged). Setting `this.watermarkPath = null` triggers the `fs.access` catch block.

### Pattern 3: Auth Middleware for Admin Routes

The project has two auth systems in transition. For hotel admin routes, use the **new system** (`requireUser` from `requireRole.js`) since it supports the legacy L2 fallback:

```javascript
// requireUser already checks BOTH new (req.auth.role) and legacy (req.authContext.level >= 2)
import { requireUser } from '../middleware/requireRole.js';

router.post('/', requireUser, async (req, res) => { ... });
router.put('/:id', requireUser, async (req, res) => { ... });
```

**Owner isolation:** After `requireUser`, manually verify `hotel.owner_id === req.authContext?.userId || req.auth?.identityId`. The CONTEXT.md confirms "service role key bypass on server" — use the same pattern as `listings.js:16-23`.

### Pattern 4: Supabase Client Initialization

Copy exactly from `listings.js:16-23`:
```javascript
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY ||
  process.env.SUPABASE_SERVICE_KEY ||
  process.env.SUPABASE_KEY ||
  process.env.SUPABASE_ANON_KEY ||
  'missing-key-placeholder'
);
```

### Pattern 5: Slug Generation for Hotels

Use existing `generateSlug()` from `server/utils/slug-generator.js` with `ensureUniqueSlug()`:

```javascript
import { generateSlug, ensureUniqueSlug } from '../utils/slug-generator.js';

const baseSlug = generateSlug(hotel.name, 50);
const slug = await ensureUniqueSlug(baseSlug, async (s) => {
  const { data } = await supabase.from('hotels').select('id').eq('slug', s).maybeSingle();
  return !!data;
});
```

### Anti-Patterns to Avoid

- **Do NOT use `app.get('/:slug', ...)` pattern** — the generic pattern `/:type/:slug` in index.js already handles specific type prefixes. `/hotel/:slug` with literal `hotel` prefix is unambiguous and won't conflict.
- **Do NOT register hotel routes inside `app.listen()`** — all routes are registered before `app.listen()` in index.js. Match this pattern.
- **Do NOT add hotel SSR route after `app.get('*', ...)`** — it will never be reached.
- **Do NOT use `fit: 'cover'`** — the existing ImageUploadService uses `fit: 'contain'` with black background. Keep consistent for hotel photos too.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Image resize to 600×400, 50KB | Custom resize logic | `ImageUploadService.compressImage()` | Already handles quality reduction loop, fallback dimensions, mozjpeg |
| Slug uniqueness check | Custom loop | `ensureUniqueSlug()` in slug-generator.js | Already handles counter suffix, safety limit, timestamp fallback |
| QR code PNG generation | Canvas drawing | `qrcode` npm v1.5.4 | QR spec compliance, error correction levels, PNG buffer output |
| Auth level gate | Manual session check | `requireUser` from requireRole.js | Handles dual auth systems (new + legacy L2), correct 401/403 |
| JSON escaping in JSON-LD | Manual `.replace()` | `JSON.stringify()` with object | Already done correctly in blog SSR (line 794) |
| Supabase Storage public URL | Construct URL manually | `supabase.storage.from(bucket).getPublicUrl(path)` | Format subject to change, official method stable |

**Key insight:** 80% of the infrastructure already exists. This phase is primarily wiring, schema, and UI — not new technical groundwork.

---

## Common Pitfalls

### Pitfall 1: Route Order — Hotel vs SPA Fallback
**What goes wrong:** `/hotel/:slug` returns `index.html` with no SSR if registered after `app.get('*', ...)`.
**Why it happens:** Express routes match in registration order. The SPA fallback on line 836 catches everything.
**How to avoid:** Register both `/hotel/:slug` and `/hotel/:slug/admin` between the blog SSR block and the `app.get('*', ...)` line.
**Warning signs:** `/hotel/test-slug` returns generic index.html with no hotel title in `<title>`.

### Pitfall 2: Admin Route Conflicts with SSR Route
**What goes wrong:** `/hotel/:slug/admin` matches before `/hotel/:slug` if Express tries to match `:slug` = `slug/admin`.
**Why it happens:** Not an issue — Express matches exact literal segments first. `/hotel/:slug/admin` has 3 segments; `/hotel/:slug` has 2. Register specific route (`/admin` suffix) first as a precaution.
**How to avoid:** Register `/hotel/:slug/admin` before `/hotel/:slug` in index.js.

### Pitfall 3: Supabase Storage Bucket Not Public
**What goes wrong:** Photos upload successfully but URLs return 403 when rendered.
**Why it happens:** Default bucket policy is private; `getPublicUrl()` returns a URL that requires auth token.
**How to avoid:** Create bucket with `public: true` (as done in `ensureBucketExists()`). RLS on `hotel-photos` bucket should allow SELECT for all (public read), INSERT/DELETE only for authenticated owner.

### Pitfall 4: JSON-LD Injection Breaks If Hotel Name Contains Quotes
**What goes wrong:** `<script type="application/ld+json">` contains unescaped `"` causing invalid JSON.
**Why it happens:** String interpolation of raw DB values. Blog SSR (line 794) does `.replace(/"/g, '\\"')` on strings manually.
**How to avoid:** Build JSON-LD as a JS object first, then `JSON.stringify()` it. `JSON.stringify` handles all escaping correctly. This is cleaner than the blog SSR approach.

### Pitfall 5: `injectMeta()` og:image Hardcoded
**What goes wrong:** `injectMeta()` (line 706-707) hardcodes `og:image` to `palanga-hero.jpg` — hotel pages won't show room photo in OG preview.
**Why it happens:** The existing function signature doesn't accept `og:image` override.
**How to avoid:** Either (a) extend `injectMeta()` to accept optional `ogImage` parameter, or (b) in the hotel SSR handler, patch the HTML after calling `injectMeta()` by replacing the hardcoded og:image value. Option (a) is cleaner. The change is backward-compatible (default remains the hero image).

### Pitfall 6: `requireUser` vs `requireAuthLevel` Confusion
**What goes wrong:** Using deprecated `requireAuthLevel(2)` when the new `requireUser` is the correct choice.
**Why it happens:** Both exist. `auth-middleware.js` explicitly marks `requireAuthLevel` as `@deprecated`.
**How to avoid:** Use `requireUser` from `requireRole.js` for hotel admin routes. It already has the legacy L2 fallback built in.

### Pitfall 7: Owner Verification Missing After Auth Check
**What goes wrong:** Any L2 user can edit any hotel if the API only checks "is logged in".
**Why it happens:** `requireUser` only checks authentication level, not resource ownership.
**How to avoid:** After auth middleware, query hotel by slug, check `hotel.owner_id` matches `req.authContext.userId` (legacy) or `req.auth.identityId` (new). Return 403 if mismatch.

### Pitfall 8: Photo Sort Order Race Condition on Reorder
**What goes wrong:** Drag-drop reorder sends multiple rapid PATCH requests and the final DB state is wrong.
**Why it happens:** Each drag fires an API call; responses arrive out of order.
**How to avoid:** Debounce the reorder API call (300ms) in frontend JS. Send the complete new order as an array `[{id, sort_order}]` in a single request, not individual per-item requests.

---

## Code Examples

### JSON-LD LodgingBusiness + HotelRoom

```javascript
// Source: Schema.org LodgingBusiness + HotelRoom spec
function buildLodgingSchema(hotel) {
  const baseUrl = 'https://sekmes.lt';
  const hotelUrl = `${baseUrl}/hotel/${hotel.slug}`;

  const rooms = (hotel.hotel_rooms || []).map(room => {
    const seaMinutes = room.sea_distance_m ? Math.ceil(room.sea_distance_m / 80) : null;
    const amenities = [];

    if (seaMinutes) {
      amenities.push({ '@type': 'LocationFeatureSpecification', name: 'Atstumas iki jūros', value: `${seaMinutes} min. pėsčiomis (${room.sea_distance_m}m)` });
    }
    if (room.orientation) {
      amenities.push({ '@type': 'LocationFeatureSpecification', name: 'Lango orientacija', value: room.orientation + (room.orientation_note ? ` — ${room.orientation_note}` : '') });
    }
    if (room.noise_level) {
      const noiseMap = { quiet: 'Ramus', moderate: 'Vidutinis', lively: 'Gyvas' };
      amenities.push({ '@type': 'LocationFeatureSpecification', name: 'Triukšmo lygis', value: noiseMap[room.noise_level] });
    }

    const windowPhoto = room.room_photos?.find(p => p.type === 'window_view');
    const photos = (room.room_photos || []).map(p => p.url);

    return {
      '@type': 'HotelRoom',
      name: room.name || `Kambarys ${room.number}`,
      description: room.description || '',
      url: `${hotelUrl}#room-${room.number}`,
      ...(room.price_per_night ? { priceRange: `${room.price_per_night}€/naktis` } : {}),
      ...(photos.length ? { image: photos } : {}),
      amenityFeature: amenities
    };
  });

  return {
    '@context': 'https://schema.org',
    '@type': 'LodgingBusiness',
    name: hotel.name,
    description: hotel.description || '',
    url: hotelUrl,
    address: {
      '@type': 'PostalAddress',
      streetAddress: hotel.address || '',
      addressLocality: hotel.city || 'Palanga',
      addressCountry: 'LT'
    },
    ...(hotel.phone ? { telephone: hotel.phone } : {}),
    containsPlace: rooms
  };
}
```

### QR Code Generation (server-side, `qrcode` v1.5.4)

```javascript
// Source: qrcode npm package docs
import QRCode from 'qrcode';

// In GET /api/hotels/:slug/rooms/:num/qr handler:
const roomUrl = `https://sekmes.lt/hotel/${slug}#room-${roomNumber}`;

// Return PNG buffer for download
const pngBuffer = await QRCode.toBuffer(roomUrl, {
  type: 'png',
  width: 300,           // 300×300px — good for print
  margin: 2,
  errorCorrectionLevel: 'M'
});

res.setHeader('Content-Type', 'image/png');
res.setHeader('Content-Disposition', `attachment; filename="room-${roomNumber}-qr.png"`);
res.send(pngBuffer);

// For inline display (admin page preview before download):
const dataUrl = await QRCode.toDataURL(roomUrl, { width: 200, margin: 2 });
// Return as JSON: { qrDataUrl: dataUrl, url: roomUrl }
```

### WhatsApp Deep Link Construction

```javascript
// Source: WhatsApp FAQ — wa.me format
function buildWhatsAppLink(whatsappNumber, messageText) {
  // whatsappNumber: stored without + or spaces, e.g. "37061234567"
  const encoded = encodeURIComponent(messageText);
  return `https://wa.me/${whatsappNumber}?text=${encoded}`;
}

// Usage in frontend JS (hotel-module.js):
function buildReservationMessage(hotel, room, formData) {
  return `Sveiki! Norėčiau rezervuoti ${room.name || 'kambarį ' + room.number} viešbutyje "${hotel.name}".\n` +
    `Atvykimas: ${formData.arrival}\nIšvykimas: ${formData.departure}\n` +
    `Vardas: ${formData.name}\n${formData.message ? 'Pastaba: ' + formData.message : ''}`;
}

// mailto construction:
function buildMailtoLink(email, hotel, room, formData) {
  const subject = encodeURIComponent(`Rezervacija — ${room.name || 'Kambarys ' + room.number}, ${hotel.name}`);
  const body = encodeURIComponent(buildReservationMessage(hotel, room, formData));
  return `mailto:${email}?subject=${subject}&body=${body}`;
}
```

### Vanilla JS Drag-Drop Photo Reorder (HTML5 API)

The project uses Vanilla JS ES6 modules. The HTML5 Drag and Drop API is the right fit — no jQuery, no extra library.

```javascript
// Source: MDN HTML5 Drag and Drop API — established browser standard
// In public/modules/hotel-admin-module.js

function initDragDropReorder(container) {
  let dragSrcEl = null;

  container.querySelectorAll('.photo-item').forEach(item => {
    item.draggable = true;

    item.addEventListener('dragstart', (e) => {
      dragSrcEl = item;
      item.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
    });

    item.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      const target = e.currentTarget;
      if (target !== dragSrcEl) {
        const rect = target.getBoundingClientRect();
        const after = e.clientX > rect.left + rect.width / 2;
        container.insertBefore(dragSrcEl, after ? target.nextSibling : target);
      }
    });

    item.addEventListener('dragend', () => {
      item.classList.remove('dragging');
      // Debounced save
      clearTimeout(window._reorderTimer);
      window._reorderTimer = setTimeout(() => savePhotoOrder(container), 300);
    });
  });
}

async function savePhotoOrder(container) {
  const items = [...container.querySelectorAll('.photo-item')];
  const order = items.map((el, idx) => ({
    id: el.dataset.photoId,
    sort_order: idx
  }));
  await fetch(`/api/hotels/${currentSlug}/rooms/${currentRoomId}/photos/order`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', 'X-Session-ID': sessionId },
    body: JSON.stringify({ order })
  });
}
```

### Availability Traffic Light Logic

```javascript
// Frontend: hotel-module.js
function getAvailabilityDisplay(room) {
  if (room.availability_status === 'available') {
    return { color: '#22c55e', label: 'LAISVAS', cssClass: 'available' };
  }
  if (room.availability_status === 'occupied') {
    if (room.available_from) {
      const from = new Date(room.available_from);
      const daysUntil = Math.ceil((from - Date.now()) / (1000 * 60 * 60 * 24));
      if (daysUntil <= 14) {
        return {
          color: '#eab308',
          label: `Laisvas netrukus — nuo ${from.toLocaleDateString('lt-LT')}`,
          cssClass: 'soon'
        };
      }
      return {
        color: '#ef4444',
        label: `UŽIMTAS / Laisvas nuo: ${from.toLocaleDateString('lt-LT')}`,
        cssClass: 'occupied'
      };
    }
    return { color: '#ef4444', label: 'UŽIMTAS', cssClass: 'occupied' };
  }
  return { color: '#6b7280', label: 'Nežinoma', cssClass: 'unknown' };
}
```

### Extending injectMeta() for og:image Override

```javascript
// Extend injectMeta() in server/index.js — backward compatible
function injectMeta(baseHtml, { title, description, url, schemaType, extraSchema = '', ogImage = null }) {
  const safeTitle = title.replace(/"/g, '&quot;').substring(0, 70);
  const safeDesc = description.replace(/"/g, '&quot;').substring(0, 160);
  const imageUrl = ogImage || 'https://sekmes.lt/img/palanga-hero.jpg';
  const metaTags = `
    <title>${safeTitle}</title>
    <meta name="description" content="${safeDesc}">
    <link rel="canonical" href="${url}">
    <meta property="og:title" content="${safeTitle}">
    <meta property="og:description" content="${safeDesc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="${url}">
    <meta property="og:locale" content="lt_LT">
    <meta property="og:site_name" content="Pajūrio Portalas">
    <meta property="og:image" content="${imageUrl}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="${imageUrl}">
    ${extraSchema}`;
  let html = baseHtml.replace(/<title>.*?<\/title>/, '');
  html = html.replace('</head>', `${metaTags}\n</head>`);
  return html;
}
```

All existing callers omit `ogImage` so they continue to use the default hero image.

---

## Supabase Design

### Table + RLS Design

```sql
-- hotels table
CREATE TABLE hotels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  address TEXT,
  city TEXT DEFAULT 'Palanga',
  phone TEXT,
  whatsapp TEXT,  -- stored without + or spaces: "37061234567"
  created_at TIMESTAMPTZ DEFAULT now()
);

-- hotel_rooms table
CREATE TABLE hotel_rooms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  hotel_id UUID NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
  number INTEGER NOT NULL,
  name TEXT,
  price_per_night NUMERIC(8,2),
  area_m2 NUMERIC(5,1),
  sea_distance_m INTEGER,
  orientation TEXT CHECK (orientation IN ('N','NE','E','SE','S','SW','W','NW')),
  orientation_note TEXT,
  noise_level TEXT CHECK (noise_level IN ('quiet','moderate','lively')),
  availability_status TEXT NOT NULL DEFAULT 'available' CHECK (availability_status IN ('available','occupied')),
  available_from DATE,
  description TEXT,
  UNIQUE(hotel_id, number)
);

-- room_photos table
CREATE TABLE room_photos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id UUID NOT NULL REFERENCES hotel_rooms(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('window_view','interior')),
  sort_order INTEGER NOT NULL DEFAULT 0
);

-- RLS Policies
ALTER TABLE hotels ENABLE ROW LEVEL SECURITY;
ALTER TABLE hotel_rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE room_photos ENABLE ROW LEVEL SECURITY;

-- Public read (for public hotel pages)
CREATE POLICY "hotels_public_read" ON hotels FOR SELECT USING (true);
CREATE POLICY "hotel_rooms_public_read" ON hotel_rooms FOR SELECT USING (true);
CREATE POLICY "room_photos_public_read" ON room_photos FOR SELECT USING (true);

-- Owner write (uses auth.uid() from Supabase JWT)
CREATE POLICY "hotels_owner_insert" ON hotels FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "hotels_owner_update" ON hotels FOR UPDATE USING (auth.uid() = owner_id);
CREATE POLICY "hotels_owner_delete" ON hotels FOR DELETE USING (auth.uid() = owner_id);
-- hotel_rooms and room_photos: owner check via join to hotels
CREATE POLICY "hotel_rooms_owner_write" ON hotel_rooms
  FOR ALL USING (EXISTS (SELECT 1 FROM hotels WHERE hotels.id = hotel_id AND hotels.owner_id = auth.uid()));
CREATE POLICY "room_photos_owner_write" ON room_photos
  FOR ALL USING (EXISTS (
    SELECT 1 FROM hotel_rooms hr
    JOIN hotels h ON h.id = hr.hotel_id
    WHERE hr.id = room_id AND h.owner_id = auth.uid()
  ));
```

**Note:** The server uses `SUPABASE_SERVICE_ROLE_KEY` which bypasses RLS entirely. The RLS policies above protect direct Supabase client access (browser SDK calls). Server-side owner verification is done manually by checking `hotel.owner_id` in the route handler — as done throughout the project.

### Supabase Storage Bucket

```javascript
// hotel-image-service.js constructor — bucket auto-created on first use
this.bucketName = 'hotel-photos';
// Bucket config: public: true, fileSizeLimit: 5MB
// Path format: {hotel_id}/{room_id}/{type}-{sortOrder}-{uuid}.jpg
// Example: a1b2c3d4/e5f6a7b8/window_view-0-550e8400.jpg
```

Bucket name `hotel-photos` is separate from `user-images` (existing general uploads). This allows independent lifecycle management and clearer RLS scoping.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `requireAuthLevel(2)` (auth-middleware.js) | `requireUser` from requireRole.js | This project — migration in progress | requireUser has dual-system fallback built in; requireAuthLevel is marked @deprecated |
| Manual `og:image` hardcode in injectMeta | Parameterized `ogImage` field | Phase 5 (this work) | Hotel pages can show real room photo in social previews |
| `fit: 'cover'` (crop) | `fit: 'contain'` + black bg | Already in ImageUploadService | Full image visible, no crop; consistent across all upload types |

**Note on auth middleware:** The project has two parallel auth systems (sessionCore new + authMiddleware legacy). For hotel routes, `requireUser` is correct — it checks both `req.auth.role` (new) and `req.authContext.level >= 2` (legacy). This dual check is explicitly implemented in requireRole.js:59-71.

---

## Open Questions

1. **Owner identity linking to `hotels.owner_id`**
   - What we know: The project uses `user_sessions_enhanced` (legacy) and `sessions_core` (new) tables. The `owner_id` FK references `auth.users(id)` in the schema above, but the legacy system uses its own UUID-based session IDs.
   - What's unclear: Which ID to store as `owner_id` — Supabase auth UUID or the internal session/user ID from `user_sessions_enhanced`.
   - Recommendation: Store the session's `userId` from `req.authContext.userId` (legacy) or `req.auth.identityId` (new). Use a TEXT column (not UUID FK) for `owner_id` to avoid FK constraint failures during the auth system transition. Enforce ownership in application code, not DB constraint.

2. **`injectMeta()` modification scope**
   - What we know: The function is defined once in `server/index.js` and called in 4+ places. Adding an optional `ogImage` parameter is backward-compatible (all existing callers omit it, default is the hero image).
   - What's unclear: Whether the planner wants to modify this shared function or duplicate it for hotel use.
   - Recommendation: Modify `injectMeta()` with the optional `ogImage` parameter. Change is minimal (2 lines), backward-compatible, and benefits future SSR routes.

3. **QR PDF generation**
   - What we know: CONTEXT.md says "Download QR (PDF)". `qrcode` generates PNG/SVG/DataURL, not PDF.
   - What's unclear: Whether a true PDF is needed or a high-res PNG is acceptable.
   - Recommendation: Generate PNG (300×300) from `qrcode`. The browser's Print-to-PDF covers the "print and hang" use case. If true PDF is required, add `pdfkit` (not in dependencies), but that adds complexity. For MVP, PNG download is sufficient.

---

## Validation Architecture

`workflow.nyquist_validation` is absent from `.planning/config.json` — treat as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Playwright (already installed) |
| Config file | `agent-network/playwright.config.cjs` |
| Quick run command | `npx playwright test --project=chromium tests/hotel.spec.js` |
| Full suite command | `npx playwright test` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| HOTEL-01 | `/hotel/:slug` returns SSR HTML with `<title>` containing hotel name | Playwright smoke | `npx playwright test --project=chromium tests/hotel.spec.js::ssr-title` | ❌ Wave 0 |
| HOTEL-02 | `/hotel/:slug` HTML contains `<script type="application/ld+json">` with `LodgingBusiness` | Playwright smoke | `npx playwright test --project=chromium tests/hotel.spec.js::json-ld` | ❌ Wave 0 |
| HOTEL-03 | `POST /api/hotels` creates hotel, returns slug | API integration | `npx playwright test --project=chromium tests/hotel.spec.js::create-hotel` | ❌ Wave 0 |
| HOTEL-04 | `GET /hotel/:slug/admin` returns 401 without auth | Playwright auth | `npx playwright test --project=chromium tests/hotel.spec.js::admin-auth` | ❌ Wave 0 |
| HOTEL-05 | Room photo upload stores to `hotel-photos` bucket | API integration | `npx playwright test --project=chromium tests/hotel.spec.js::photo-upload` | ❌ Wave 0 |
| HOTEL-06 | QR endpoint `/api/hotels/:slug/rooms/:num/qr` returns PNG image | API smoke | `npx playwright test --project=chromium tests/hotel.spec.js::qr-png` | ❌ Wave 0 |
| HOTEL-07 | Availability traffic light shows yellow when available_from within 14 days | Unit | manual-only (date math logic unit test) | ❌ Wave 0 |
| HOTEL-08 | WhatsApp link format: `https://wa.me/{number}?text=...` | Unit | manual-only (URL format check) | ❌ Wave 0 |

**Note:** HOTEL-07 and HOTEL-08 can be tested as pure function unit tests in Node.js (`node -e`) without a browser.

### Sampling Rate
- **Per task commit:** `npx playwright test --project=chromium tests/hotel.spec.js`
- **Per wave merge:** `npx playwright test`
- **Phase gate:** Full Playwright suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `agent-network/tests/hotel.spec.js` — covers HOTEL-01 through HOTEL-06
- [ ] No new fixtures needed — existing `webServer` config in playwright.config.cjs handles server startup

---

## Sources

### Primary (HIGH confidence)
- Direct code read: `server/index.js:695-714` — exact `injectMeta()` signature and injection mechanism
- Direct code read: `server/services/image-upload-service.js` — exact resize, compress, upload pattern
- Direct code read: `server/routes/upload.js` — multer config, bucket name, processAndUploadImage call
- Direct code read: `server/middleware/requireRole.js` — requireUser dual-system implementation
- Direct code read: `server/middleware/auth-middleware.js` — requireAuthLevel marked @deprecated
- Direct code read: `server/utils/slug-generator.js` — generateSlug, ensureUniqueSlug signatures
- Direct code read: `server/routes/hotel-street-view.js` — WING_HEADINGS N/NE/E/SE/S/SW/W/NW constants
- `npm view qrcode version` → 1.5.4 (verified 2026-03-19)

### Secondary (MEDIUM confidence)
- Schema.org LodgingBusiness spec: https://schema.org/LodgingBusiness — LodgingBusiness, HotelRoom, amenityFeature, containsPlace
- Schema.org HotelRoom spec: https://schema.org/HotelRoom
- WhatsApp deep link format: https://faq.whatsapp.com/425747423114628 — wa.me/{number}?text={encoded}
- MDN HTML5 Drag and Drop API — draggable, dragstart, dragover, dragend events

### Tertiary (LOW confidence)
- None — all critical findings verified against code or official registry

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all dependencies verified against package.json and npm registry
- Architecture patterns: HIGH — derived directly from existing production code in the same codebase
- JSON-LD schema: MEDIUM — based on Schema.org spec; exact field set matches CONTEXT.md requirements
- Supabase RLS: MEDIUM — standard pattern, matches how other tables in project are structured
- QR generation: HIGH — npm version verified, API is stable since v1.x
- Pitfalls: HIGH — route ordering, og:image, auth deprecation all verified from code

**Research date:** 2026-03-19
**Valid until:** 2026-06-19 (stable stack — Node.js/Express/Supabase/Schema.org)
