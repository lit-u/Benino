#!/usr/bin/env python3
"""
Import scraped JSON data → sekmes.lt public API
Sources: cafes_all_cities.json, prekyba_raw.json
"""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path

API_URL  = "http://localhost:3000/api/admin/import/maxun"
API_KEY  = "ak_77aad7f0459e4f449ded9ba6bb1f820e799e291746be1a2b"
SCRIPTS  = Path(__file__).parent

FOOD_TYPES = {'kavinė','cafe','coffee','kavine','bar','baras','restoranas','restaurant',
              'picerija','pizza','sushi','fastfood','fast food','maitinimas'}

def detect_subcategory(t):
    t = (t or '').lower()
    if any(f in t for f in FOOD_TYPES):
        return 'restaurant'
    return 'service'

def post(items):
    payload = json.dumps(items, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        API_URL, data=payload,
        headers={'Content-Type':'application/json','X-API-Key': API_KEY},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': e.read().decode()}

def import_cafes():
    print("\n── cafes_all_cities.json ──────────────────")
    data = json.load(open(SCRIPTS/'cafes_all_cities.json', encoding='utf-8'))
    items, total_imp, total_skip = [], 0, 0
    for city, lst in data.items():
        for b in lst:
            items.append({
                'name':          b.get('name'),
                'type':          b.get('type',''),
                'subcategory':   detect_subcategory(b.get('type','')),
                'city':          city,
                'phone':         b.get('phone'),
                'website':       b.get('website'),
                'working_hours': b.get('opening_hours'),
            })
            if len(items) >= 20:
                r = post(items)
                total_imp += r.get('imported',0)
                total_skip += r.get('skipped',0)
                print(f"  batch: +{r.get('imported',0)} imported, {r.get('skipped',0)} skipped")
                items = []
                time.sleep(0.3)
    if items:
        r = post(items)
        total_imp += r.get('imported',0)
        total_skip += r.get('skipped',0)
    print(f"  TOTAL: {total_imp} imported, {total_skip} skipped")
    return total_imp

def import_prekyba():
    print("\n── prekyba_raw.json ───────────────────────")
    data = json.load(open(SCRIPTS/'prekyba_raw.json', encoding='utf-8'))
    items, total_imp, total_skip = [], 0, 0
    for city, lst in data.items():
        for b in lst:
            items.append({
                'name':        b.get('name'),
                'type':        b.get('type',''),
                'subcategory': detect_subcategory(b.get('type','')),
                'city':        b.get('city') or city,
                'address':     b.get('address'),
                'phone':       b.get('phone'),
                'email':       b.get('email'),
                'website':     b.get('website'),
                'description': b.get('description'),
                'image_url':   b.get('photo_url'),
                'price_range': None,
            })
            if len(items) >= 20:
                r = post(items)
                total_imp += r.get('imported',0)
                total_skip += r.get('skipped',0)
                print(f"  batch: +{r.get('imported',0)} imported, {r.get('skipped',0)} skipped")
                items = []
                time.sleep(0.3)
    if items:
        r = post(items)
        total_imp += r.get('imported',0)
        total_skip += r.get('skipped',0)
    print(f"  TOTAL: {total_imp} imported, {total_skip} skipped")
    return total_imp

if __name__ == '__main__':
    print("🚀 Importuoju į sekmes.lt API...")
    total = 0
    total += import_cafes()
    total += import_prekyba()
    print(f"\n✅ Viso importuota: {total} įrašų")
