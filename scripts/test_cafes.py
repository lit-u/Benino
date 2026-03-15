# -*- coding: utf-8 -*-
"""Test: scrape cafes/restaurants using Scrapling - DynamicFetcher"""
import sys, asyncio, json
sys.stdout.reconfigure(encoding='utf-8')
from scrapling.fetchers import DynamicFetcher

# Overpass API - OpenStreetMap, nemokamas, be JS, turi opening_hours
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

CITIES = {
    'Sventoji':  (56.0308, 21.0717),
    'Palanga':   (55.9175, 21.0708),
    'Nida':      (55.3086, 21.0123),
}

async def get_cafes_overpass(city_name: str, lat: float, lng: float):
    query = f"""
[out:json][timeout:10];
(
  node["amenity"~"restaurant|cafe|bar|fast_food"](around:3000,{lat},{lng});
);
out body;
"""
    fetcher = DynamicFetcher(headless=True)
    # Overpass yra POST request - naudosim paprastą fetch
    import urllib.request, urllib.parse
    data = urllib.parse.urlencode({'data': query}).encode()
    req = urllib.request.Request(OVERPASS_URL, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())

    places = []
    for el in result.get('elements', []):
        tags = el.get('tags', {})
        name = tags.get('name')
        if not name:
            continue
        oh = tags.get('opening_hours', '')
        amenity = tags.get('amenity', '')
        lat2 = el.get('lat', lat)
        lng2 = el.get('lon', lng)
        maps_link = f"https://www.google.com/maps?q={lat2},{lng2}"
        places.append({
            'name': name,
            'type': amenity,
            'opening_hours': oh or None,
            'link': maps_link,
        })
    return places

async def main():
    for city, (lat, lng) in CITIES.items():
        print(f"\n--- {city} ---")
        try:
            places = await get_cafes_overpass(city, lat, lng)
            print(f"  Rasta: {len(places)}")
            for p in places[:10]:
                oh = p['opening_hours'] or 'laikas nezinomas'
                print(f"  [{p['type']}] {p['name']} | {oh}")
        except Exception as e:
            print(f"  KLAIDA: {e}")

if __name__ == '__main__':
    asyncio.run(main())
