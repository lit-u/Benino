import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from collections import Counter

data = json.load(open('d:/_PAL/benino/workspace/_tmp/priejuros_raw.json', encoding='utf-8'))

by_city = Counter(d['city'] for d in data)
by_cat = Counter(d['category'] for d in data)
print('By city:')
for k,v in by_city.most_common(): print(f'  {k}: {v}')
print('By category:')
for k,v in by_cat.most_common(): print(f'  {k}: {v}')

existing = set()
for f in ['hotels','kavines','paslaugos','sveikatos']:
    d2 = json.load(open(f'd:/_PAL/benino/agent-network/public/data/{f}.json', encoding='utf-8'))
    for city, places in d2.items():
        for p in places: existing.add(p['name'].lower().strip())

new = [d for d in data if d['name'].lower().strip() not in existing]
has_email = sum(1 for d in data if d.get('email'))
has_web   = sum(1 for d in data if d.get('website'))

print(f'\nTotal scraped:  {len(data)}')
print(f'New entries:    {len(new)}')
print(f'With email:     {has_email}')
print(f'With website:   {has_web}')

print('\nSample new entries:')
for d in new[:15]:
    print(f'  {d["name"][:45]} | {d["city"]} | {d["category"]} | {d.get("email","—")}')
