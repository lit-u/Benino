"""
scrape_missing_emails.py
Scrapes contact pages of businesses that have a website but no email.
Updates kavines.json, hotels.json, paslaugos.json in place.
"""
import sys, io, json, re, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from scrapling import Fetcher

DATA_DIR = 'd:/_PAL/benino/agent-network/public/data'
FILES = ['kavines.json', 'hotels.json', 'paslaugos.json']

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
FAKE_EMAILS = {
    'tic@kretingosturizmas.info', 'info@example.com',
    'example@example.com', 'test@test.com', 'noreply@',
}
CONTACT_PATHS = ['/kontaktai', '/kontaktai/', '/contact', '/contact/', '/apie', '/apie-mus', '/contacts']

def clean_email(email):
    email = email.lower().strip()
    if any(f in email for f in FAKE_EMAILS):
        return None
    # Skip image filenames, CSS, JS files accidentally matched
    if any(email.endswith(x) for x in ['.png', '.jpg', '.gif', '.svg', '.css', '.js']):
        return None
    # Skip sentry/tracking emails
    if any(x in email for x in ['sentry.io', 'wix.com', 'wordpress.com', 'cloudflare', 'google.com']):
        return None
    return email

def find_emails_in_page(page):
    text = page.get_all_text() if hasattr(page, 'get_all_text') else ''
    html = page.html_content if hasattr(page, 'html_content') else ''
    # mailto: links first (most reliable)
    mailtos = re.findall(r'mailto:([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})', html)
    # then generic regex on text
    found = EMAIL_RE.findall(text)
    all_found = mailtos + found
    cleaned = []
    seen = set()
    for e in all_found:
        c = clean_email(e)
        if c and c not in seen:
            seen.add(c)
            cleaned.append(c)
    return cleaned

def try_scrape_email(fetcher, website):
    base = website.rstrip('/')
    emails = []

    # 1. Try root URL
    try:
        r = fetcher.get(base, timeout=8)
        if r.status == 200:
            emails = find_emails_in_page(r)
            if emails:
                return emails[0]
    except Exception:
        pass

    # 2. Try contact paths
    for path in CONTACT_PATHS:
        try:
            r = fetcher.get(base + path, timeout=8)
            if r.status == 200:
                emails = find_emails_in_page(r)
                if emails:
                    return emails[0]
        except Exception:
            continue

    return None

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Main ──────────────────────────────────────────────────────────────────────

fetcher = Fetcher()
total_found = 0
total_checked = 0

for filename in FILES:
    path = os.path.join(DATA_DIR, filename)
    data = load_json(path)
    changed = False

    candidates = []
    for city, lst in data.items():
        if not isinstance(lst, list):
            continue
        for i, biz in enumerate(lst):
            if not isinstance(biz, dict):
                continue
            has_email = biz.get('email') and str(biz['email']).strip() not in ('', 'None')
            has_web = biz.get('website') and str(biz['website']).strip() not in ('', 'None')
            is_fb = 'facebook.com' in str(biz.get('website', ''))
            if not has_email and has_web and not is_fb:
                candidates.append((city, i, biz))

    print(f'\n{filename}: {len(candidates)} verslų be email')

    for idx, (city, i, biz) in enumerate(candidates):
        name = biz.get('name', '')[:45]
        web = biz['website']
        total_checked += 1
        print(f'  [{idx+1}/{len(candidates)}] {name[:40]:40}', end=' ', flush=True)

        email = try_scrape_email(fetcher, web)

        if email:
            data[city][i]['email'] = email
            changed = True
            total_found += 1
            print(f'✉  {email}')
        else:
            print('—')

        time.sleep(1.5)

    if changed:
        save_json(path, data)
        print(f'  Saved {filename}')

print(f'\n✅ Iš viso patikrinta: {total_checked} | Rasta emailų: {total_found}')
