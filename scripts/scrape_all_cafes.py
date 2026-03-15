# -*- coding: utf-8 -*-
"""
Scrape visi restoranai/kavinės per 18 pajūrio miestų
Šaltinis: OpenStreetMap Overpass API
"""
import sys, json, time, urllib.request, urllib.parse
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
TYPE_LT = {
    'restaurant': 'Restoranas',
    'cafe':       'Kavinė',
    'bar':        'Baras',
    'fast_food':  'Greitas maistas',
    'pub':        'Pub',
    'food_court': 'Maisto kiemas',
    'ice_cream':  'Ledai',
    'bakery':     'Kepykla',
}

def fetch_places(city, lat, lng, radius):
    query = f"""[out:json][timeout:15];
(
  node["amenity"~"restaurant|cafe|bar|fast_food|pub|food_court|ice_cream"](around:{radius},{lat},{lng});
  node["shop"~"bakery|deli"](around:{radius},{lat},{lng});
);
out body;"""
    data = urllib.parse.urlencode({'data': query}).encode()
    req = urllib.request.Request(OVERPASS, data=data,
          headers={'User-Agent': 'PajurioPortalas/1.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())

all_results = {}
total = 0

for city, (lat, lng, radius) in CITIES.items():
    print(f"  Kraunama: {city}...", end=' ', flush=True)
    try:
        data = fetch_places(city, lat, lng, radius)
        places = []
        seen = set()
        for el in data.get('elements', []):
            t = el.get('tags', {})
            name = t.get('name')
            if not name or name in seen:
                continue
            seen.add(name)
            amenity = t.get('amenity') or t.get('shop', '')
            places.append({
                'name': name,
                'type': TYPE_LT.get(amenity, amenity),
                'opening_hours': t.get('opening_hours') or t.get('opening_hours:covid19') or None,
                'phone': t.get('phone') or t.get('contact:phone') or None,
                'website': t.get('website') or t.get('contact:website') or None,
                'maps': f"https://www.google.com/maps?q={el.get('lat',lat)},{el.get('lon',lng)}",
            })
        places.sort(key=lambda x: x['name'])
        all_results[city] = places
        total += len(places)
        print(f"{len(places)} vnt.")
        time.sleep(1)  # Overpass rate limit
    except Exception as e:
        print(f"KLAIDA: {e}")
        all_results[city] = []

# Išsaugoti JSON
out_path = r"d:\_PAL\benino\scripts\cafes_all_cities.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"ISVISO: {total} maitinimo vietu per {len(CITIES)} miestu")
print(f"Isaugota: {out_path}")
print(f"{'='*50}\n")

# Suvestine
for city, places in all_results.items():
    if not places:
        print(f"  {city}: (nieko nerasta)")
        continue
    print(f"\n  {city} ({len(places)}):")
    for p in places:
        oh = f" | {p['opening_hours']}" if p['opening_hours'] else ''
        print(f"    - [{p['type']}] {p['name']}{oh}")
