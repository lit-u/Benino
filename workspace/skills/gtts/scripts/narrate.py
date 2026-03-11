#!/usr/bin/env python3
"""gTTS narration script - converts Lithuanian text to MP3"""
import argparse
import sys

def narrate(text, output_file):
    try:
        from gtts import gTTS
    except ImportError:
        print("Instaliuoju gTTS...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "gTTS", "-q"])
        from gtts import gTTS

    tts = gTTS(text=text, lang='lt')
    tts.save(output_file)
    print(f"✅ Audio išsaugotas: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="Tekstas įgarsinimui")
    parser.add_argument("--file", help="Tekstinis failas (.txt)")
    parser.add_argument("--out", default="output.mp3", help="Išvesties failas")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Klaida: nurodyk --text arba --file")
        sys.exit(1)

    narrate(text, args.out)
