#!/usr/bin/env python3
# Scrape aplankykkretinga.lt — visi verslo sąrašai
# Output: workspace/_tmp/kretinga_raw.json

import json, re, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from scrapling.fetchers import Fetcher

OUTPUT = Path('d:/_PAL/benino/workspace/_tmp/kretinga_raw.json')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
DELAY = 1.0
fetcher = Fetcher()
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

SOURCES = [
    ('Kretinga', 'restoranas',      'https://aplankykkretinga.lt/kur-pavalgyti/'),
    ('Kretinga', 'viešbutis',       'https://aplankykkretinga.lt/kur-apsistoti/'),
    ('Kretinga', 'pramogos',        'https://aplankykkretinga.lt/ka-veikti/aktyvus-laisvalaikis/'),
    ('Kretinga', 'lankytinos',      'https://aplankykkretinga.lt/ka-veikti/lankytinos-vietos/'),
]

def extract_email(html):
    found = EMAIL_RE.findall(html or '')
    return next((e for e in found if not any(e.endswith(x) for x in ['.png','.jpg','.css','.js'])
                 and 'example' not in e), None)

def scrape_page(city, category, url):
    print(f'\n[{city}] {category}')
    try:
        page = fetcher.get(url)
        print(f'  Status: {page.status}, Length: {len(page.html_content)}')
        if page.status != 200: return []
    except Exception as e:
        print(f'  ERROR: {e}'); return []

    cards = page.css('.archive-item')
    print(f'  Cards: {len(cards)}')
    results = []
    for card in cards:
        link = card.css('a')
        name_el = card.css('h5 a, h2 a, h3 a, h4 a, .archive-item__title a')
        href = link[0].attrib.get('href','') if link else ''
        name = name_el[0].text.strip() if name_el else ''
        if not name:  # fallback: any link with text
            name = next((a.text.strip() for a in card.css('a') if a.text and len(a.text.strip()) > 2), '')
        if name and len(name) > 2:
            results.append({'name': name, 'city': city, 'category': category,
                            'detail_url': href, 'source': 'aplankykkretinga.lt'})
    return results

def enrich(entry):
    url = entry.get('detail_url', '')
    if not url or not url.startswith('http'): return entry
    time.sleep(DELAY)
    try:
        page = fetcher.get(url)
        if page.status != 200: return entry
        # Email
        mailto = page.css('a[href^="mailto:"]')
        if mailto:
            entry['email'] = mailto[0].attrib.get('href','').replace('mailto:','')
        else:
            entry['email'] = extract_email(page.html_content)
        # Phone
        tel = page.css('a[href^="tel:"]')
        if tel: entry['phone'] = tel[0].attrib.get('href','').replace('tel:','')
        # Website
        for a in page.css('a[href^="http"]'):
            h = a.attrib.get('href','')
            if h and 'aplankykkretinga' not in h and 'facebook' not in h and 'google' not in h:
                entry['website'] = h
                break
        # Address — look for structured address text
        addr_el = page.css('.contact-info, .address, address, .entry-content p')
        if addr_el:
            txt = addr_el[0].text.strip()
            if len(txt) > 5 and len(txt) < 100:
                entry['address'] = txt
    except Exception:
        pass
    return entry

all_results = []
for city, category, url in SOURCES:
    entries = scrape_page(city, category, url)
    for i, entry in enumerate(entries):
        print(f'  [{i+1}/{len(entries)}] {entry["name"][:40]}', end=' ')
        entry = enrich(entry)
        markers = ('✉' if entry.get('email') else '') + ('🌐' if entry.get('website') else '') + ('📞' if entry.get('phone') else '')
        print(markers or '—')
    all_results.extend(entries)
    time.sleep(DELAY)

OUTPUT.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')
emails   = sum(1 for e in all_results if e.get('email'))
websites = sum(1 for e in all_results if e.get('website'))
print(f'\nDone: {len(all_results)} entries | {emails} emails | {websites} websites -> {OUTPUT}')
