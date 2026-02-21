#!/usr/bin/env python3
"""
video_pipeline.py - Video Content Pipeline

Usage: python video_pipeline.py <URL> [--skip-video] [--tts-only "text"]

Full pipeline:
1. Download video + subtitles (yt-dlp)
2. Extract audio (ffmpeg)
3. Transcribe speech â†’ text (faster-whisper)
4. Analyze content + find sources (Groq LLM)
5. Generate informative script (Groq LLM)
6. Generate voice-over (edge-tts, Lithuanian)
7. Assemble final video (ffmpeg/moviepy)

Output: workspace/video/output/{date}_{slug}/
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

# Resolve paths
SCRIPT_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SCRIPT_DIR.parent.parent  # d:\_PAL\benino
WORKSPACE_DIR = ROOT_DIR / "workspace"
VIDEO_DIR = WORKSPACE_DIR / "video"
OUTPUT_DIR = VIDEO_DIR / "output"
TMP_DIR = VIDEO_DIR / "tmp"
CONFIG_PATH = ROOT_DIR / "nanobot" / "config.json"

# Colors for terminal
class C:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    RED = "\033[31m"
    BOLD = "\033[1m"


def log(emoji, msg, color=C.RESET):
    text = f"{color}{emoji} {msg}{C.RESET}"
    try:
        print(text)
    except UnicodeEncodeError:
        # Windows cp1252 can't handle emoji/Lithuanian chars
        safe = text.encode("ascii", errors="replace").decode("ascii")
        print(safe)


def load_config():
    """Load API keys from nanobot config.json."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        return {
            "gemini_key": cfg.get("providers", {}).get("gemini", {}).get("apiKey", ""),
            "groq_key": cfg.get("providers", {}).get("groq", {}).get("apiKey", ""),
            "brave_key": cfg.get("tools", {}).get("web", {}).get("search", {}).get("apiKey", ""),
        }
    return {
        "gemini_key": os.environ.get("GEMINI_API_KEY", ""),
        "groq_key": os.environ.get("GROQ_API_KEY", ""),
        "brave_key": "",
    }


def ytdlp_cmd():
    """Return the correct yt-dlp command (binary or python module)."""
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    return [sys.executable, "-m", "yt_dlp"]
    
def slugify(text):
    """Convert text to filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '_', text)
    return text[:60]



def normalize_video_url(url):
    """Normalize known URL variants that may confuse extractors."""
    try:
        parsed = urllib.parse.urlparse(url)
        host = (parsed.netloc or "").lower()
        path = parsed.path or ""
    except Exception:
        return url

    # yt-dlp handles Twitter extractor paths more consistently in some setups.
    if host in {"x.com", "www.x.com", "mobile.x.com"} and path.startswith("/i/status/"):
        normalized = f"https://twitter.com{path}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return normalized

    return url


def has_source_subtitles(url):
    """Quick preflight check: does extractor report subtitles for this URL."""
    normalized_url = normalize_video_url(url)
    cmd = ytdlp_cmd() + [
        "--skip-download",
        "--list-subs",
        "--no-playlist",
        "--socket-timeout", "20",
        "--retries", "1",
        normalized_url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        return False

    output = f"{result.stdout}\n{result.stderr}".lower()
    if "has no subtitles" in output:
        return False
    return result.returncode == 0


# ============================================================
# STEP 1: Download Video
# ============================================================

def download_video(url, output_dir):
    """Download video + subtitles using yt-dlp."""
    normalized_url = normalize_video_url(url)
    log("📥", f"Downloading: {normalized_url}", C.BLUE)

    # Use %(ext)s so yt-dlp picks the right extension
    video_template = str(output_dir / "source.%(ext)s")
    attempt_cmds = [
        (
            "full",
            ytdlp_cmd() + [
                "-o", video_template,
                "--write-subs", "--write-auto-subs",
                "--sub-lang", "lt,en,ru",
                "--sub-format", "srt",
                "--merge-output-format", "mp4",
                "--no-playlist",
                "--socket-timeout", "20",
                "--retries", "2",
                "--fragment-retries", "2",
                "--js-runtimes", "node",
                "--quiet", "--progress",
                normalized_url,
            ],
            240,
        ),
    ]

    if "twitter.com/i/status/" in normalized_url:
        attempt_cmds.append(
            (
                "twitter_fallback",
                ytdlp_cmd() + [
                    "-o", video_template,
                    "--write-auto-subs",
                    "--sub-lang", "en,lt,ru",
                    "--sub-format", "srt",
                    "--merge-output-format", "mp4",
                    "--extractor-args", "twitter:api=syndication",
                    "--no-playlist",
                    "--socket-timeout", "20",
                    "--retries", "1",
                    "--fragment-retries", "1",
                    "--js-runtimes", "node",
                    "--quiet", "--progress",
                    normalized_url,
                ],
                180,
            )
        )

    attempt_cmds.append(
        (
            "simple",
            ytdlp_cmd() + [
                "-o", video_template,
                "--no-playlist",
                "--socket-timeout", "20",
                "--retries", "1",
                "--fragment-retries", "1",
                "--js-runtimes", "node",
                normalized_url,
            ],
            180,
        )
    )

    for attempt_name, cmd, timeout_sec in attempt_cmds:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
            if result.returncode == 0:
                break
            log("⚠️", f"yt-dlp {attempt_name} failed: {result.stderr[:200]}", C.YELLOW)
        except subprocess.TimeoutExpired:
            log("⚠️", f"yt-dlp {attempt_name} timed out after {timeout_sec}s, retrying...", C.YELLOW)

    # Find the downloaded video file (could be .mp4, .mkv, .webm)
    video_path = None
    for f in sorted(output_dir.glob("source.*"), key=lambda p: p.stat().st_size, reverse=True):
        if f.suffix in [".mp4", ".mkv", ".webm", ".mp3"]:
            video_path = f
            break

    if video_path and video_path.exists():
        size_mb = video_path.stat().st_size / (1024 * 1024)
        log("✅", f"Downloaded: {video_path.name} ({size_mb:.1f} MB)", C.GREEN)
    else:
        video_path = None

    # Find subtitle files
    subs = list(output_dir.glob("source*.srt")) + list(output_dir.glob("source*.vtt"))
    if subs:
        log("📝", f"Subtitles found: {[s.name for s in subs]}", C.CYAN)

    return video_path, subs


# ============================================================
# STEP 2: Extract Audio
# ============================================================

def extract_audio(video_path, output_dir):
    """Extract audio track as MP3."""
    log("ðŸ”Š", "Extracting audio...", C.BLUE)

    audio_path = output_dir / "source_audio.mp3"
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vn", "-acodec", "libmp3lame", "-q:a", "2",
        "-y", str(audio_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if audio_path.exists():
        log("âœ…", f"Audio extracted: {audio_path.name}", C.GREEN)
    else:
        log("âŒ", f"Audio extraction failed: {result.stderr[:200]}", C.RED)

    return audio_path


# ============================================================
# STEP 3: Extract Keyframes
# ============================================================

def extract_keyframes(video_path, output_dir, interval=5):
    """Extract keyframes every N seconds."""
    log("ðŸ–¼ï¸", f"Extracting keyframes every {interval}s...", C.BLUE)

    frames_dir = output_dir / "frames"
    frames_dir.mkdir(exist_ok=True)

    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", f"fps=1/{interval}",
        "-y", str(frames_dir / "frame_%03d.jpg")
    ]

    subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    frames = list(frames_dir.glob("*.jpg"))
    log("âœ…", f"Extracted {len(frames)} keyframes", C.GREEN)
    return frames


# ============================================================
# STEP 4: Transcribe
# ============================================================

def transcribe(audio_path, subtitle_files=None, require_subtitles=True):
    """Transcribe audio to text. Uses subtitles first; optional whisper fallback."""

    # Try subtitles first
    if subtitle_files:
        for sub_file in subtitle_files:
            try:
                text = sub_file.read_text(encoding="utf-8", errors="ignore")
                # Strip SRT formatting
                lines = []
                for line in text.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    if re.match(r'^\d+$', line):
                        continue
                    if re.match(r'\d{2}:\d{2}', line):
                        continue
                    line = re.sub(r'<[^>]+>', '', line)  # Remove HTML tags
                    if line:
                        lines.append(line)

                clean_text = " ".join(lines)
                if len(clean_text) > 50:
                    log("ðŸ“", f"Using subtitles from {sub_file.name} ({len(clean_text)} chars)", C.GREEN)
                    return clean_text
            except Exception:
                continue

    if require_subtitles:
        log("❌", "No usable subtitles found. Stopping because subtitles are required.", C.RED)
        return ""

    # Fallback to faster-whisper
    log("ðŸŽ¤", "Transcribing with faster-whisper (this may take a minute)...", C.BLUE)

    try:
        from faster_whisper import WhisperModel

        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, info = model.transcribe(
            str(audio_path),
            language=None,  # auto-detect
            beam_size=5
        )

        text_parts = []
        for segment in segments:
            text_parts.append(segment.text)

        full_text = " ".join(text_parts)
        log("âœ…", f"Transcribed: {len(full_text)} chars, language: {info.language}", C.GREEN)
        return full_text

    except Exception as e:
        log("âŒ", f"Transcription failed: {e}", C.RED)
        return ""


# ============================================================
# STEP 5: LLM Analysis (Groq)
# ============================================================

def call_llm(config, system_prompt, user_prompt, json_mode=False):
    """Call LLM API (Gemini preferred, Groq fallback)."""
    import urllib.request

    gemini_key = config.get("gemini_key", "")
    groq_key = config.get("groq_key", "")

    # Try Gemini first (free tier, reliable)
    if gemini_key:
        try:
            return _call_gemini(gemini_key, system_prompt, user_prompt, json_mode)
        except Exception as e:
            log("âš ï¸", f"Gemini failed: {e}, trying Groq...", C.YELLOW)

    # Fallback to Groq
    if groq_key:
        return _call_groq(groq_key, system_prompt, user_prompt, json_mode)

    raise RuntimeError("No LLM API key available (need Gemini or Groq)")


def _call_gemini(api_key, system_prompt, user_prompt, json_mode=False):
    """Call Google Gemini API."""
    import urllib.request

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    body = {
        "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4000,
        },
    }

    if json_mode:
        body["generationConfig"]["responseMimeType"] = "application/json"

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())
        return result["candidates"][0]["content"]["parts"][0]["text"]


def _call_groq(api_key, system_prompt, user_prompt, json_mode=False):
    """Call Groq API."""
    import urllib.request

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
    }

    if json_mode:
        body["response_format"] = {"type": "json_object"}

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=data,
        headers=headers,
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())
        return result["choices"][0]["message"]["content"]


def analyze_content(transcript, config):
    """Analyze transcript: identify topics, suggest search queries, generate script."""
    log("ðŸ§ ", "Analyzing content with AI...", C.BLUE)

    # Step 1: Analyze and identify topics
    analysis = call_llm(
        config,
        system_prompt="""Tu esi turinio analitikas. Analizuok video transkripcijÄ… ir pateik JSON:
{
  "title": "Trumpas video pavadinimas lietuviÅ¡kai",
  "topics": ["tema1", "tema2", "tema3"],
  "key_facts": ["faktas1", "faktas2", "faktas3"],
  "search_queries": ["paieÅ¡kos uÅ¾klausa originaliam Å¡altiniui 1", "uÅ¾klausa 2"],
  "youtube_search": ["YouTube paieÅ¡kos terminas 1", "terminas 2"],
  "summary": "2-3 sakiniÅ³ santrauka lietuviÅ¡kai",
  "language": "detected language code"
}""",
        user_prompt=f"Analizuok Å¡iÄ… video transkripcijÄ…:\n\n{transcript[:3000]}",
        json_mode=True,
    )

    try:
        analysis_data = json.loads(analysis)
    except json.JSONDecodeError:
        analysis_data = {
            "title": "Video analizÄ—",
            "topics": [],
            "key_facts": [],
            "search_queries": [],
            "youtube_search": [],
            "summary": analysis[:500],
            "language": "unknown",
        }

    log("âœ…", f"Topics: {analysis_data.get('topics', [])}", C.GREEN)
    return analysis_data


def generate_script(analysis_data, transcript, config):
    """Generate an informative Lithuanian script for voice-over."""
    log("ðŸ“", "Generating informative script...", C.BLUE)

    script = call_llm(
        config,
        system_prompt="""Tu esi profesionalus informaciniÅ³ video scenarijÅ³ raÅ¡ytojas.
RaÅ¡yk lietuviÅ¡kai. Stilius: aiÅ¡kus, informatyvus, patrauklus.
Scenarijus turi bÅ«ti skirtas voice-over Ä¯garsinimui (1-3 minutÄ—s kalbos).
StruktÅ«ra:
1. Ä®Å¾anga (patraukli pradÅ¾ia, 2-3 sakiniai)
2. PagrindinÄ— dalis (faktai, analizÄ—, 5-8 sakiniai)
3. Pabaiga (iÅ¡vada arba klausimas Å¾iÅ«rovui, 2 sakiniai)

NeraÅ¡yk techniniÅ³ nuorodÅ³ (timestamp, kadro numerio). Tik grynas tekstas kalbÄ—jimui.""",
        user_prompt=f"""Sukurk informacinÄ¯ scenarijÅ³ pagal Å¡iÄ… analizÄ™:

Pavadinimas: {analysis_data.get('title', '')}
Temos: {', '.join(analysis_data.get('topics', []))}
Faktai: {', '.join(analysis_data.get('key_facts', []))}
Santrauka: {analysis_data.get('summary', '')}

Originali transkripcija (kontekstui):
{transcript[:2000]}""",
    )

    log("âœ…", f"Script generated: {len(script)} chars", C.GREEN)
    return script


# ============================================================
# STEP 6: Find Original Sources
# ============================================================

def find_sources(analysis_data, brave_key=""):
    """Search for original source videos/articles."""
    log("ðŸ”", "Searching for original sources...", C.BLUE)

    sources = []

    # YouTube search via yt-dlp
    for query in analysis_data.get("youtube_search", [])[:3]:
        try:
            cmd = ytdlp_cmd() + [
                "--flat-playlist",
                "--print", "%(title)s ||| %(url)s",
                f"ytsearch3:{query}",
                "--quiet"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            for line in result.stdout.strip().split("\n"):
                if "|||" in line:
                    title, url = line.split("|||", 1)
                    sources.append({
                        "type": "youtube",
                        "title": title.strip(),
                        "url": url.strip(),
                        "query": query,
                    })
        except Exception as e:
            log("âš ï¸", f"YouTube search failed for '{query}': {e}", C.YELLOW)

    # Brave web search (if API key available)
    if brave_key:
        for query in analysis_data.get("search_queries", [])[:2]:
            try:
                import urllib.request
                req = urllib.request.Request(
                    f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}&count=3",
                    headers={"X-Subscription-Token": brave_key, "Accept": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read())
                    for r in data.get("web", {}).get("results", []):
                        sources.append({
                            "type": "web",
                            "title": r.get("title", ""),
                            "url": r.get("url", ""),
                            "description": r.get("description", ""),
                        })
            except Exception as e:
                log("âš ï¸", f"Brave search failed: {e}", C.YELLOW)

    log("âœ…", f"Found {len(sources)} potential sources", C.GREEN)
    for s in sources[:5]:
        log("  ðŸ“Œ", f"[{s['type']}] {s['title'][:60]}", C.CYAN)

    return sources


# ============================================================
# STEP 7: Text-to-Speech (edge-tts)
# ============================================================

async def generate_voiceover(text, output_path, voice="lt-LT-LeonasNeural"):
    """Generate Lithuanian voice-over using edge-tts."""
    log("ðŸŽ™ï¸", f"Generating voice-over ({voice})...", C.BLUE)

    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))

    if output_path.exists():
        size_kb = output_path.stat().st_size / 1024
        log("âœ…", f"Voice-over: {output_path.name} ({size_kb:.0f} KB)", C.GREEN)
    else:
        log("âŒ", "Voice-over generation failed", C.RED)

    return output_path


# ============================================================
# STEP 8: Assemble Video
# ============================================================

def assemble_video(frames_dir, voiceover_path, output_path, script_text=""):
    """Assemble final video from keyframes + voiceover."""
    log("ðŸŽ¬", "Assembling final video...", C.BLUE)

    frames = sorted(frames_dir.glob("*.jpg"))
    if not frames:
        log("âš ï¸", "No keyframes to assemble", C.YELLOW)
        return None

    # Get voiceover duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(voiceover_path)
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_duration = float(result.stdout.strip()) if result.stdout.strip() else 60.0

    # Calculate duration per frame
    duration_per_frame = audio_duration / max(len(frames), 1)

    # Create slideshow with ffmpeg
    # Write concat file
    concat_file = frames_dir.parent / "frames_list.txt"
    with open(concat_file, "w") as f:
        for frame in frames:
            f.write(f"file '{frame}'\n")
            f.write(f"duration {duration_per_frame:.2f}\n")
        # Add last frame again (ffmpeg concat requirement)
        f.write(f"file '{frames[-1]}'\n")

    cmd = [
        "ffmpeg",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(voiceover_path),
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1:color=black",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        "-y", str(output_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        log("âœ…", f"Video assembled: {output_path.name} ({size_mb:.1f} MB)", C.GREEN)
    else:
        log("âŒ", f"Video assembly failed: {result.stderr[:300]}", C.RED)

    return output_path


# ============================================================
# STEP 9: Save Results
# ============================================================

def save_results(project_dir, analysis, script_text, sources, transcript):
    """Save all text results as markdown."""
    report_path = project_dir / "README.md"

    content = f"""# {analysis.get('title', 'Video Analysis')}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Santrauka
{analysis.get('summary', '')}

## Temos
{chr(10).join(f'- {t}' for t in analysis.get('topics', []))}

## Pagrindiniai Faktai
{chr(10).join(f'- {f}' for f in analysis.get('key_facts', []))}

## Scenarijus (Voice-over)

{script_text}

## Rasti Å altiniai

"""
    for s in sources:
        content += f"- [{s.get('title', 'Source')}]({s.get('url', '')}) ({s['type']})\n"

    content += f"""
## Originali Transkripcija

{transcript[:5000]}

## Failai
- `source.mp4` - originalus video
- `source_audio.mp3` - audio takelis
- `voiceover.mp3` - Ä¯garsinimas lietuviÅ¡kai
- `final.mp4` - galutinis informacinis klipas
- `frames/` - keyframes
"""

    report_path.write_text(content, encoding="utf-8")
    log("ðŸ“„", f"Report saved: {report_path.name}", C.GREEN)
    return report_path


# ============================================================
# TTS-Only Mode
# ============================================================

async def tts_only(text, output_path=None, voice="lt-LT-LeonasNeural"):
    """Generate voice-over only, without video pipeline."""
    if not output_path:
        slug = slugify(text[:30])
        output_path = OUTPUT_DIR / f"tts_{slug}.mp3"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    await generate_voiceover(text, output_path, voice)
    print(f"\nOutput: {output_path}")
    return output_path


# ============================================================
# MAIN PIPELINE
# ============================================================

async def run_pipeline(url, skip_video=False, require_subtitles=True):
    """Run the full video pipeline."""
    start_time = time.time()

    log("ðŸš€", f"Video Pipeline Start: {url}", C.BOLD)
    print("=" * 60)

    if require_subtitles and not has_source_subtitles(url):
        log("❌", "This video has no source subtitles. Stopping by requirement.", C.RED)
        sys.exit(1)

    # Load config
    config = load_config()
    if not config["gemini_key"] and not config["groq_key"]:
        log("âŒ", "No LLM API key found in nanobot/config.json (need Gemini or Groq)", C.RED)
        sys.exit(1)

    # Create project directory
    date_str = datetime.now().strftime("%Y-%m-%d")
    project_slug = slugify(url.split("/")[-1] or "video")
    project_dir = OUTPUT_DIR / f"{date_str}_{project_slug}"
    project_dir.mkdir(parents=True, exist_ok=True)
    log("ðŸ“", f"Project: {project_dir.name}", C.CYAN)

    # Step 1: Download
    video_path, subs = download_video(url, project_dir)
    if not video_path or not video_path.exists():
        log("âŒ", "Download failed. Check URL.", C.RED)
        sys.exit(1)

    # Step 2: Extract audio
    audio_path = extract_audio(video_path, project_dir)

    # Step 3: Extract keyframes
    frames = extract_keyframes(video_path, project_dir, interval=5)

    # Step 4: Transcribe
    transcript = transcribe(audio_path, subs, require_subtitles=require_subtitles)
    if not transcript:
        if require_subtitles:
            log("❌", "No full subtitles available for this video. Pipeline stopped.", C.RED)
        else:
            log("âŒ", "No transcript available", C.RED)
        sys.exit(1)

    # Save transcript
    (project_dir / "transcript.txt").write_text(transcript, encoding="utf-8")

    # Step 5: Analyze
    analysis = analyze_content(transcript, config)
    (project_dir / "analysis.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Step 6: Find sources
    sources = find_sources(analysis, config.get("brave_key", ""))

    # Step 7: Generate script
    script_text = generate_script(analysis, transcript, config)
    (project_dir / "script.txt").write_text(script_text, encoding="utf-8")

    # Step 8: Voice-over
    voiceover_path = project_dir / "voiceover.mp3"
    await generate_voiceover(script_text, voiceover_path)

    # Step 9: Assemble video (unless skipped)
    final_video = None
    if not skip_video:
        frames_dir = project_dir / "frames"
        if frames_dir.exists() and list(frames_dir.glob("*.jpg")):
            final_path = project_dir / "final.mp4"
            final_video = assemble_video(frames_dir, voiceover_path, final_path, script_text)

    # Step 10: Save report
    save_results(project_dir, analysis, script_text, sources, transcript)

    # Summary
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    log("ðŸ", f"Pipeline complete in {elapsed:.0f}s", C.BOLD)
    print()
    log("ðŸ“", f"Output: {project_dir}", C.GREEN)
    log("ðŸ“", f"Script: script.txt ({len(script_text)} chars)", C.CYAN)
    log("ðŸŽ™ï¸", f"Voice-over: voiceover.mp3", C.CYAN)
    if final_video and final_video.exists():
        log("ðŸŽ¬", f"Video: final.mp4", C.CYAN)
    log("ðŸ“„", f"Report: README.md", C.CYAN)
    log("ðŸ”", f"Sources found: {len(sources)}", C.CYAN)

    # Nanobot notification
    notify = {
        "timestamp": datetime.now().isoformat(),
        "type": "VIDEO_PIPELINE",
        "title": analysis.get("title", "Video"),
        "project_dir": str(project_dir),
        "topics": analysis.get("topics", []),
        "sources_count": len(sources),
        "has_video": final_video is not None,
    }
    notify_path = project_dir / "nanobot_notify.json"
    notify_path.write_text(json.dumps(notify, ensure_ascii=False, indent=2), encoding="utf-8")

    return project_dir


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Video Content Pipeline")
    parser.add_argument("url", nargs="?", help="Video URL (Facebook, YouTube, etc.)")
    parser.add_argument("--skip-video", action="store_true", help="Skip final video assembly")
    parser.add_argument("--allow-whisper", action="store_true", help="Allow Whisper fallback when subtitles are missing")
    parser.add_argument("--tts", type=str, help="TTS-only mode: generate voice-over from text")
    parser.add_argument("--tts-file", type=str, help="TTS from file: read text from file")
    parser.add_argument("--voice", type=str, default="lt-LT-LeonasNeural", help="TTS voice")
    parser.add_argument("--output", type=str, help="Output file path")

    args = parser.parse_args()

    if args.tts:
        asyncio.run(tts_only(args.tts, Path(args.output) if args.output else None, args.voice))
    elif args.tts_file:
        text = Path(args.tts_file).read_text(encoding="utf-8")
        asyncio.run(tts_only(text, Path(args.output) if args.output else None, args.voice))
    elif args.url:
        asyncio.run(
            run_pipeline(
                args.url,
                skip_video=args.skip_video,
                require_subtitles=not args.allow_whisper,
            )
        )
    else:
        parser.print_help()
        print("\nExamples:")
        print('  python video_pipeline.py "https://youtube.com/watch?v=..."')
        print('  python video_pipeline.py "https://facebook.com/share/r/..." --skip-video')
        print('  python video_pipeline.py --tts "Sveiki, tai informacinis praneÅ¡imas"')
        print('  python video_pipeline.py --tts-file script.txt --output voiceover.mp3')


if __name__ == "__main__":
    main()


