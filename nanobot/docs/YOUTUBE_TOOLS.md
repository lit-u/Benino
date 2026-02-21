# YouTube Tools - Nanobot Integration

## Overview

Nanobot dabar turi 3 naujus įrankius darbui su YouTube:

### 1. **youtube_info** - Video Metadata
Gauti video informaciją (pavadinimą, trukmę, kanalą, aprašymą).

**Pavyzdžiai:**
- "Koks šio video pavadinimas: https://youtube.com/watch?v=..."
- "Kiek laiko trunka šis video?"
- "Ar šis video turi subtitrus?"

### 2. **youtube_subtitles** - Subtitle Download
Parsisiųsti video subtitrus/transkriptą.

**Pavyzdžiai:**
- "Parsisiųsk subtitrus iš https://youtube.com/watch?v=..."
- "Gauk lietuviškus subtitrus iš šio video"
- "Download English subtitles from this video"

**Parametrai:**
- `url` (būtinas): YouTube video nuoroda
- `lang` (optional): Kalbos kodas (default: 'en')
  - Lietuvių: `lt`
  - Anglų: `en`
  - Rusų: `ru`
  - Vokiečių: `de`
  - ir kt.
- `auto` (optional): Ar leisti auto-generuotus subtitrus (default: true)
- `max_chars` (optional): Maksimalus simbolių skaičius (default: 50000)

### 3. **youtube_transcript** - Full Analysis
Gauti IR video informaciją IR pilną transkriptą vienu kartu.

**Pavyzdžiai:**
- "Analizuok šį video: https://youtube.com/watch?v=..."
- "Susumuok kas vyksta šiame video"
- "Ištrauk pagrindinius taškas iš šio video"

## Kaip Naudoti per Nanobot

### Per WhatsApp / CLI

```
Tu: OldBoy, ištrauk subtitrus iš šio video: https://youtube.com/watch?v=dQw4w9WgXcQ

OldBoy: 🤞 Viena akimirka, viešpatie...
[Nanobot calls youtube_subtitles tool]
OldBoy: Štai transkriptas:
[Rick Astley lyrics...]
```

### Per CLI Direct

```powershell
cd nanobot
.\nanobot-env\Scripts\activate
nanobot agent -m "Gauk info apie: https://youtube.com/watch?v=dQw4w9WgXcQ"
```

## Use Cases

### 1. Content Analysis
```
"Susumuok šį podcast epizodą: https://youtube.com/watch?v=..."
→ Nanobot download subtitrus ir sukuria santrauką
```

### 2. Research
```
"Ištrauk visas citatas apie AI iš šio video"
→ Nanobot gauna transkriptą ir ieško citatų
```

### 3. Language Learning
```
"Gauk lietuviškus subtitrus iš šio video"
→ Nanobot parsisiunčia LT subtitrus mokymosi tikslais
```

### 4. Knowledge Base Building
```
"Išanalizuok visus tech talk video iš šios playlist ir išsaugok pagrindinius faktus"
→ Nanobot gali batch process kelis video
```

## Technical Details

### Installation
```bash
pip install yt-dlp  # ✅ Jau įdiegta
```

### Files Added
- `nanobot/src/nanobot/agent/tools/youtube.py` - Tool implementations
- `nanobot/src/nanobot/agent/loop.py` - Tool registration (modified)

### Supported Formats
- **Subtitles**: VTT, SRT, auto-captions
- **Languages**: Any language YouTube supports
- **Video Types**: Public videos with available captions

### Limitations
- ❌ Private/age-restricted videos may not work
- ❌ Very long videos (>2h) may hit character limits
- ⚠️ Auto-captions may have errors (especially for technical content)
- ⚠️ Rate limiting: YouTube may block excessive requests

## Advanced Usage

### Multiple Languages
```python
# Per agent prompt:
"Gauk TIEK anglų TIEK lietuviškus subtitrus iš šio video"

# Agent can call youtube_subtitles twice with different lang params
```

### Chunked Processing
```python
# Per agent:
"Išanalizuok šį 2h video dalimis po 30min"

# Agent can use timestamps + multiple calls
```

### Knowledge Extraction
```python
"Ištrauk struktūrizuotą informaciją (temos, faktai, citatos) iš šio video"

# Agent gali kombine youtube_transcript + Cogni-Vault
```

## Examples from Real World

### Podcast Analysis (2h video)
```
User: "Analizuok 'Lex Fridman Podcast #380 with Yann LeCun'"

OldBoy: 🤞 Viena akimirka, viešpatie...
[calls youtube_info → 2:18:45 duration]
[calls youtube_subtitles lang=en → 50000 chars]
[calls LLM with transcript → structured analysis]

OldBoy: Štai pagrindinės temos:
1. Self-supervised learning...
2. AI safety concerns...
3. Future of AGI...
[Full analysis]
```

### Knowledge Building
```
User: "Eik per visus 'Two Minute Papers' video apie Diffusion Models ir sukurk žinių bazę"

OldBoy: [Batch processes 15 videos]
OldBoy: Sukurta žinių bazė su 127 faktais apie Diffusion Models
```

## Integration with Agent Network

YouTube tools galima integruoti su:
- **Brain Graph** - Išsaugoti video mintis kaip nodes
- **Blog** - Generuoti blog post iš video content
- **SOC** - Share video insights į social feed
- **Cogni-Vault** - Struktūrizuoti video turinį

## Troubleshooting

### "No subtitles found"
→ Check if video has captions: `youtube_info` first
→ Try `auto=true` for auto-generated captions
→ Try different language: `lang=en` instead of `lang=lt`

### "Download failed"
→ Video may be private/restricted
→ YouTube API rate limit (wait 1-2 min)
→ Check internet connection

### "Transcript too long"
→ Use `max_chars` parameter
→ Ask agent to "summarize only first 30 minutes"

## Future Enhancements

- [ ] Audio download + Whisper transcription (for videos without captions)
- [ ] Playlist batch processing
- [ ] Timestamp-specific extraction ("what happens at 15:30?")
- [ ] Multi-language comparison
- [ ] Video thumbnail extraction
- [ ] Comments analysis

---

**Status:** ✅ Production Ready
**Version:** 1.0.0
**Dependencies:** yt-dlp 2026.2.4
**Last Updated:** 2026-02-08
