#!/usr/bin/env python3
# Scrape visitneringa.com — Neringos turizmo katalogas
# Output: workspace/_tmp/visitneringa_raw.json

import json, time, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from scrapling.fetchers import Fetcher

fetcher = Fetcher()
OUTPUT = Path('d:/_PAL/benino/workspace/_tmp/visitneringa_raw.json')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
DELAY = 1.0

SOURCES = [
    ('Neringa', 'viesbutis',    'https://www.visitneringa.com/lt/kur-apsistoti/'),
    ('Neringa', 'restoranas',   'https://www.visitneringa.com/lt/maitinimas/'),
    ('Neringa', 'spa',          'https://www.visitneringa.com/lt/ka-nuveikti/spa-ir-sveikata/'),
    ('Neringa', 'pramogos',     'https://www.visitneringa.com/lt/ka-nuveikti/aktyvus-poilsis/'),
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

    # Try common listing patterns
    for selector in ['article', '.listing', '.entry', '.card', '.item', 'li.post', '.accommodation', '.restaurant']:
        cards = page.css(selector)
        if len(cards) > 2:
            print(f'  Found {len(cards)} cards via "{selector}"')
            for card in cards:
                links = card.css('a')
                name_el = card.css('h2, h3, h4, .title, .name')
                name = name_el[0].text.strip() if name_el else (links[0].text.strip() if links else '')
                href = links[0].attrib.get('href','') if links else ''
                if name and len(name) > 2:
                    results.append({
                        'name': name,
                        'city': city,
                        'category': category,
                        'detail_url': href,
                        'source': 'visitneringa.com',
                    })
            break

    # Fallback: all internal links
    if not results:
        links = page.css(f'a[href*="visitneringa.com"], a[href^="/lt/"]')
        seen = set()
        for lnk in links:
            href = lnk.attrib.get('href','')
            name = lnk.text.strip()
            if name and len(name) > 3 and href not in seen and href != url:
                seen.add(href)
                results.append({
                    'name': name, 'city': city, 'category': category,
                    'detail_url': href, 'source': 'visitneringa.com',
                })
        print(f'  Fallback: {len(results)} links')

    return results

all_results = []
for city, category, url in SOURCES:
    entries = scrape_page(city, category, url)
    # Fetch detail pages
    for i, entry in enumerate(entries):
        durl = entry.get('detail_url','')
        if not durl or not durl.startswith('http'):
            if durl.startswith('/'):
                durl = 'https://www.visitneringa.com' + durl
                entry['detail_url'] = durl
            else:
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
                    if h and 'visitneringa' not in h and 'facebook' not in h:
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
