#!/usr/bin/env python3
"""
Scrape nakvynės objektus iš OSM Overpass: viešbučiai, hosteliai,
apartamentai, svečių namai, poilsio namai, kempingai su kotedžais.
Importuoja tiesiai į Supabase rental_properties_real lentelę.
"""
import sys, json, time, urllib.request, urllib.parse, os, re
sys.stdout.reconfigure(encoding='utf-8')

CITIES = {
    'Palanga':  (55.9175, 21.0708, 5000),
    'Šventoji': (56.0308, 21.0717, 3000),
    'Kretinga': (55.8897, 21.2442, 4000),
    'Klaipėda': (55.7103, 21.1443, 7000),
    'Nida':     (55.3086, 21.0123, 3000),
    'Neringa':  (55.4500, 21.0500, 8000),
    'Šilutė':   (55.3500, 21.4800, 4000),
}

OVERPASS = "https://overpass-api.de/api/interpreter"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; PajurioBot/1.0)',
    'Accept': '*/*',
}

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_URL:
    try:
        for line in open("d:/_PAL/benino/agent-network/.env", encoding='utf-8'):
            line = line.strip()
            if line.startswith("SUPABASE_URL="):
                SUPABASE_URL = line.split("=", 1)[1].strip().strip('"').strip("'")
            if line.startswith("SUPABASE_SERVICE_ROLE_KEY=") or (not SUPABASE_KEY and line.startswith("SUPABASE_KEY=")):
                SUPABASE_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
    except: pass

TYPE_MAP = {
    'hotel':       'Viešbutis',
    'hostel':      'Hostelis',
    'guest_house': 'Svečių namai',
    'motel':       'Motelis',
    'apartment':   'Apartamentai',
    'chalet':      'Kotedžas',
    'villa':       'Vila',
    'camp_site':   'Kempingas',
    'caravan_site':'Kemperio aikštelė',
    'holiday_village': 'Poilsio kaimelis',
}

def overpass_query(lat, lng, radius):
    return f"""
[out:json][timeout:30];
(
  node["tourism"~"hotel|hostel|guest_house|motel|apartment|chalet|villa|camp_site|caravan_site|holiday_village"](around:{radius},{lat},{lng});
  way["tourism"~"hotel|hostel|guest_house|motel|apartment|chalet|villa"](around:{radius},{lat},{lng});
);
out center tags;
"""

def fetch(query):
    data = urllib.parse.urlencode({'data': query}).encode()
    req = urllib.request.Request(OVERPASS, data=data)
    req.add_header('User-Agent', 'curl/7.88.1')
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read())

API_URL  = "http://localhost:3000"
API_KEY  = "ak_77aad7f0459e4f449ded9ba6bb1f820e799e291746be1a2b"

def import_via_api(records):
    """Import per admin-import endpoint — jis žino teisingą schema."""
    ok = err = 0
    for rec in records:
        payload = json.dumps(rec, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            f"{API_URL}/api/admin/import/maxun",
            data=payload,
            headers={'Content-Type':'application/json','X-API-Key':API_KEY}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                ok += 1
        except Exception:
            err += 1
    return ok, err

def parse_address(tags):
    parts = []
    if tags.get('addr:street'): parts.append(tags['addr:street'])
    if tags.get('addr:housenumber'): parts.append(tags['addr:housenumber'])
    return ', '.join(parts) if parts else None

def slugify(text):
    lt = {'ą':'a','č':'c','ę':'e','ė':'e','į':'i','š':'s','ų':'u','ū':'u','ž':'z'}
    t = text.lower()
    for k,v in lt.items(): t=t.replace(k,v)
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')[:60]

def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Trūksta SUPABASE kredencialų"); return

    print("🏨 Viešbučių scraping iš OSM\n")
    all_imported = 0

    for city, (lat, lng, radius) in CITIES.items():
        print(f"── {city}", flush=True)
        try:
            raw = fetch(overpass_query(lat, lng, radius))
        except Exception as e:
            print(f"  ERR: {e}"); time.sleep(5); continue

        records = []
        seen = set()
        for el in raw.get('elements', []):
            tags = el.get('tags', {})
            name = tags.get('name') or tags.get('name:lt')
            if not name: continue
            key = name.lower().strip()
            if key in seen: continue
            seen.add(key)

            tourism_type = tags.get('tourism', '')
            type_label = TYPE_MAP.get(tourism_type, 'Nakvynė')

            if el['type'] == 'way':
                c = el.get('center', {})
                elat, elng = c.get('lat'), c.get('lon')
            else:
                elat, elng = el.get('lat'), el.get('lon')

            addr = parse_address(tags)
            website = tags.get('website') or tags.get('contact:website')
            phone = tags.get('phone') or tags.get('contact:phone')
            stars = tags.get('stars')
            desc_parts = [type_label]
            if stars: desc_parts.append(f"{stars}★")
            description = ' · '.join(desc_parts)

            records.append({
                'title':       name,
                'description': description,
                'city':        city,
                'address':     addr or city,
                'phone':       phone,
                'website':     website,
                'type':        type_label,
            })

        if records:
            ok, err = import_via_api(records)
            print(f"  {ok}/{len(records)} importuota (klaidos: {err})", flush=True)
            all_imported += ok
        else:
            print(f"  0 objektų rasta", flush=True)

        time.sleep(2)

    print(f"\n✅ Viso importuota: {all_imported} nakvynės objektų")

if __name__ == '__main__':
    main()
