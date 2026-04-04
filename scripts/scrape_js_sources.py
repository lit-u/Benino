#!/usr/bin/env python3
# Scrape JS-rendered pages: visitneringa.com + klaipedatravel.lt
# Uses PlaywrightFetcher for full JS execution
# Output: workspace/_tmp/visitneringa_raw.json, klaipedatravel_raw.json

import json, time, re, sys, io, asyncio
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from scrapling.fetchers import DynamicFetcher

OUTPUT_DIR = Path('d:/_PAL/benino/workspace/_tmp')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DELAY = 1.5

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

def extract_email(html):
    found = EMAIL_RE.findall(html or '')
    found = [e for e in found if not any(e.endswith(x) for x in ['.png','.jpg','.css','.js'])
             and 'example' not in e and '@2x' not in e]
    return found[0] if found else None

SOURCES = {
    'visitneringa_raw.json': [
        ('Neringa', 'viesbutis',  'https://www.visitneringa.com/lt/kur-apsistoti/',
         'article, .accommodation, .listing, .post, .object, li.item'),
        ('Neringa', 'restoranas', 'https://www.visitneringa.com/lt/maitinimas/',
         'article, .restaurant, .listing, .post, li.item'),
    ],
    'klaipedatravel_raw.json': [
        ('Klaipėda', 'viesbutis',   'https://klaipedatravel.lt/en/accommodation/',
         'article, .hotel, .listing, .entry, .card, .post'),
        ('Klaipėda', 'restoranas',  'https://klaipedatravel.lt/en/restaurants-and-cafes/',
         'article, .restaurant, .listing, .entry, .card, .post'),
        ('Klaipėda', 'spa',         'https://klaipedatravel.lt/lt/spa-ir-gerove/',
         'article, .spa, .listing, .entry, .card'),
    ],
}

def scrape_with_playwright(url, selector, city, category):
    print(f'  [{city}] {category}: {url}')
    try:
        fetcher = DynamicFetcher()
        page = fetcher.fetch(url, headless=True, wait=3000, network_idle=True)
        print(f'    Status: {page.status}, Length: {len(page.html_content)}')
        if page.status != 200:
            return []
    except Exception as e:
        print(f'    ERROR: {e}')
        return []

    results = []
    for sel in selector.split(','):
        sel = sel.strip()
        cards = page.css(sel)
        if len(cards) > 2:
            print(f'    Found {len(cards)} cards via "{sel}"')
            for card in cards:
                links = card.css('a')
                name_el = card.css('h1, h2, h3, h4, .title, .name, .entry-title')
                name = name_el[0].text.strip() if name_el else (links[0].text.strip() if links else '')
                href = links[0].attrib.get('href','') if links else ''
                email_in_card = extract_email(card.html_content)
                if name and len(name) > 2:
                    results.append({
                        'name': name, 'city': city, 'category': category,
                        'detail_url': href, 'source': url.split('/')[2],
                        'email': email_in_card,
                    })
            break

    # Fallback: all links with titles
    if not results:
        links = page.css('a[href]')
        domain = url.split('/')[2]
        seen = set()
        for lnk in links:
            href = lnk.attrib.get('href','')
            name = lnk.text.strip()
            if (name and len(name) > 3 and href not in seen and href != url
                    and (domain in href or href.startswith('/'))):
                seen.add(href)
                results.append({
                    'name': name, 'city': city, 'category': category,
                    'detail_url': href, 'source': domain,
                })
        print(f'    Fallback: {len(results)} links')

    return results

for output_file, sources in SOURCES.items():
    all_results = []
    for city, category, url, selector in sources:
        entries = scrape_with_playwright(url, selector, city, category)
        all_results.extend(entries)
        time.sleep(DELAY)

    out_path = OUTPUT_DIR / output_file
    out_path.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')
    emails = sum(1 for e in all_results if e.get('email'))
    print(f'\n  -> {len(all_results)} entries, {emails} emails: {out_path}\n')

print('Done!')
