"""
geocode_businesses.py
Geocodes kavines.json and paslaugos.json entries using Nominatim (OpenStreetMap).
Adds lat/lng fields. Respects 1 req/s rate limit.
"""
import json, time, sys, io, os, urllib.request, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_DIR = 'd:/_PAL/benino/agent-network/public/data'
FILES = ['hotels.json', 'kavines.json', 'paslaugos.json']
PHOTON_URL = 'https://photon.komoot.io/api/'
HEADERS = {'User-Agent': 'PajurioPortalas/1.0 (sekmes.lt)'}

# Palanga coast bounding box — reject coords outside this region
LAT_MIN, LAT_MAX = 55.5, 56.6
LNG_MIN, LNG_MAX = 20.5, 21.8

def geocode(address, city):
    """Returns (lat, lng) or (None, None)"""
    query = address if 'Lietuva' in address else f"{address}, Lietuva"
    # Build URL manually to avoid encoding issues with Lithuanian chars
    encoded = urllib.parse.quote(query, safe='')
    url = f"{PHOTON_URL}?q={encoded}&limit=1"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            features = data.get('features', [])
            if features:
                coords = features[0]['geometry']['coordinates']
                return float(coords[1]), float(coords[0])  # lat, lng
    except Exception as e:
        print(f"  ⚠️  {e}")
    return None, None

total_geocoded = 0

for filename in FILES:
    path = os.path.join(DATA_DIR, filename)
    data = json.load(open(path, encoding='utf-8'))
    changed = False
    geocoded = 0
    skipped = 0

    candidates = []
    for city, lst in data.items():
        if not isinstance(lst, list): continue
        for i, biz in enumerate(lst):
            if not isinstance(biz, dict): continue
            if biz.get('lat'): continue  # already has coords
            # Use address if available, else fallback to name + city
            query = biz.get('address') or f"{biz.get('name', '')}, {biz.get('city', city)}"
            if not query.strip(): continue
            candidates.append((city, i, biz, query))

    print(f'\n{filename}: {len(candidates)} be koordinačių')

    for idx, (city, i, biz, query) in enumerate(candidates):
        name = biz.get('name', '')[:40]
        src = 'adr' if biz.get('address') else 'vardas'
        print(f'  [{idx+1:3}/{len(candidates)}] {name:40} [{src}]', end=' ', flush=True)

        lat, lng = geocode(query, biz.get('city', city))
        if lat and LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX:
            data[city][i]['lat'] = lat
            data[city][i]['lng'] = lng
            geocoded += 1
            total_geocoded += 1
            changed = True
            # Save immediately after each success
            json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            print(f'✅ {lat:.5f},{lng:.5f}')
        elif lat:
            print(f'⛔ {lat:.5f},{lng:.5f} (ne regione)')
            skipped += 1
        else:
            skipped += 1
            print('—')

        time.sleep(0.5)  # Photon is more lenient

    if changed:
        print(f'  💾 Išsaugota {filename} ({geocoded} naujos koordinatės)')

print(f'\n✅ Viso geocoduota: {total_geocoded}')
