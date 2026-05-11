# -*- coding: utf-8 -*-
"""
Scrape papildomos kategorijos iš OpenStreetMap Overpass API:
SPA, grožio salonai, automobilių nuoma, dviračiai, stovyklavietės,
muziejai, atrakcijos, kempingai, paplūdimiai, sportas.
Rezultatas: scripts/papildomos_raw.json
"""
import sys, json, time, urllib.request, urllib.parse, re
sys.stdout.reconfigure(encoding='utf-8')

CITIES = {
    'Palanga':    (55.9175, 21.0708, 4000),
    'Šventoji':   (56.0308, 21.0717, 2500),
    'Kretinga':   (55.8897, 21.2442, 3000),
    'Klaipėda':   (55.7103, 21.1443, 6000),
    'Nida':       (55.3086, 21.0123, 3000),
    'Neringa':    (55.4500, 21.0500, 5000),
    'Šilutė':     (55.3500, 21.4800, 3000),
    'Gargždai':   (55.7100, 21.3900, 3000),
}

OVERPASS = "https://overpass-api.de/api/interpreter"

# OSM tag → tipo pavadinimas lietuviškai
TYPE_MAP = {
    # amenity=
    'spa':              'SPA',
    'beauty':           'Grožio salonas',
    'hairdresser':      'Kirpykla',
    'massage':          'Masažo salonas',
    'gym':              'Sporto salė',
    'sports_centre':    'Sporto centras',
    'swimming_pool':    'Baseinas',
    'car_rental':       'Automobilių nuoma',
    'car_wash':         'Automazgykla',
    'bicycle_rental':   'Dviračių nuoma',
    'boat_rental':      'Valtis / nuoma',
    'casino':           'Kazino',
    'cinema':           'Kino teatras',
    'nightclub':        'Naktinis klubas',
    'theatre':          'Teatras',
    'museum':           'Muziejus',
    'arts_centre':      'Kultūros centras',
    'community_centre': 'Bendruomenės centras',
    'place_of_worship': 'Bažnyčia',
    # tourism=
    'attraction':       'Atrakcija',
    'camp_site':        'Stovyklavietė',
    'caravan_site':     'Kempingas',
    'picnic_site':      'Poilsiavietė',
    'viewpoint':        'Apžvalgos taškas',
    'aquarium':         'Akvariumas',
    'gallery':          'Galerija',
    'theme_park':       'Pramogų parkas',
    'zoo':              'Zoologijos sodas',
    # leisure=
    'beach':            'Paplūdimys',
    'playground':       'Žaidimų aikštelė',
    'miniature_golf':   'Golfo aikštelė',
    'bowling_alley':    'Boulingas',
    'escape_game':      'Bėgimo žaidimas',
    'sauna':            'Pirtis / sauna',
    # shop=
    'bicycle':          'Dviračiai',
    'surf':             'Vandens sportas',
    'sports':           'Sporto prekės',
    'massage':          'Masažo salonas',
    'beauty':           'Grožio salonas',
    'hairdresser':      'Kirpykla',
    'cosmetics':        'Kosmetika',
    'tattoo':           'Tatuiruočių salonas',
}

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; PajurioBot/1.0)'}

def overpass_query(lat, lng, radius):
    return f"""
[out:json][timeout:30];
(
  node["amenity"~"spa|beauty|hairdresser|massage|gym|sports_centre|swimming_pool|car_rental|car_wash|bicycle_rental|boat_rental|casino|cinema|nightclub|theatre|museum|arts_centre|community_centre"](around:{radius},{lat},{lng});
  node["tourism"~"attraction|camp_site|caravan_site|picnic_site|viewpoint|aquarium|gallery|theme_park|zoo"](around:{radius},{lat},{lng});
  node["leisure"~"beach|playground|miniature_golf|bowling_alley|sauna"](around:{radius},{lat},{lng});
  node["shop"~"bicycle|surf|sports|cosmetics|tattoo"](around:{radius},{lat},{lng});
  way["amenity"~"spa|museum|arts_centre|sports_centre|swimming_pool|cinema|theatre"](around:{radius},{lat},{lng});
  way["tourism"~"attraction|camp_site|theme_park|zoo"](around:{radius},{lat},{lng});
  way["leisure"~"beach|playground|miniature_golf"](around:{radius},{lat},{lng});
);
out center tags;
"""

def fetch(query):
    data = urllib.parse.urlencode({'data': query}).encode()
    req = urllib.request.Request(OVERPASS, data=data, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read())

def detect_type(tags):
    for key in ('amenity', 'tourism', 'leisure', 'shop'):
        val = tags.get(key, '')
        if val in TYPE_MAP:
            return TYPE_MAP[val]
    return None

def parse_address(tags):
    parts = []
    if tags.get('addr:street'):
        parts.append(tags['addr:street'])
    if tags.get('addr:housenumber'):
        parts.append(tags['addr:housenumber'])
    if tags.get('addr:city'):
        parts.append(tags['addr:city'])
    return ', '.join(parts) if parts else None

def main():
    results = {}
    total = 0

    for city, (lat, lng, radius) in CITIES.items():
        print(f"\n── {city} ──────────────────", flush=True)
        try:
            raw = fetch(overpass_query(lat, lng, radius))
        except Exception as e:
            print(f"  ERR: {e}", flush=True)
            time.sleep(5)
            continue

        items = []
        seen = set()
        for el in raw.get('elements', []):
            tags = el.get('tags', {})
            name = tags.get('name') or tags.get('name:lt')
            if not name:
                continue
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)

            typ = detect_type(tags)
            if not typ:
                continue

            # Koordinatės
            if el['type'] == 'way':
                c = el.get('center', {})
                elat, elng = c.get('lat'), c.get('lon')
            else:
                elat, elng = el.get('lat'), el.get('lon')

            item = {
                'name':        name,
                'type':        typ,
                'city':        city,
                'address':     parse_address(tags),
                'phone':       tags.get('phone') or tags.get('contact:phone'),
                'website':     tags.get('website') or tags.get('contact:website'),
                'description': tags.get('description'),
                'lat':         elat,
                'lng':         elng,
                'opening_hours': tags.get('opening_hours'),
            }
            items.append(item)

        results[city] = items
        total += len(items)
        print(f"  {len(items)} objektų", flush=True)
        time.sleep(1.5)

    out = 'scripts/papildomos_raw.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Viso: {total} objektų → {out}", flush=True)

if __name__ == '__main__':
    main()
