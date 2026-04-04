#!/usr/bin/env python3
# Scrape priejuros.lt — pajūrio apgyvendinimo ir pramogų katalogas
# Scrapes: viešbučiai, restoranai, SPA, kavinės per miestus
# Output: workspace/_tmp/priejuros_raw.json

import json, time, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from scrapling.fetchers import Fetcher

fetcher = Fetcher()
OUTPUT = Path('d:/_PAL/benino/workspace/_tmp/priejuros_raw.json')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

DELAY = 1.0  # polite delay between requests

SOURCES = [
    # (city, category_label, url)
    ('Palanga', 'viešbutis',   'https://www.priejuros.lt/lt/poilsis-nuoma/palangoje/viesbuciai/'),
    ('Palanga', 'svečių namai','https://www.priejuros.lt/lt/poilsis-nuoma/palangoje/sveciu-namai/'),
    ('Palanga', 'apartamentai','https://www.priejuros.lt/lt/poilsis-nuoma/palangoje/apartamentai/'),
    ('Šventoji','viešbutis',   'https://www.priejuros.lt/lt/poilsis-nuoma/sventojoje/viesbuciai/'),
    ('Šventoji','svečių namai','https://www.priejuros.lt/lt/poilsis-nuoma/sventojoje/sveciu-namai/'),
    ('Klaipėda','viešbutis',   'https://www.priejuros.lt/lt/poilsis-nuoma/klaipedoje/viesbuciai/'),
    ('Neringa', 'viešbutis',   'https://www.priejuros.lt/lt/poilsis-nuoma/neringoje/viesbuciai/'),
    ('Neringa', 'svečių namai','https://www.priejuros.lt/lt/poilsis-nuoma/neringoje/sveciu-namai/'),
    ('Kretinga','viešbutis',   'https://www.priejuros.lt/lt/poilsis-nuoma/kretingoje/'),
    ('Palanga', 'restoranas',  'https://www.priejuros.lt/lt/pramogos/restoranai/palangoje/'),
    ('Klaipėda','restoranas',  'https://www.priejuros.lt/lt/pramogos/restoranai/klaipedoje/'),
    ('Neringa', 'restoranas',  'https://www.priejuros.lt/lt/pramogos/restoranai/nidoje/'),
]

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

def extract_email(html):
    if not html:
        return None
    found = EMAIL_RE.findall(html)
    found = [e for e in found if not any(e.endswith(x) for x in ['.png','.jpg','.css','.js'])
             and 'example' not in e and '@2x' not in e]
    return found[0] if found else None

def scrape_listing_page(city, category, url):
    print(f'\n📍 {city} / {category}')
    print(f'   {url}')
    try:
        page = fetcher.get(url)
        if page.status != 200:
            print(f'   ❌ Status {page.status}')
            return []
    except Exception as e:
        print(f'   ❌ Error: {e}')
        return []

    cards = page.css('.apgyvendinimas, .restoranas, .paslaugos')
    if not cards:
        print(f'   ⚠️  No cards found, trying .search_list__link...')
        links = page.css('.search_list__link')
        print(f'   Found {len(links)} links')
        # Fallback: collect name+url from links
        results = []
        for lnk in links:
            href = lnk.attrib.get('href','')
            name = lnk.text.strip() if lnk.text else ''
            if href and name:
                results.append({'name': name, 'city': city, 'category': category,
                                 'detail_url': href, 'source': 'priejuros.lt'})
        print(f'   → {len(results)} entries (name+url only)')
        return results

    results = []
    for card in cards:
        link = card.css('.search_list__link')
        name_el = card.css('.h2')
        href = link[0].attrib.get('href','') if link else ''
        name = name_el[0].text.strip() if name_el else card.find('a', first=True)
        if not name:
            continue
        if hasattr(name, 'text'):
            name = name.text.strip()
        results.append({
            'name': str(name),
            'city': city,
            'category': category,
            'detail_url': href,
            'source': 'priejuros.lt',
        })

    print(f'   → {len(results)} entries')
    return results

def scrape_detail_page(entry):
    """Fetch individual business page for contact details."""
    url = entry.get('detail_url','')
    if not url or not url.startswith('http'):
        return entry
    try:
        time.sleep(DELAY)
        page = fetcher.get(url)
        if page.status != 200:
            return entry

        # Try to extract phone, website, email, address
        phone_el = page.css('.phone, .tel, [href^="tel:"]')
        web_el   = page.css('.website a, [href^="http"]:not([href*="priejuros"])')
        addr_el  = page.css('.address, .adresas, .addr')

        if phone_el:
            ph = phone_el[0].text.strip() if phone_el[0].text else phone_el[0].attrib.get('href','').replace('tel:','')
            entry['phone'] = ph

        if web_el:
            for w in web_el:
                href = w.attrib.get('href','')
                if href and 'priejuros' not in href and href.startswith('http'):
                    entry['website'] = href
                    break

        if addr_el:
            entry['address'] = addr_el[0].text.strip()

        # Email from page
        email = extract_email(page.html_content)
        if email:
            entry['email'] = email

    except Exception:
        pass
    return entry

# ─── Main ─────────────────────────────────────────────────────────────────────
all_results = []

for city, category, url in SOURCES:
    entries = scrape_listing_page(city, category, url)
    all_results.extend(entries)
    time.sleep(DELAY)

print(f'\n\n📋 Total entries collected: {len(all_results)}')
print('🔍 Fetching detail pages for contact info...\n')

for i, entry in enumerate(all_results):
    print(f'[{i+1}/{len(all_results)}] {entry["name"][:45].ljust(45)}', end=' ')
    entry = scrape_detail_page(entry)
    has_email = '✉️' if entry.get('email') else ''
    has_web   = '🌐' if entry.get('website') else ''
    has_phone = '📞' if entry.get('phone') else ''
    print(has_email, has_web, has_phone)

    # Save incrementally
    if (i+1) % 10 == 0:
        OUTPUT.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')

OUTPUT.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')

emails = sum(1 for e in all_results if e.get('email'))
websites = sum(1 for e in all_results if e.get('website'))
print(f'\n✅ Done!')
print(f'   Total:    {len(all_results)}')
print(f'   Emails:   {emails}')
print(f'   Websites: {websites}')
print(f'   Output:   {OUTPUT}')
