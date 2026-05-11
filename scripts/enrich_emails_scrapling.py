#!/usr/bin/env python3
"""
Scrapling enrichment: email + adresas iš įmonių svetainių.
Randa: mailto: nuorodas, adresus (schema.org, contact puslapiai).
Išsaugo į enriched_data.jsonl ir atnaujina per PATCH /api/admin/import/enrich/:id
"""
import re, json, time, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

from scrapling.fetchers import StealthyFetcher

API_URL = "http://localhost:3000"
API_KEY = "ak_77aad7f0459e4f449ded9ba6bb1f820e799e291746be1a2b"
OUT     = 'scripts/enriched_data.jsonl'

LT_STREET_RE = re.compile(
    r'(?:g\.|gatvė|pr\.|prospektas|al\.|alėja|pl\.|plentas)\s*\d*'
    r'|\b(?:g\.|gatvė)\s+\d+'
    r'|\b\w+(?:io|ės|ių|os)\s+(?:g\.|gatvė|pr\.|al\.|pl\.)\s*\d*',
    re.I | re.U
)

def api_get(path):
    req = urllib.request.Request(API_URL + path, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def api_patch(item_id, updates):
    payload = json.dumps(updates, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        f"{API_URL}/api/admin/import/enrich/{item_id}",
        data=payload,
        headers={'Content-Type': 'application/json', 'X-API-Key': API_KEY},
        method='PATCH'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {'error': str(e)}

def extract_domain(url):
    return re.sub(r'https?://(www\.)?', '', url).split('/')[0].lower()

def find_email(page, domain):
    found = [
        e.attrib.get('href','').replace('mailto:','').strip().lower()
        for e in page.css('a[href^="mailto:"]')
        if '@' in e.attrib.get('href','')
    ]
    for e in found:
        if domain in e:
            return e
    return found[0] if found else None

def find_address(page, html):
    # 1. schema.org streetAddress
    schema = re.findall(r'"streetAddress"\s*:\s*"([^"]{5,80})"', html)
    if schema:
        return schema[0].strip()

    # 2. itemprop="streetAddress"
    itemprop = re.findall(r'itemprop="streetAddress"[^>]*>([^<]{5,80})<', html)
    if itemprop:
        return itemprop[0].strip()

    # 3. Lietuviška gatvė tekste
    text = page.text or ''
    matches = LT_STREET_RE.findall(text)
    if matches:
        # Raskime kontekstą aplink pirmą atitikmenį
        idx = text.find(matches[0])
        snippet = text[max(0, idx-30):idx+60].strip()
        if len(snippet) > 5:
            return re.sub(r'\s+', ' ', snippet)

    return None

def get_records(limit=300):
    """Visi su website (nepriklausomai ar turi email/adresą)."""
    records, offset = [], 0
    while len(records) < limit:
        try:
            data = api_get(f'/v1/services?limit=100&offset={offset}')
        except Exception as e:
            print(f'  API klaida: {e}', flush=True)
            break
        items = data.get('data', [])
        if not items:
            break
        for item in items:
            if item.get('website') and (not item.get('email') or not item.get('address') or item.get('address') == item.get('city')):
                records.append(item)
        offset += len(items)
        if len(items) < 100:
            break
    return records[:limit]

def main():
    print("🔍 Scrapling enrichment: email + adresas\n", flush=True)
    records = get_records(limit=300)
    print(f"Rasta {len(records)} įrašų praturtinimui\n", flush=True)

    emails_found = addr_found = skipped = errors = 0

    for i, item in enumerate(records, 1):
        name    = item.get('title', '')
        website = item.get('website', '')
        item_id = item.get('id')
        has_email = bool(item.get('email'))
        has_addr  = item.get('address') and item.get('address') != item.get('city')

        print(f"[{i:3}/{len(records)}] {name[:38]:38} ", end='', flush=True)

        try:
            page = StealthyFetcher.fetch(website, headless=True, network_idle=False, timeout=20000)
            if page.status != 200:
                print(f"→ {page.status} SKIP", flush=True)
                skipped += 1
                continue

            html  = str(page.html_content or '')
            domain = extract_domain(website)
            updates = {}

            if not has_email:
                email = find_email(page, domain)
                if email:
                    updates['email'] = email
                    emails_found += 1

            if not has_addr:
                addr = find_address(page, html)
                if addr:
                    updates['location'] = addr
                    addr_found += 1

            if updates:
                api_patch(item_id, updates)
                with open(OUT, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'id': item_id, 'name': name, 'website': website, **updates}, ensure_ascii=False) + '\n')
                parts = []
                if 'email' in updates:   parts.append(f"✉ {updates['email'][:30]}")
                if 'location' in updates: parts.append(f"📍 {updates['location'][:30]}")
                print(f"→ {' | '.join(parts)}", flush=True)
            else:
                print("→ nieko nerasta", flush=True)
                skipped += 1

        except Exception as e:
            print(f"→ ERR: {str(e)[:60]}", flush=True)
            errors += 1

        time.sleep(1.2)

    print(f"\n✅ Emailai: {emails_found} | Adresai: {addr_found} | Praleista: {skipped} | Klaidos: {errors}", flush=True)
    print(f"Duomenys: {OUT}", flush=True)

if __name__ == '__main__':
    main()
