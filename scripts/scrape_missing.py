# -*- coding: utf-8 -*-
"""Retry tik trukstami miestai - su ilgesniu sleep"""
import sys, json, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

MISSING = {
    'Kretinga':            (55.8897, 21.2442, 3000),
    'Salantai':            (56.0600, 21.5700, 2000),
    'Kūlupėnai':          (55.9400, 21.3800, 1500),
    'Jokūbavas':           (55.8500, 21.3200, 1500),
    'Klaipėda':            (55.7103, 21.1443, 6000),
    'Gargždai':            (55.7100, 21.3900, 3000),
    'Priekulė':            (55.5500, 21.3200, 2000),
    'Nida':                (55.3086, 21.0123, 3000),
    'Šilutė':              (55.3500, 21.4800, 3000),
    'Žemaičių Naumiestis': (55.3700, 21.5800, 2000),
    'Kintai':              (55.3800, 21.2600, 2000),
}

TYPE_LT = {'restaurant':'Restoranas','cafe':'Kavinė','bar':'Baras',
           'fast_food':'Greitas maistas','pub':'Pub','food_court':'Maisto kiemas',
           'ice_cream':'Ledai','bakery':'Kepykla','deli':'Deli'}

OVERPASS = "https://overpass-api.de/api/interpreter"

def fetch(lat, lng, radius):
    q = f"""[out:json][timeout:20];(
  node["amenity"~"restaurant|cafe|bar|fast_food|pub|food_court|ice_cream"](around:{radius},{lat},{lng});
  node["shop"~"bakery|deli"](around:{radius},{lat},{lng});
);out body;"""
    data = urllib.parse.urlencode({'data': q}).encode()
    req = urllib.request.Request(OVERPASS, data=data,
          headers={'User-Agent': 'PajurioPortalas/1.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())

# Krauti esamus rezultatus
with open(r'd:\_PAL\benino\scripts\cafes_all_cities.json', encoding='utf-8') as f:
    all_results = json.load(f)

for city, (lat, lng, radius) in MISSING.items():
    print(f"  {city}...", end=' ', flush=True)
    for attempt in range(3):
        try:
            data = fetch(lat, lng, radius)
            places, seen = [], set()
            for el in data.get('elements', []):
                t = el.get('tags', {})
                name = t.get('name')
                if not name or name in seen: continue
                seen.add(name)
                amenity = t.get('amenity') or t.get('shop', '')
                places.append({
                    'name': name,
                    'type': TYPE_LT.get(amenity, amenity),
                    'opening_hours': t.get('opening_hours') or None,
                    'phone': t.get('phone') or t.get('contact:phone') or None,
                    'website': t.get('website') or t.get('contact:website') or None,
                    'maps': f"https://www.google.com/maps?q={el.get('lat',lat)},{el.get('lon',lng)}",
                })
            places.sort(key=lambda x: x['name'])
            all_results[city] = places
            print(f"{len(places)} vnt.")
            break
        except Exception as e:
            print(f"[{attempt+1}] {e} ", end='')
            time.sleep(8)
    time.sleep(5)

# Issaugoti
with open(r'd:\_PAL\benino\scripts\cafes_all_cities.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

total = sum(len(v) for v in all_results.values())
print(f"\n=== VISO: {total} vietu ===\n")
for city, places in all_results.items():
    if places:
        print(f"  {city} ({len(places)}):")
        for p in places:
            oh = f" | {p['opening_hours']}" if p['opening_hours'] else ''
            w = f" | {p['website']}" if p['website'] else ''
            print(f"    {p['name']} [{p['type']}]{oh}{w}")
            print(f"      {p['maps']}")
