#!/usr/bin/env python3
"""
Scrapling test: rekvizitai.lt - 1 miestas (Palanga), kategorija 'restoranai'
Lygina su tuo ką gavo paprastas scraper
"""
import json
from scrapling.fetchers import StealthyFetcher, DynamicFetcher

TEST_URL = "https://rekvizitai.vz.lt/imones/restoranai/palanga/"

def try_static():
    """Pirmiausia bandome StealthyFetcher (greičiau, be JS)"""
    print("── StealthyFetcher (static stealth) ────────")
    page = StealthyFetcher.fetch(TEST_URL, headless=True, network_idle=True)
    print(f"  Status: {page.status}")

    items = page.css('.company-list-item, .list-item, article.item, .result-item')
    print(f"  Rasta elementų: {len(items)}")

    if not items:
        # Bandome rasti įrašus pagal struktūrą
        links = page.css('a[href*="/imone/"]')
        print(f"  Nuorodos į įmones: {len(links)}")
        for l in links[:5]:
            print(f"    {l.text.strip()[:60]} → {l.attrib.get('href','')}")

    return page

def try_dynamic():
    """DynamicFetcher - su JS rendering"""
    print("\n── DynamicFetcher (JS rendering) ────────────")
    page = DynamicFetcher.fetch(TEST_URL, headless=True, network_idle=True)
    print(f"  Status: {page.status}")

    # Rekvizitai.lt struktūra
    companies = page.css('div.company, .companies-list > li, .company-card, h2.company-name')
    print(f"  Įmonių elementų: {len(companies)}")

    # Bandome rasti vardus
    names = page.css('h2, h3, .name, [class*="company-name"], [class*="title"]')
    print(f"  Vardų elementų: {len(names)}")
    for n in names[:8]:
        t = n.text.strip()
        if t and len(t) > 3:
            print(f"    {t[:70]}")

    # Emails
    emails = page.css('a[href^="mailto:"]')
    print(f"\n  Email nuorodos: {len(emails)}")
    for e in emails[:5]:
        print(f"    {e.attrib.get('href','')}")

    # Telefonai
    phones = page.css('a[href^="tel:"]')
    print(f"  Tel nuorodos: {len(phones)}")
    for p in phones[:5]:
        print(f"    {p.text.strip()}")

    # Nuotraukos
    imgs = page.css('img[src*="logo"], img[src*="photo"], img[src*="company"]')
    print(f"  Logotipų/nuotraukų: {len(imgs)}")

    return page

def scrape_company_page(url):
    """Bandome atidaryti vieną įmonės puslapį"""
    print(f"\n── Įmonės puslapis: {url} ────")
    page = StealthyFetcher.fetch(url, headless=True, network_idle=True)
    print(f"  Status: {page.status}")

    # Ieškome kontaktų
    email = page.css('a[href^="mailto:"]')
    phone = page.css('a[href^="tel:"]')
    img = page.css('img.company-logo, .company-photo img, img[alt*="logo"]')
    desc = page.css('.company-description, .about-company, p.description')

    print(f"  Email: {[e.attrib.get('href','').replace('mailto:','') for e in email[:3]]}")
    print(f"  Tel: {[p.text.strip() for p in phone[:3]]}")
    print(f"  Img: {[i.attrib.get('src','')[:80] for i in img[:2]]}")
    print(f"  Desc: {desc[0].text.strip()[:150] if desc else 'nėra'}")

if __name__ == '__main__':
    print("🔍 Scrapling test: rekvizitai.vz.lt\n")

    try:
        page = try_static()

        # Pabandome vieno įmonės puslapį jei radome nuorodas
        links = page.css('a[href*="/imone/"]')
        if links:
            sample_url = "https://rekvizitai.vz.lt" + links[0].attrib.get('href','') if links[0].attrib.get('href','').startswith('/') else links[0].attrib.get('href','')
            scrape_company_page(sample_url)
    except Exception as e:
        print(f"  StealthyFetcher klaida: {e}")
        print("  Bandome DynamicFetcher...")
        try:
            try_dynamic()
        except Exception as e2:
            print(f"  DynamicFetcher klaida: {e2}")
