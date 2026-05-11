# -*- coding: utf-8 -*-
"""
Scrape visa prekyba (parduotuvės, supermarketai, suvenyrai, vaistinės ir kt.)
per 18 pajūrio miestų. Šaltinis: OpenStreetMap Overpass API.
Rezultatas: scripts/prekyba_raw.json  +  public/data/prekyba.json
"""
import sys, json, time, urllib.request, urllib.parse, re
sys.stdout.reconfigure(encoding='utf-8')

CITIES = {
    'Palanga':               (55.9175, 21.0708, 4000),
    'Šventoji':              (56.0308, 21.0717, 2500),
    'Kretinga':              (55.8897, 21.2442, 3000),
    'Vydmantai':             (55.9200, 21.1900, 2000),
    'Darbėnai':              (56.0200, 21.2700, 2000),
    'Salantai':              (56.0600, 21.5700, 2000),
    'Kūlupėnai':             (55.9400, 21.3800, 1500),
    'Jokūbavas':             (55.8500, 21.3200, 1500),
    'Klaipėda':              (55.7103, 21.1443, 6000),
    'Gargždai':              (55.7100, 21.3900, 3000),
    'Priekulė':              (55.5500, 21.3200, 2000),
    'Dovilai':               (55.7500, 21.2400, 1500),
    'Nida':                  (55.3086, 21.0123, 3000),
    'Šilutė':                (55.3500, 21.4800, 3000),
    'Švėkšna':               (55.4500, 21.5700, 2000),
    'Rusnė':                 (55.2900, 21.3700, 2000),
    'Žemaičių Naumiestis':   (55.3700, 21.5800, 2000),
    'Kintai':                (55.3800, 21.2600, 2000),
}

OVERPASS = "https://overpass-api.de/api/interpreter"

# OSM tag → Lithuanian type name
TYPE_MAP = {
    # shop= tags
    'supermarket':    'Supermarketas',
    'convenience':    'Parduotuvė',
    'general':        'Parduotuvė',
    'department_store': 'Parduotuvė',
    'gift':           'Suvenyrų parduotuvė',
    'souvenir':       'Suvenyrų parduotuvė',
    'clothes':        'Drabužiai',
    'fashion':        'Drabužiai',
    'boutique':       'Drabužiai',
    'shoes':          'Drabužiai',
    'seafood':        'Žuvies parduotuvė',
    'fish':           'Žuvies parduotuvė',
    'fishing':        'Žvejybos reikmenys',
    'outdoor':        'Žvejybos reikmenys',
    'sports':         'Paplūdimio prekės',
    'beach':          'Paplūdimio prekės',
    'swimwear':       'Paplūdimio prekės',
    'pharmacy':       'Vaistinė',
    'alcohol':        'Alkoholis',
    'wine':           'Alkoholis',
    'beverages':      'Alkoholis',
    'florist':        'Gėlių parduotuvė',
    'flowers':        'Gėlių parduotuvė',
    'toys':           'Žaislai ir pramogos',
    'games':          'Žaislai ir pramogos',
    'electronics':    'Elektronika',
    'mobile_phone':   'Elektronika',
    'hardware':       'Statybos prekės',
    'doityourself':   'Statybos prekės',
    'garden':         'Sodas ir namas',
    'furniture':      'Sodas ir namas',
    'greengrocer':    'Daržovės ir vaisiai',
    'butcher':        'Mėsinė',
    'deli':           'Delikatesas',
    'bakery':         'Kepykla / parduotuvė',
    'confectionery':  'Kepykla / parduotuvė',
    'kiosk':          'Kioskas',
    'newsagent':      'Kioskas',
    # amenity= tags
    'marketplace':    'Turgus / Mugė',
    'pharmacy':       'Vaistinė',
}

# Tipai, kuriuos RODOME (filtruojame triukšmą)
ALLOWED_TYPES = {
    'Supermarketas', 'Parduotuvė', 'Suvenyrų parduotuvė', 'Drabužiai',
    'Žuvies parduotuvė', 'Turgus / Mugė', 'Žvejybos reikmenys', 'Vaistinė',
    'Paplūdimio prekės', 'Alkoholis', 'Gėlių parduotuvė',
    'Žaislai ir pramogos', 'Elektronika', 'Statybos prekės',
    'Daržovės ir vaisiai', 'Mėsinė', 'Delikatesas', 'Kepykla / parduotuvė',
    'Kioskas', 'Sodas ir namas',
}

def slugify(name, city):
    s = name.lower()
    s = re.sub(r'[ąą]', 'a', s); s = re.sub(r'[čč]', 'c', s)
    s = re.sub(r'[ęę]', 'e', s); s = re.sub(r'[ėė]', 'e', s)
    s = re.sub(r'[įį]', 'i', s); s = re.sub(r'[šš]', 's', s)
    s = re.sub(r'[ųų]', 'u', s); s = re.sub(r'[ūū]', 'u', s)
    s = re.sub(r'[žž]', 'z', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    city_slug = re.sub(r'[^a-z0-9]+', '-', city.lower()).strip('-')
    return f"{s}-{city_slug}"

def fetch_places(city, lat, lng, radius):
    query = f"""[out:json][timeout:30];
(
  node["shop"](around:{radius},{lat},{lng});
  node["amenity"="marketplace"](around:{radius},{lat},{lng});
  node["amenity"="pharmacy"](around:{radius},{lat},{lng});
);
out body;"""
    data = urllib.parse.urlencode({'data': query}).encode()
    for attempt in range(3):
        try:
            req = urllib.request.Request(OVERPASS, data=data,
                  headers={'User-Agent': 'PajurioPortalas/1.0'})
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt < 2:
                wait = 10 * (attempt + 1)
                print(f"retry {attempt+1} po {wait}s ({e})...", end=' ', flush=True)
                time.sleep(wait)
            else:
                raise

all_results = {}
total = 0

print("=" * 55)
print("  PAJŪRIO PREKYBA — OSM scraperis")
print("=" * 55)

for city, (lat, lng, radius) in CITIES.items():
    print(f"  {city}...", end=' ', flush=True)
    try:
        data = fetch_places(city, lat, lng, radius)
        places = []
        seen = set()
        for el in data.get('elements', []):
            t = el.get('tags', {})
            name = t.get('name')
            if not name or name in seen:
                continue

            shop_tag    = t.get('shop', '')
            amenity_tag = t.get('amenity', '')
            raw_type    = shop_tag or amenity_tag

            lt_type = TYPE_MAP.get(raw_type)
            if not lt_type or lt_type not in ALLOWED_TYPES:
                continue

            seen.add(name)
            el_lat = el.get('lat', lat)
            el_lon = el.get('lon', lng)
            nick = slugify(name, city)

            addr_parts = [
                t.get('addr:street'),
                t.get('addr:housenumber'),
                t.get('addr:city') or city,
            ]
            address = ' '.join(p for p in addr_parts if p) or None

            places.append({
                'name':          name,
                'type':          lt_type,
                'city':          city,
                'address':       address,
                'phone':         t.get('phone') or t.get('contact:phone') or None,
                'website':       t.get('website') or t.get('contact:website') or None,
                'maps':          f"https://www.google.com/maps?q={el_lat},{el_lon}",
                'opening_hours': t.get('opening_hours') or None,
                'lat':           el_lat,
                'lng':           el_lon,
                'rating':        None,
                'reviews_count': None,
                'nickname':      nick,
                'has_account':   False,
                'photo_url':     None,
                'description':   None,
                'tags':          [],
                'email':         t.get('email') or t.get('contact:email') or None,
            })

        places.sort(key=lambda x: (x['type'], x['name']))
        all_results[city] = places
        total += len(places)
        print(f"{len(places)} vnt.")
        time.sleep(4)  # Overpass rate limit
    except Exception as e:
        print(f"KLAIDA: {e}")
        all_results[city] = []

# --- Išsaugoti raw JSON ---
raw_path = r"d:\_PAL\benino\scripts\prekyba_raw.json"
with open(raw_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

# --- Išsaugoti į public/data/prekyba.json ---
out_path = r"d:\_PAL\benino\agent-network\public\data\prekyba.json"
# Filtruojame tik miestus su duomenimis
public_data = {city: places for city, places in all_results.items() if places}
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(public_data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*55}")
print(f"  VISO: {total} prekybos vietu per {len(CITIES)} miestu")
print(f"  Raw:    {raw_path}")
print(f"  Public: {out_path}")
print(f"{'='*55}\n")

# Suvestinė pagal tipą
type_counts = {}
for places in all_results.values():
    for p in places:
        type_counts[p['type']] = type_counts.get(p['type'], 0) + 1
print("  Pagal tipą:")
for tp, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"    {tp:30s} {cnt:4d}")
