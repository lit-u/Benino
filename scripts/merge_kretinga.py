#!/usr/bin/env python3
# Clean + merge aplankykkretinga.lt data into catalogs
# Filters out: lankytinos vietos, fake TIC emails, browsehappy.com

import json, re, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from scrapling.fetchers import Fetcher

DATA_DIR  = Path('d:/_PAL/benino/agent-network/public/data')
RAW_FILE  = Path('d:/_PAL/benino/workspace/_tmp/kretinga_raw.json')
MEMBERS_DIR = Path('d:/_PAL/benino/workspace/members')
DELAY = 1.2

fetcher = Fetcher()
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

FAKE_EMAILS = {'tic@kretingosturizmas.info', 'info@example.com'}
FAKE_URLS   = {'http://browsehappy.com/', 'https://browsehappy.com/'}

CAT_MAP = {
    'restoranas': 'kavines',
    'viešbutis':  'hotels',
    'pramogos':   'paslaugos',
}

def to_slug(s):
    s = s.lower().strip()
    for a,b in [('ą','a'),('č','c'),('ę','e'),('ė','e'),('į','i'),('š','s'),('ų','u'),('ū','u'),('ž','z')]:
        s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')[:60]

def clean_email(e):
    if not e or e in FAKE_EMAILS: return None
    return e

def clean_url(u):
    if not u or u in FAKE_URLS: return None
    return u

def scrape_business_email(detail_url):
    """Fetch the aplankykkretinga detail page for real contact info."""
    if not detail_url or not detail_url.startswith('http'): return {}
    try:
        time.sleep(DELAY)
        page = fetcher.get(detail_url)
        if page.status != 200: return {}
        result = {}
        # Look for real external website link
        for a in page.css('a[href^="http"]'):
            h = a.attrib.get('href','')
            if h and 'aplankykkretinga' not in h and 'browsehappy' not in h and 'facebook' not in h and 'google' not in h:
                result['website'] = h
                break
        # Phone
        tel = page.css('a[href^="tel:"]')
        if tel: result['phone'] = tel[0].attrib.get('href','').replace('tel:','')
        # Real email (not TIC)
        for a in page.css('a[href^="mailto:"]'):
            e = a.attrib.get('href','').replace('mailto:','')
            if e and e not in FAKE_EMAILS:
                result['email'] = e
                break
        # Also scan text for emails
        if not result.get('email'):
            found = EMAIL_RE.findall(page.html_content)
            for e in found:
                if e not in FAKE_EMAILS and not any(e.endswith(x) for x in ['.png','.jpg','.css','.js']):
                    result['email'] = e
                    break
        return result
    except Exception:
        return {}

# ─── Load and clean raw data ──────────────────────────────────────────────────
raw = json.loads(RAW_FILE.read_text(encoding='utf-8'))
# Filter: only businesses, not tourist attractions
businesses = [d for d in raw if d['category'] != 'lankytinos']
print(f'Raw: {len(raw)} | Businesses (ex. lankytinos): {len(businesses)}')
from collections import Counter
print('By category:', dict(Counter(d['category'] for d in businesses)))

# ─── Load existing slugs ──────────────────────────────────────────────────────
existing_files = {k: json.loads((DATA_DIR/f'{k}.json').read_text(encoding='utf-8'))
                  for k in ['hotels','kavines','paslaugos','sveikatos']}
existing_slugs = set()
existing_urls  = set()
for fd in existing_files.values():
    for city, places in fd.items():
        for p in places:
            existing_slugs.add(to_slug(p['name']))
            if p.get('website'): existing_urls.add(re.sub(r'^https?://(www\.)?','',p['website'].lower()).rstrip('/'))

# ─── Process each business ────────────────────────────────────────────────────
new_entries = []
for i, biz in enumerate(businesses):
    slug = to_slug(biz['name'])
    if slug in existing_slugs:
        print(f'  [{i+1}] SKIP (exists): {biz["name"][:40]}')
        continue

    print(f'  [{i+1}/{len(businesses)}] {biz["name"][:40]}', end=' ')

    # Scrape real contact from detail page
    contacts = scrape_business_email(biz.get('detail_url',''))
    website = clean_url(contacts.get('website') or biz.get('website'))
    email   = clean_email(contacts.get('email')  or biz.get('email'))
    phone   = contacts.get('phone') or biz.get('phone','')

    # Check URL dedup
    if website:
        norm = re.sub(r'^https?://(www\.)?','',website.lower()).rstrip('/')
        if norm in existing_urls:
            print(f'SKIP (url dup)')
            continue
        existing_urls.add(norm)

    existing_slugs.add(slug)
    record = {
        'name':       biz['name'],
        'nickname':   slug,
        'type':       biz['category'],
        'address':    biz.get('address',''),
        'phone':      phone,
        'website':    website or '',
        'email':      email or '',
        'city':       'Kretinga',
        'has_account': False,
        'source':     'aplankykkretinga.lt',
    }
    new_entries.append(record)
    markers = ('✉' if email else '') + ('🌐' if website else '') + ('📞' if phone else '')
    print(markers or '—')

print(f'\nNew entries to add: {len(new_entries)}')

# ─── Merge into JSON files ────────────────────────────────────────────────────
for record in new_entries:
    target = CAT_MAP.get(record['type'], 'paslaugos')
    existing_files[target].setdefault('Kretinga', []).append(record)

total_added = 0
for fname, data in existing_files.items():
    # Count new Kretinga entries
    kret = [p for p in data.get('Kretinga',[]) if p.get('source') == 'aplankykkretinga.lt']
    if kret:
        (DATA_DIR/f'{fname}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'  {fname}.json: +{len(kret)} Kretinga entries')
        total_added += len(kret)

# ─── Create profile.md files ──────────────────────────────────────────────────
profiles = 0
for r in new_entries:
    d = MEMBERS_DIR / r['nickname']
    d.mkdir(parents=True, exist_ok=True)
    p = d / 'profile.md'
    if not p.exists():
        p.write_text('\n'.join([
            f'# {r["name"]}', '',
            f'**Nickname:** {r["nickname"]}  ',
            f'**Miestas:** Kretinga  ',
            f'**Adresas:** {r.get("address","")}  ', '',
            f'## {r["type"].capitalize()}', '',
            f'- **Tel.:** {r.get("phone","")}',
            f'- **Web:** {r.get("website","")}',
            f'- **Email:** {r.get("email","")}', '',
            f'## Nuorodos & Naujienos', '',
            f'## Pastabos',
        ]), encoding='utf-8')
        profiles += 1

print(f'\n✅ Viso pridėta: {total_added} | Profiliai: {profiles}')
