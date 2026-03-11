# TTS & Avatar Bankas

## TTS Sprendimai

### Nemokama
| Paslauga | Lietuvių | Kokybė | Pastaba |
|---------|----------|--------|---------|
| **gTTS** | ✅ | ⭐⭐ | Google Translate TTS, vienas balsas, kirčiavimas silpnas |
| **Azure F0** | ✅ | ⭐⭐⭐⭐ | 500K simbolių/mėn, Leonas ♂ / Ona ♀ |
| **ElevenLabs Free** | ✅* | ⭐⭐⭐⭐⭐ | 10K simbolių/mėn, savo balso klonas |

### Mokama
| Paslauga | Kaina | Lietuvių | Pastaba |
|---------|-------|----------|---------|
| **ElevenLabs Starter** | $5/mėn | ✅ | 30K simbolių, balso klonas |
| **Azure Neural** | $15/1M simbolių | ✅ | Leonas/Ona Neural balsai |
| **Azure Neural HD** | $30/1M simbolių | ✅ | Aukštesnė kokybė |
| **Netgeist.ai** | $0.10/min | ✅ | 7 LT balsai, lietuviška įmonė |
| **snekos-sinteze.lt** | Komercinė (susisiekti) | ✅ | Intelektika, natyvus LT. Free: 5K simbolių/mėn (neregistr.), 10K/request (registr.) |

### Išbandyta — Kirčiavimas Silpnas
| Paslauga | Lietuvių | Pastaba |
|---------|----------|---------|
| **NaturalReaders** (naturalreaders.com/online) | ✅ | Daug balsų, bet kirčiavimas šlubuoja. Free + mokamas planas |

### Netinka lietuvių kalbai
- ElevenLabs standartiniai balsai (be klonavimo) — nėra LT
- OuteTTS — nėra LT
- Qwen3-TTS — nėra LT
- Kokoro-82M — nėra LT oficialiai

---

## Avatar Sprendimai

### 3D Naršyklėje (TalkingHead)
- **Biblioteka:** github.com/met4citizen/TalkingHead
- **Avatarų šaltinis:** readyplayer.me (nemokama)
- **TTS integracija:** Azure / ElevenLabs / Google
- **Kokybė:** ⭐⭐⭐ (stilizuotas, ne fotorealistinis)
- **Kaina:** Nemokama (tik TTS mokestis)

### Fotorealistinis Video
| Paslauga | Kaina | Lietuvių | Pastaba |
|---------|-------|----------|---------|
| **HeyGen Creator** | $29/mėn | ✅ | 15 min/mėn, Instant Avatar iš 2min video |
| **HeyGen API** | ~$0.30-0.50/min | ✅ | Programinis valdymas |
| **Synthesia** | ~$29+/mėn | ✅ | 140+ kalbų, profesionalūs avatariai |
| **D-ID** | ~$6+/mėn | ❓ | Animacija iš nuotraukos |

### Workflow: EL Balsas + HeyGen Avatar
1. ElevenLabs → sugeneruok audio (savo klonuotas LT balsas)
2. HeyGen → įkelk audio + Instant Avatar (fotorealistinis)
3. Rezultatas: fotorealistinis video su savo balsu lietuviškai

---

## Greito Įgarsinimo Skill
- **Skill:** `workspace/skills/gtts/`
- **Naudojimas:** "Įgarsink šitą tekstą" → OldBoy paleidžia narrate.py → MP3
