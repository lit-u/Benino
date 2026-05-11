#!/usr/bin/env python3
"""
Generuoja SEO blog postus iš v1 API duomenų naudojant Groq,
tada įrašo tiesiai į Supabase blog_posts lentelę.
"""
import sys, json, re, time, urllib.request, os
sys.stdout.reconfigure(encoding='utf-8')

GROQ_KEY    = os.environ.get("GROQ_API_KEY", "")
GROQ_URL    = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL  = "llama-3.3-70b-versatile"
API_LOCAL   = "http://localhost:3000"
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY", "")

# Jei env nėra, skaitome iš .env failo
if not SUPABASE_URL:
    try:
        for line in open("d:/_PAL/benino/agent-network/.env", encoding='utf-8'):
            line = line.strip()
            if line.startswith("SUPABASE_URL="):
                SUPABASE_URL = line.split("=",1)[1].strip()
            if line.startswith("SUPABASE_SERVICE_ROLE_KEY=") or (not SUPABASE_KEY and line.startswith("SUPABASE_KEY=")):
                SUPABASE_KEY = line.split("=",1)[1].strip()
    except: pass

def api_get(path):
    with urllib.request.urlopen(API_LOCAL + path, timeout=10) as r:
        return json.loads(r.read())

def groq(prompt):
    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": [{"role":"user","content": prompt}],
        "temperature": 0.7, "max_tokens": 1200
    }).encode()
    req = urllib.request.Request(GROQ_URL, data=payload,
        headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()

def slugify(text):
    lt = {'ą':'a','č':'c','ę':'e','ė':'e','į':'i','š':'s','ų':'u','ū':'u','ž':'z'}
    t = text.lower()
    for k,v in lt.items(): t=t.replace(k,v)
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')[:60]

def supabase_insert(post):
    payload = json.dumps(post, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/blog_posts",
        data=payload,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return result[0].get("id") if result else None
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"    Supabase klaida: {err[:200]}")
        return None

TOPICS = [
    {
        "title": "Geriausi restoranai Palangoje 2025: pilnas sąrašas su telefonais",
        "category": "Turizmas",
        "city": "Palanga",
        "endpoint": "/v1/restaurants?city=Palanga&limit=20",
        "prompt_template": """Parašyk lietuvišką SEO straipsnį apie geriausius restoranus Palangoje.
Straipsnio pavadinimas: "{title}"
Čia realūs restoranai iš mūsų duomenų bazės:
{items}

Reikalavimai:
- Apie 600-800 žodžių, HTML formatas (p, h2, h3, ul, li tagai)
- Pradėk su įdomiu įvadu apie Palangos gastronomiją
- Suskirstyk į kategorijas (jūros gėrybės, tradiciniai, tarptautiniai ir pan.)
- Paminėk keletą konkrečių vardų iš sąrašo
- Baik su praktiniais patarimais (rezervacija, sezonas ir pan.)
- Rašyk šnekamąja, patariančia lietuviška kalba
- NE: nenaudok markdown (#, **, *), tik HTML"""
    },
    {
        "title": "Ką veikti Neringoje: atrakcijos, kopų takai ir įdomybės",
        "category": "Turizmas",
        "city": "Neringa",
        "endpoint": "/v1/services?city=Neringa&limit=20",
        "prompt_template": """Parašyk lietuvišką SEO straipsnį apie Neringos atrakcijas ir veiklas.
Straipsnio pavadinimas: "{title}"
Realūs objektai:
{items}

Reikalavimai:
- Apie 600-800 žodžių, HTML formatas
- Gamtos atrakcijos (Parnidžio kopa, Saulės laikrodis ir kt.)
- Aktyvus poilsis, dviračių takai
- Kultūros ir istorijos vietos
- Praktiniai patarimai (kaip nuvykti, sezonai)
- Šnekamoji lietuviška kalba, be markdown"""
    },
    {
        "title": "SPA ir relaksas Palangoje: masažai, saunos ir grožio salonai",
        "category": "Sveikata",
        "city": "Palanga",
        "endpoint": "/v1/services?city=Palanga&limit=50",
        "filter_types": ["SPA","Masažo salonas","Pirtis / sauna","Baseinas","Grožio salonas","Kirpykla"],
        "prompt_template": """Parašyk lietuvišką SEO straipsnį apie SPA ir relaksą Palangoje.
Straipsnio pavadinimas: "{title}"
Realūs objektai (SPA, masažai, grožio salonai):
{items}

Reikalavimai:
- Apie 600 žodžių, HTML formatas
- Jūros oro ir SPA derinys — kodėl Palanga ideali
- Skirtingų procedūrų apžvalga (masažai, grožio procedūros, saunos)
- Keletas konkretių vietų iš sąrašo
- Praktiniai patarimai (rezervacija iš anksto, sezonas)
- Šnekamoji kalba, be markdown"""
    },
    {
        "title": "Dviračių nuoma Palangoje ir Neringoje: kainos, maršrutai, patarimai",
        "category": "Sportas",
        "city": "Palanga",
        "endpoint": "/v1/services?city=Palanga&limit=50",
        "filter_types": ["Dviračių nuoma","Dviračiai","Vandens sportas"],
        "prompt_template": """Parašyk lietuvišką SEO straipsnį apie dviračių nuomą pajūryje.
Straipsnio pavadinimas: "{title}"
Realūs objektai:
{items}

Reikalavimai:
- Apie 600 žodžių, HTML formatas
- Dviračių takai Palangoje ir Neringoje
- Nuomos vietos ir apytikslės kainos
- Rekomenduojami maršrutai (kopų takas, pajūrio takas)
- Šeimoms tinkamos vietos
- Šnekamoji kalba, be markdown"""
    },
    {
        "title": "Stovyklavietės ir kempingai pajūryje: Palanga, Šventoji, Neringa",
        "category": "Turizmas",
        "city": "Palanga",
        "endpoint": "/v1/services?limit=100",
        "filter_types": ["Stovyklavietė","Kempingas","Poilsiavietė"],
        "prompt_template": """Parašyk lietuvišką SEO straipsnį apie stovyklavietes pajūryje.
Straipsnio pavadinimas: "{title}"
Realūs objektai:
{items}

Reikalavimai:
- Apie 600 žodžių, HTML formatas
- Stovyklavimas pajūryje — gamta, jūra, miškai
- Konkretūs objektai iš sąrašo
- Ką pasiimti, kada važiuoti, kainos
- Šeimų ir solo keliaujančiųjų patarimai
- Šnekamoji kalba, be markdown"""
    },
]

def main():
    print("✍️  Blog postų generavimas\n", flush=True)

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Trūksta SUPABASE_URL arba SUPABASE_KEY")
        return

    for topic in TOPICS:
        print(f"── {topic['title'][:60]}", flush=True)

        # Gauti duomenis
        try:
            data = api_get(topic["endpoint"])
            items = data.get("data", [])
            if topic.get("filter_types"):
                items = [x for x in items if x.get("type") in topic["filter_types"]]
            items = items[:15]
        except Exception as e:
            print(f"  API klaida: {e}", flush=True)
            items = []

        items_text = "\n".join(
            f"- {it.get('title','')} ({it.get('city','')}) — tel: {it.get('phone','–')} svetainė: {it.get('website','–')}"
            for it in items
        ) or "(nėra konkrečių duomenų — rašyk bendriau)"

        prompt = topic["prompt_template"].format(title=topic["title"], items=items_text)

        try:
            content = groq(prompt)
            print(f"  Sugeneruota: {len(content)} simbolių", flush=True)
        except Exception as e:
            print(f"  Groq klaida: {e}", flush=True)
            continue

        slug = slugify(topic["title"])
        post = {
            "title":            topic["title"],
            "slug":             slug,
            "content":          content,
            "excerpt":          content[:200].replace("<p>","").replace("</p>","").strip() + "...",
            "category":         topic["category"],
            "author":           "OldBoy-RSS",
            "is_published":     True,
            "is_featured":      False,
            "meta_title":       topic["title"],
            "meta_description": content[:155].replace("<p>","").replace("</p>","").strip(),
        }

        post_id = supabase_insert(post)
        if post_id:
            print(f"  ✅ Įrašyta: /blog/{slug}", flush=True)
        else:
            print(f"  ⚠ Nepavyko įrašyti", flush=True)

        time.sleep(2)

    print("\n✅ Baigta", flush=True)

if __name__ == "__main__":
    main()
