#!/usr/bin/env python3
# Scrape info.lt — Lithuanian business directory with emails
# Pajūrio miestai × kategorijos
# Output: workspace/_tmp/infolt_raw.json

import json, re, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from scrapling.fetchers import Fetcher

OUTPUT = Path('d:/_PAL/benino/workspace/_tmp/infolt_raw.json')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
DELAY = 3.0  # polite — info.lt rate limits aggressively

fetcher = Fetcher()
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

# category_id/city combos from info.lt URL pattern:
# https://www.info.lt/rubrika/{Kategorija}/{cat_id}/{Miestas}
SOURCES = [
    # Kretinga — pilnas aprėptis
    ('Kretinga', 'restoranas',      'https://www.info.lt/rubrika/Restoranai/100209630/Kretinga'),
    ('Kretinga', 'kavinė',          'https://www.info.lt/rubrika/Kavin%C4%97s/100209549/Kretinga'),
    ('Kretinga', 'viešbutis',       'https://www.info.lt/rubrika/Vie%C5%A1bu%C4%8Diai-apgyvendinimas/100209681/Kretinga'),
    ('Kretinga', 'grožio salonas',  'https://www.info.lt/rubrika/Kirpyklos-gro%C5%BEio-salonai/100209553/Kretinga'),
    ('Kretinga', 'odontologas',     'https://www.info.lt/rubrika/Odontologai/100209605/Kretinga'),
    ('Kretinga', 'autoservisas',    'https://www.info.lt/rubrika/Autoserviso-paslaugos/100209521/Kretinga'),
    ('Kretinga', 'gydytojas',       'https://www.info.lt/rubrika/Gydytojai-klinikos/100209543/Kretinga'),
    ('Kretinga', 'parduotuvė',      'https://www.info.lt/rubrika/Maisto-preki%C5%B3-parduotuv%C4%97s/100209568/Kretinga'),
    # Palanga — trūkstami emailai
    ('Palanga',  'restoranas',      'https://www.info.lt/rubrika/Restoranai/100209630/Palanga'),
    ('Palanga',  'kavinė',          'https://www.info.lt/rubrika/Kavin%C4%97s/100209549/Palanga'),
    ('Palanga',  'grožio salonas',  'https://www.info.lt/rubrika/Kirpyklos-gro%C5%BEio-salonai/100209553/Palanga'),
    ('Palanga',  'viešbutis',       'https://www.info.lt/rubrika/Vie%C5%A1bu%C4%8Diai-apgyvendinimas/100209681/Palanga'),
    # Neringa/Nida
    ('Neringa',  'restoranas',      'https://www.info.lt/rubrika/Restoranai/100209630/Neringa'),
    ('Neringa',  'viešbutis',       'https://www.info.lt/rubrika/Vie%C5%A1bu%C4%8Diai-apgyvendinimas/100209681/Neringa'),
    # Šventoji
    ('Šventoji', 'viešbutis',       'https://www.info.lt/rubrika/Vie%C5%A1bu%C4%8Diai-apgyvendinimas/100209681/%C5%A0ventoji'),
]

def extract_email(html):
    found = EMAIL_RE.findall(html or '')
    found = [e for e in found
             if not any(e.endswith(x) for x in ['.png','.jpg','.css','.js'])
             and 'example' not in e and '@2x' not in e]
    return found[0] if found else None

def scrape_listing(city, category, url):
    print(f'\n[{city}] {category}')
    time.sleep(DELAY)
    try:
        page = fetcher.get(url)
        if page.status == 429:
            print(f'  429 rate limit — waiting 30s...')
            time.sleep(30)
            page = fetcher.get(url)
        if page.status != 200:
            print(f'  Status {page.status} — skip')
            return []
        print(f'  OK ({len(page.html_content)} bytes)')
    except Exception as e:
        print(f'  ERROR: {e}')
        return []

    results = []
    # info.lt listing cards
    cards = page.css('.company-item, .listing-item, .firm, .company, article.item')
    if not cards:
        # Try links to individual business pages
        links = page.css('a.company-name, a.firm-name, h2 a, h3 a, .title a')
        print(f'  Cards: 0, Links: {len(links)}')
        for lnk in links:
            name = lnk.text.strip()
            href = lnk.attrib.get('href', '')
            if name and len(name) > 2:
                results.append({'name': name, 'city': city, 'category': category,
                                 'detail_url': href, 'source': 'info.lt'})
    else:
        print(f'  Cards: {len(cards)}')
        for card in cards:
            name_el = card.css('h2, h3, .company-name, .title, .name')
            link_el = card.css('a')
            phone_el = card.css('.phone, [href^="tel:"]')
            web_el = card.css('.website a, a[href^="http"]:not([href*="info.lt"])')
            email_el = card.css('a[href^="mailto:"]')

            name = name_el[0].text.strip() if name_el else ''
            href = link_el[0].attrib.get('href','') if link_el else ''
            phone = phone_el[0].text.strip() if phone_el else ''
            website = web_el[0].attrib.get('href','') if web_el else ''
            email = email_el[0].attrib.get('href','').replace('mailto:','') if email_el else ''
            if not email:
                email = extract_email(card.html_content)

            if name:
                results.append({
                    'name': name, 'city': city, 'category': category,
                    'detail_url': href, 'phone': phone, 'website': website,
                    'email': email, 'source': 'info.lt',
                })

    print(f'  → {len(results)} entries')
    return results

# ─── Fetch detail pages for missing info ─────────────────────────────────────
def enrich_detail(entry):
    url = entry.get('detail_url', '')
    if not url or not url.startswith('http') or entry.get('email'):
        return entry
    if 'info.lt' not in url:
        return entry
    try:
        time.sleep(DELAY)
        page = fetcher.get(url)
        if page.status != 200:
            return entry
        email_el = page.css('a[href^="mailto:"]')
        if email_el:
            entry['email'] = email_el[0].attrib.get('href','').replace('mailto:','')
        else:
            entry['email'] = extract_email(page.html_content)
        phone_el = page.css('[href^="tel:"]')
        if phone_el and not entry.get('phone'):
            entry['phone'] = phone_el[0].attrib.get('href','').replace('tel:','')
        web_el = page.css('a[href^="http"]:not([href*="info.lt"])')
        if web_el and not entry.get('website'):
            entry['website'] = web_el[0].attrib.get('href','')
    except Exception:
        pass
    return entry

# ─── Main ─────────────────────────────────────────────────────────────────────
all_results = []
if OUTPUT.exists():
    all_results = json.loads(OUTPUT.read_text(encoding='utf-8'))
    done_keys = {(r['city'], r['category']) for r in all_results}
    print(f'Resuming — {len(all_results)} already collected')
else:
    done_keys = set()

for city, category, url in SOURCES:
    if (city, category) in done_keys:
        print(f'  Skip (done): [{city}] {category}')
        continue
    entries = scrape_listing(city, category, url)
    # Enrich detail pages
    for i, entry in enumerate(entries):
        if not entry.get('email') and entry.get('detail_url','').startswith('http'):
            print(f'  detail [{i+1}/{len(entries)}] {entry["name"][:35]}...', end=' ')
            entry = enrich_detail(entry)
            print('✅' if entry.get('email') else '—')
    all_results.extend(entries)
    OUTPUT.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')

emails = sum(1 for e in all_results if e.get('email'))
print(f'\n✅ Done: {len(all_results)} entries, {emails} emails → {OUTPUT}')
