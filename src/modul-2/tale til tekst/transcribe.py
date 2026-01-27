import sys
from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv

def load_root_env():
    src_dir = next(p for p in Path(__file__).resolve().parents if p.name == "src")
    root_dir = src_dir.parent
    env_file = str(root_dir / ".env")
    load_dotenv(env_file)


load_root_env()






api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")
client = OpenAI(api_key=api_key)

audio_path = Path(__file__).with_name("speech.wav")

with open(audio_path, "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
    )

output_path = Path(__file__).with_name("transcribe.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(transcript.text)

print(transcript.text)
print(f"Wrote {output_path.name}")
