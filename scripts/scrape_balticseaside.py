"""
scrape_balticseaside.py
Scrapes balticseaside.lt listing pages to extract email and real website
for businesses that have balticseaside.lt as their only URL.
Updates kavines.json, hotels.json, paslaugos.json in place.
"""
import sys, io, json, re, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from scrapling import Fetcher

DATA_DIR = 'd:/_PAL/benino/agent-network/public/data'
FILES = ['kavines.json', 'hotels.json', 'paslaugos.json']

SKIP_DOMAINS = [
    'balticseaside.', 'priejuros.lt', 'google.', 'facebook.com',
    'booking.com', 'airbnb.', 'tripadvisor.', 'urlaublitauen.de',
    'wakacjelitwa.pl', 'pukarags.', 'expedia.', 'hotels.com',
    'youtube.com', 'instagram.com', 'twitter.com', 'tiktok.com',
    'holidaylettings.', 'homeaway.', 'vrbo.', 'holidaycheck.',
]
FAKE_EMAILS = {'info@example.com', 'noreply@', 'support@', 'webmaster@'}

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

def is_real_site(url):
    """Only accept Lithuanian (.lt) business websites."""
    if not url.startswith('http'): return False
    if any(d in url for d in SKIP_DOMAINS): return False
    # Prefer .lt domains, but accept others if clearly a business site
    return '.lt' in url or (not any(url.endswith(x) for x in ['.lv','.de','.pl','.ee','.ru']))

def clean_email(email):
    e = email.lower().strip()
    if any(f in e for f in FAKE_EMAILS): return None
    if any(e.endswith(x) for x in ['.png','.jpg','.gif','.svg','.css','.js']): return None
    if any(x in e for x in ['sentry.io','wix.com','cloudflare','google.com','gtm.']): return None
    return e

def scrape_bslt(fetcher, url):
    """Returns (email, website) from a balticseaside.lt listing page."""
    try:
        r = fetcher.get(url, timeout=20)
        if r.status != 200:
            return None, None

        html = r.html_content

        # 1. Email — mailto: links only (most reliable, avoids false positives)
        mailtos = re.findall(r'mailto:([^\"\s&<>]+)', html)
        email = None
        for m in mailtos:
            c = clean_email(m)
            if c:
                email = c
                break

        # 2. Website — look inside main content only, not nav/header/footer
        # The listing content is in <div class="description"> or <div id="main">
        # Strategy: find all external .lt links in <article> or <main> or .listing
        website = None
        content_selectors = [
            'article a[href]', '.listing-description a[href]',
            '.description a[href]', '#content a[href]', 'main a[href]',
            '.col-md-8 a[href]', '.col-lg-8 a[href]',
        ]
        for sel in content_selectors:
            for link in r.css(sel):
                href = link.attrib.get('href', '')
                if is_real_site(href):
                    website = href
                    break
            if website:
                break

        # Fallback: scan all links but skip known footer/nav/aggregator domains
        if not website:
            FOOTER_PATTERNS = ['vilaartemide', 'pukarags', 'urlaublitauen', 'wakacjelitwa',
                               'holidaylettings', 'homeaway', 'novasol', 'interhome']
            for link in r.css('a[href]'):
                href = link.attrib.get('href', '')
                if is_real_site(href) and not any(p in href for p in FOOTER_PATTERNS):
                    website = href
                    break

        return email, website

    except Exception as e:
        return None, None

# ── Main ──────────────────────────────────────────────────────────────────────

fetcher = Fetcher()
total_emails = 0
total_sites  = 0
total_checked = 0

for filename in FILES:
    path = os.path.join(DATA_DIR, filename)
    data = json.load(open(path, encoding='utf-8'))
    changed = False

    candidates = []
    for city, lst in data.items():
        if not isinstance(lst, list): continue
        for i, biz in enumerate(lst):
            if not isinstance(biz, dict): continue
            web = str(biz.get('website') or '')
            if 'balticseaside.lt' in web:
                candidates.append((city, i, biz))

    print(f'\n{filename}: {len(candidates)} balticseaside įrašų')

    for idx, (city, i, biz) in enumerate(candidates):
        name = biz.get('name', '')[:42]
        url  = biz['website']
        has_email = biz.get('email') and not biz.get('email_generated')
        total_checked += 1

        print(f'  [{idx+1:3}/{len(candidates)}] {name:42}', end=' ', flush=True)

        email, website = scrape_bslt(fetcher, url)

        markers = []
        if email and not has_email:
            data[city][i]['email'] = email
            data[city][i].pop('email_generated', None)
            total_emails += 1
            markers.append(f'✉  {email}')
            changed = True
        if website:
            data[city][i]['website'] = website
            total_sites += 1
            markers.append(f'🌐 {website[:45]}')
            changed = True

        print(' | '.join(markers) if markers else '—')
        time.sleep(4)

    if changed:
        json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f'  Saved {filename}')

print(f'\n✅ Patikrinta: {total_checked} | Emailų: {total_emails} | Svetainių: {total_sites}')
