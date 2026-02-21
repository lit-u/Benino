# Benino Atmintis

## Kas aš esu
Aš esu Benino - AI asistentas Agent Network platformai. Mano tikslas padėti vartotojams su informacija, naujienomis ir žiniomis.

## Mano žinių šaltiniai
- **Vieta**: `documents/blog-news/`
- **Turinys**: 26 sinchronizuoti straipsniai iš Agent Network blogo
- **Tipas**: Viešai prieinamos naujienos, tech straipsniai

### 2. Brain Channels (Privatus turinys)
- **Vieta**: `documents/brain-channels/`
- **Turinys**: Privatūs/brain_capture kanalai su asmenine informacija
- **Kanalai**:
  - 🚀 AI news, vibekodingas, promtai, tendencijos (4 postai)
  - 💼 KRETINGA (1 postas)

### 3. Brain Graph (Grafų atmintis)
- **Vieta**: `documents/brain-graph/`
- **Turinys**: Mintys, temos, sprendimai su ryšiais
- **Statistika**:
  - 41 nodes (thought, note, theme, decision, outcome, question)
  - 124 edges (HAS_THEME, TEMPORAL_NEXT, LED_TO, RESULTED_IN)
  - 28 temų failai
  - 5 dienų mintys

### 4. Cogni-Vault (Žinių struktūrizavimas)
- **UI**: `/brain.html` → Cogni-Vault tab
- **API**: `POST /api/brain/structure-text` (Groq LLM)
- **Funkcija**: Ilgų tekstų struktūrizavimas į temas, citatas, faktus
- **Išsaugojimas**: Struktūrizuoti rezultatai → brain_nodes (source: cogni-vault)

## Kaip rasti informaciją

```bash
# Viešos naujienos
ls documents/blog-news/
read documents/blog-news/[filename].md

# Privatūs brain kanalai
ls documents/brain-channels/
ls documents/brain-channels/[channel-slug]/
read documents/brain-channels/[channel-slug]/[filename].md
```

## Brain OS Architektūra

```
┌─────────────────────────────────────────────┐
│           ĮVESTIES KANALAI                  │
├─────────────┬─────────────┬─────────────────┤
│   SOC       │    Blog     │    Discord      │
│ (brain_cap) │  (public)   │   (dashboard)   │
└──────┬──────┴──────┬──────┴────────┬────────┘
       │             │               │
       ▼             ▼               ▼
┌─────────────────────────────────────────────┐
│              SUPABASE DB                    │
│  brain_nodes ←→ brain_edges (GRAPH)         │
└──────────────────┬──────────────────────────┘
                   │ sync scripts
                   ▼
┌─────────────────────────────────────────────┐
│         OPENCLAW WORKSPACE                  │
│  documents/blog-news/      (26 straipsniai) │
│  documents/brain-channels/ (5 postai)       │
│  documents/brain-graph/    (41 nodes)       │
└─────────────────────────────────────────────┘
```

## OpenClaw Konfigūracija
- **sessionMemory**: `true` (pokalbių istorija indeksuojama)
- **extraPaths**: blog-news, brain-graph, brain-channels
- **Skills**: cogni-vault (žinių struktūrizavimas)

## Dabartinė būsena
- Paskutinis atnaujinimas: 2026-02-03
- Blog straipsniai: 26
- Brain kanalų postai: 5
- Brain graph nodes: 41+
- Brain graph edges: 124
- Cogni-Vault: Aktyvus
- Statusas: Aktyvus
