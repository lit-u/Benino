"""Test YouTube tools integration."""

import asyncio
import json
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nanobot.agent.tools.youtube import YouTubeInfoTool, YouTubeSubtitlesTool, YouTubeTranscriptTool


async def test_youtube_info():
    """Test YouTube info extraction."""
    print("=" * 60)
    print("TEST 1: YouTube Video Info")
    print("=" * 60)

    tool = YouTubeInfoTool()

    # Test with a short video (example: a famous tech talk)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up (has subtitles)

    result = await tool.execute(test_url)
    data = json.loads(result)

    print(f"\n+ Title: {data.get('title')}")
    print(f"+ Channel: {data.get('channel')}")
    print(f"+ Duration: {data.get('duration_formatted')}")
    print(f"+ Views: {data.get('view_count'):,}")
    print(f"+ Has Subtitles: {data.get('has_subtitles')}")
    print(f"+ Has Auto Captions: {data.get('has_auto_captions')}")
    print(f"+ Available Languages: {', '.join(data.get('available_subtitle_languages', [])[:5])}")

    return data


async def test_youtube_subtitles():
    """Test subtitle extraction."""
    print("\n" + "=" * 60)
    print("TEST 2: YouTube Subtitles")
    print("=" * 60)

    tool = YouTubeSubtitlesTool()

    # Test URL (same as above)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    result = await tool.execute(test_url, lang="en", auto=True, max_chars=1000)
    data = json.loads(result)

    if "error" in data:
        print(f"\n- Error: {data['error']}")
        return None

    print(f"\n+ Title: {data.get('title')}")
    print(f"+ Language: {data.get('language')}")
    print(f"+ Transcript Length: {data.get('transcript_length')} chars")
    print(f"+ Truncated: {data.get('truncated')}")
    print(f"\n--- First 500 chars of transcript ---")

    # Handle Windows console encoding
    transcript_preview = data.get('transcript', '')[:500]
    try:
        print(transcript_preview)
    except UnicodeEncodeError:
        print(transcript_preview.encode('ascii', errors='replace').decode('ascii'))
    print("...\n")

    return data


async def test_youtube_transcript():
    """Test combined info + transcript."""
    print("\n" + "=" * 60)
    print("TEST 3: YouTube Full Transcript (Info + Subs)")
    print("=" * 60)

    tool = YouTubeTranscriptTool()

    # Test URL
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    result = await tool.execute(test_url, lang="en", auto=True)
    data = json.loads(result)

    if "error" in data:
        print(f"\n- Error: {data['error']}")
        return None

    video_info = data.get('video_info', {})
    transcript_data = data.get('transcript', {})

    print(f"\n+ Video: {video_info.get('title')}")
    print(f"+ Duration: {video_info.get('duration_formatted')}")
    print(f"+ Transcript Length: {transcript_data.get('transcript_length')} chars")

    return data


async def main():
    """Run all tests."""
    print("\nTesting YouTube Tools Integration\n")

    try:
        # Test 1: Video Info
        await test_youtube_info()

        # Test 2: Subtitles
        await test_youtube_subtitles()

        # Test 3: Full Transcript
        await test_youtube_transcript()

        print("\n" + "=" * 60)
        print("[OK] All tests completed!")
        print("=" * 60)
        print("\nYouTube tools are ready to use with Nanobot!")
        print("\nExample agent commands:")
        print("  - 'Get info about this YouTube video: https://...'")
        print("  - 'Download subtitles from this video in Lithuanian'")
        print("  - 'Summarize this YouTube video: https://...'")

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
