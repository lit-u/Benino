"""
scrape_rekvizitai.lt — gauna adresą iš juridinio pavadinimo
Strategija:
  1. Slug = name.lower() transliteruotas, spaces->_
  2. GET https://rekvizitai.vz.lt/imone/{slug}/
  3. Adresas: ... iš HTML teksto
  4. Geocode per Nominatim
"""
import json, sys, time, re, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

FILES = [
    ('hotels',   'd:/_PAL/benino/agent-network/public/data/hotels.json'),
    ('kavines',  'd:/_PAL/benino/agent-network/public/data/kavines.json'),
    ('paslaugos','d:/_PAL/benino/agent-network/public/data/paslaugos.json'),
]

LAT_MIN, LAT_MAX, LNG_MIN, LNG_MAX = 55.2, 56.6, 20.5, 21.8
LEGAL_RE = re.compile(r'\b(UAB|MB|IVV|AB|VšĮ)\b', re.I)
REGION_CITIES = ['palanga', 'kretinga', 'šventoji', 'klaipėda', 'neringa', 'nida',
                 'juodkrantė', 'pervalka', 'preila', 'kartena', 'darbėnai']
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120'}
LT_MAP = {'ą':'a','č':'c','ę':'e','ė':'e','į':'i','š':'s','ų':'u','ū':'u','ž':'z',
          'Ą':'a','Č':'c','Ę':'e','Ė':'e','Į':'i','Š':'s','Ų':'u','Ū':'u','Ž':'z'}

def to_slug(name):
    """Įmonės pavadinimas → rekvizitai.lt URL slug."""
    # Remove legal suffix and marketing text
    name = re.sub(r',?\s*(uab|mb|ivv|ab|vši|uždaroji|akcinė)\b.*', '', name, flags=re.I)
    name = name.strip().lower()
    for k, v in LT_MAP.items():
        name = name.replace(k, v)
    name = re.sub(r'[^a-z0-9]+', '_', name).strip('_')
    return name

def get_address(slug):
    """Grąžina adresą arba None."""
    url = f'https://rekvizitai.vz.lt/imone/{slug}/'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='replace')
        m = re.search(r'Adresas:\s*([^\n<"]+)', html)
        if m:
            return m.group(1).strip()
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f'  HTTPError {e.code}')
    except Exception as e:
        print(f'  ERR: {e}')
    return None

def in_region(addr):
    addr_l = addr.lower()
    return any(c in addr_l for c in REGION_CITIES)

def nominatim(query):
    url = ('https://nominatim.openstreetmap.org/search?q='
           + urllib.parse.quote(query) + '&format=json&limit=3&countrycodes=lt')
    req = urllib.request.Request(url, headers={'User-Agent': 'benino-geo/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        for item in data:
            lat, lng = float(item['lat']), float(item['lon'])
            if LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX:
                return lat, lng
    except Exception as e:
        print(f'  nominatim err: {e}')
    return None, None

total_coords = 0
total_addr = 0

for fname, path in FILES:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    found_coords = 0
    found_addr = 0

    for city, items in data.items():
        for e in items:
            if e.get('lat'):
                continue
            if not LEGAL_RE.search(e.get('name', '')):
                continue

            slug = to_slug(e['name'])
            print(f'[{fname}/{city}] {e["name"][:45]!r}')
            print(f'  slug: {slug}', end=' ', flush=True)

            addr = get_address(slug)
            time.sleep(1.2)

            if not addr:
                print('→ not found on rekvizitai')
                continue

            if not in_region(addr):
                print(f'→ out-of-region: {addr[:50]}')
                continue

            print(f'→ {addr[:50]}')

            # Save address
            if not e.get('address'):
                e['address'] = addr
                found_addr += 1

            # Geocode
            lat, lng = nominatim(addr)
            time.sleep(1.1)

            if lat:
                e['lat'] = lat
                e['lng'] = lng
                found_coords += 1
                print(f'  coords: {lat:.5f},{lng:.5f}')
            else:
                # Fallback: name + city
                short = slug.replace('_', ' ')
                lat, lng = nominatim(f'{short} {city} Lietuva')
                time.sleep(1.1)
                if lat:
                    e['lat'] = lat
                    e['lng'] = lng
                    found_coords += 1
                    print(f'  coords (fallback): {lat:.5f},{lng:.5f}')
                else:
                    print('  coords: not found')

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total_coords += found_coords
    total_addr += found_addr
    print(f'--- {fname}: +{found_coords} coords, +{found_addr} addresses ---\n')

print(f'VISO: +{total_coords} koordinatės, +{total_addr} adresai')
