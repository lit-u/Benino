#!/usr/bin/env python3
# Scrape klaipedatravel.lt — Klaipėdos turizmo katalogas
# Output: workspace/_tmp/klaipedatravel_raw.json

import json, time, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from scrapling.fetchers import Fetcher

fetcher = Fetcher()
OUTPUT = Path('d:/_PAL/benino/workspace/_tmp/klaipedatravel_raw.json')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
DELAY = 1.0

SOURCES = [
    ('Klaipėda', 'viesbutis',   'https://klaipedatravel.lt/en/accommodation/'),
    ('Klaipėda', 'restoranas',  'https://klaipedatravel.lt/en/restaurants-and-cafes/'),
    ('Klaipėda', 'spa',         'https://klaipedatravel.lt/en/spa-wellness/'),
    ('Klaipėda', 'pramogos',    'https://klaipedatravel.lt/en/what-to-do/'),
]

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

def extract_email(html):
    found = EMAIL_RE.findall(html or '')
    found = [e for e in found if not any(e.endswith(x) for x in ['.png','.jpg','.css','.js'])
             and 'example' not in e and '@2x' not in e and e.split('@')[1].count('.') >= 1]
    return found[0] if found else None

def scrape_page(city, category, url):
    print(f'\n[{city}] {category} -> {url}')
    try:
        page = fetcher.get(url)
        print(f'  Status: {page.status}, Length: {len(page.html_content)}')
        if page.status != 200:
            return []
    except Exception as e:
        print(f'  ERROR: {e}')
        return []

    results = []
    for selector in ['article', '.listing-item', '.card', '.entry', '.business', '.venue', 'li.post']:
        cards = page.css(selector)
        if len(cards) > 2:
            print(f'  Found {len(cards)} cards via "{selector}"')
            for card in cards:
                links = card.css('a')
                name_el = card.css('h2, h3, h4, .title, .name, .entry-title')
                name = name_el[0].text.strip() if name_el else (links[0].text.strip() if links else '')
                href = links[0].attrib.get('href','') if links else ''
                if name and len(name) > 2:
                    results.append({
                        'name': name, 'city': city, 'category': category,
                        'detail_url': href, 'source': 'klaipedatravel.lt',
                    })
            break

    if not results:
        # Fallback: links with internal paths
        links = page.css('a[href*="klaipedatravel"]')
        seen = set()
        for lnk in links:
            href = lnk.attrib.get('href','')
            name = lnk.text.strip()
            if name and len(name) > 3 and href not in seen and href != url:
                seen.add(href)
                results.append({
                    'name': name, 'city': city, 'category': category,
                    'detail_url': href, 'source': 'klaipedatravel.lt',
                })
        print(f'  Fallback: {len(results)} links')

    return results

all_results = []
for city, category, url in SOURCES:
    entries = scrape_page(city, category, url)
    for i, entry in enumerate(entries):
        durl = entry.get('detail_url','')
        if not durl or not durl.startswith('http'):
            continue
        time.sleep(DELAY)
        try:
            dp = fetcher.get(durl)
            if dp.status == 200:
                email = extract_email(dp.html_content)
                if email: entry['email'] = email
                phone_els = dp.css('[href^="tel:"]')
                if phone_els: entry['phone'] = phone_els[0].attrib.get('href','').replace('tel:','')
                web_els = dp.css('a[href^="http"]')
                for w in web_els:
                    h = w.attrib.get('href','')
                    if h and 'klaipedatravel' not in h and 'facebook' not in h and 'google' not in h:
                        entry['website'] = h
                        break
        except Exception:
            pass
        print(f'  [{i+1}/{len(entries)}] {entry["name"][:40]} {"[email]" if entry.get("email") else ""}')
    all_results.extend(entries)
    time.sleep(DELAY)

OUTPUT.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')
emails = sum(1 for e in all_results if e.get('email'))
print(f'\nDone: {len(all_results)} entries, {emails} emails -> {OUTPUT}')
