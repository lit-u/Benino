#!/usr/bin/env python3
# Merge priejuros.lt scraped data into existing JSON catalogs
# Dedup by website URL (most reliable) then by name+city fuzzy match
# New entries go into new category files per city

import json, re, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from scrapling.fetchers import Fetcher

DATA_DIR  = Path('d:/_PAL/benino/agent-network/public/data')
RAW_FILE  = Path('d:/_PAL/benino/workspace/_tmp/priejuros_raw.json')
OUT_FILE  = Path('d:/_PAL/benino/workspace/_tmp/merge_report.json')

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

def to_slug(s):
    s = s.lower().strip()
    s = re.sub(r'[āàáâã]','a', s)
    s = re.sub(r'[čć]','c', s)
    s = re.sub(r'[ę]','e', s)
    s = re.sub(r'[ėéê]','e', s)
    s = re.sub(r'[įī]','i', s)
    s = re.sub(r'[š]','s', s)
    s = re.sub(r'[ų]','u', s)
    s = re.sub(r'[ū]','u', s)
    s = re.sub(r'[ž]','z', s)
    s = re.sub(r'[^a-z0-9]+','-', s)
    return s.strip('-')[:60]

def normalize_url(url):
    """Strip protocol, www, trailing slash for comparison."""
    if not url: return ''
    url = re.sub(r'^https?://(www\.)?','', url.lower())
    return url.rstrip('/')

def extract_email_from_page(url, fetcher, delay=0.8):
    """Try to scrape email from business website."""
    if not url or not url.startswith('http'):
        return None
    try:
        time.sleep(delay)
        page = fetcher.get(url)
        if page.status != 200:
            return None
        found = EMAIL_RE.findall(page.html_content)
        found = [e for e in found
                 if not any(e.endswith(x) for x in ['.png','.jpg','.css','.js'])
                 and 'example' not in e and '@2x' not in e]
        if found: return found[0]
        # Try /kontaktai
        kontaktai = url.rstrip('/') + '/kontaktai'
        time.sleep(delay)
        page2 = fetcher.get(kontaktai)
        if page2.status == 200:
            found2 = EMAIL_RE.findall(page2.html_content)
            found2 = [e for e in found2
                      if not any(e.endswith(x) for x in ['.png','.jpg','.css','.js'])
                      and 'example' not in e]
            if found2: return found2[0]
    except Exception:
        pass
    return None

# ─── Load raw data ────────────────────────────────────────────────────────────
raw = json.loads(RAW_FILE.read_text(encoding='utf-8'))
print(f'Raw priejuros entries: {len(raw)}')

# ─── Load existing data ───────────────────────────────────────────────────────
existing_files = {
    'hotels':    json.loads((DATA_DIR/'hotels.json').read_text(encoding='utf-8')),
    'kavines':   json.loads((DATA_DIR/'kavines.json').read_text(encoding='utf-8')),
    'paslaugos': json.loads((DATA_DIR/'paslaugos.json').read_text(encoding='utf-8')),
    'sveikatos': json.loads((DATA_DIR/'sveikatos.json').read_text(encoding='utf-8')),
}

# Build lookup sets
existing_urls = set()
existing_names = set()
for fname, fdata in existing_files.items():
    for city, places in fdata.items():
        for p in places:
            if p.get('website'): existing_urls.add(normalize_url(p['website']))
            existing_names.add(to_slug(p['name']))

print(f'Existing entries with URL: {len(existing_urls)}')
print(f'Existing entries total names: {len(existing_names)}')

# ─── Category mapping ─────────────────────────────────────────────────────────
CAT_MAP = {
    'viešbutis':    'hotels',
    'svečių namai': 'hotels',
    'apartamentai': 'hotels',
    'restoranas':   'kavines',
    'kavinė':       'kavines',
    'spa':          'paslaugos',
}

# ─── Determine new vs existing ────────────────────────────────────────────────
new_entries = []
duplicates  = []
fetcher = Fetcher()

for entry in raw:
    norm_url  = normalize_url(entry.get('website',''))
    norm_name = to_slug(entry.get('name',''))

    if norm_url and norm_url in existing_urls:
        duplicates.append({'name': entry['name'], 'reason': 'url_match'})
        continue
    if norm_name in existing_names:
        duplicates.append({'name': entry['name'], 'reason': 'name_match'})
        continue

    # New entry — enrich email if missing
    email = entry.get('email')
    if not email and entry.get('website'):
        print(f'  Fetching email: {entry["name"][:40]}...', end=' ')
        email = extract_email_from_page(entry['website'], fetcher)
        if email:
            print(f'✅ {email}')
        else:
            print('—')
        entry['email'] = email

    new_entries.append(entry)

print(f'\nNew entries: {len(new_entries)}')
print(f'Duplicates:  {len(duplicates)}')

# ─── Build new JSON structure ─────────────────────────────────────────────────
# Map to target file
new_by_file = {'hotels': {}, 'kavines': {}, 'paslaugos': {}, 'sveikatos': {}}

for entry in new_entries:
    cat  = entry.get('category','')
    city = entry.get('city','Kita')
    target_file = CAT_MAP.get(cat, 'paslaugos')

    slug = to_slug(entry['name'])
    # Ensure unique slug
    base_slug = slug
    n = 2
    while slug in existing_names:
        slug = f'{base_slug}-{n}'
        n += 1
    existing_names.add(slug)

    record = {
        'name':       entry['name'],
        'nickname':   slug,
        'type':       cat,
        'address':    entry.get('address', ''),
        'phone':      entry.get('phone', ''),
        'website':    entry.get('website', ''),
        'email':      entry.get('email', ''),
        'city':       city,
        'has_account': False,
        'source':     'priejuros.lt',
    }

    if city not in new_by_file[target_file]:
        new_by_file[target_file][city] = []
    new_by_file[target_file][target_file == 'hotels' and city or city].append(record)
    new_by_file[target_file].setdefault(city, []).append(record)

# Fix duplicate append bug above
for fname in new_by_file:
    for city in new_by_file[fname]:
        seen = set()
        deduped = []
        for r in new_by_file[fname][city]:
            if r['nickname'] not in seen:
                seen.add(r['nickname'])
                deduped.append(r)
        new_by_file[fname][city] = deduped

# ─── Merge into existing files ────────────────────────────────────────────────
total_added = 0
for fname, new_data in new_by_file.items():
    existing = existing_files[fname]
    added = 0
    for city, places in new_data.items():
        if city not in existing:
            existing[city] = []
        existing[city].extend(places)
        added += len(places)
    if added:
        out_path = DATA_DIR / f'{fname}.json'
        out_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'  {fname}.json: +{added} entries')
        total_added += added

print(f'\n✅ Total added: {total_added}')
print(f'   Duplicates skipped: {len(duplicates)}')

# ─── Generate profile.md for new entries ─────────────────────────────────────
MEMBERS_DIR = Path('d:/_PAL/benino/workspace/members')
profiles_created = 0
for fname, new_data in new_by_file.items():
    for city, places in new_data.items():
        for p in places:
            nick = p['nickname']
            profile_dir = MEMBERS_DIR / nick
            profile_dir.mkdir(parents=True, exist_ok=True)
            profile_path = profile_dir / 'profile.md'
            if not profile_path.exists():
                lines = [
                    f'# {p["name"]}',
                    f'',
                    f'**Nickname:** {nick}  ',
                    f'**Miestas:** {city}  ',
                    f'**Adresas:** {p.get("address","")}  ',
                    f'',
                    f'## {p["type"].capitalize() if p["type"] else "Paslaugos"}',
                    f'',
                    f'- **Tel.:** {p.get("phone","")}',
                    f'- **Web:** {p.get("website","")}',
                    f'- **Email:** {p.get("email","")}',
                    f'',
                    f'## Nuorodos & Naujienos',
                    f'',
                    f'## Pastabos',
                ]
                profile_path.write_text('\n'.join(lines), encoding='utf-8')
                profiles_created += 1

print(f'   Profile.md sukurta: {profiles_created}')

# Save report
OUT_FILE.write_text(json.dumps({
    'total_raw': len(raw),
    'new_added': total_added,
    'duplicates': len(duplicates),
    'profiles_created': profiles_created,
    'new_entries': new_entries[:20],  # sample
}, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'\n   Report: {OUT_FILE}')
