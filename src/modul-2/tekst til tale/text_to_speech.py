import argparse
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






VOICE_BY_GENDER = {
    "male": "onyx",
    "female": "nova",
}

def main():
    parser = argparse.ArgumentParser(description="OpenRouter text-to-speech example.")
    parser.add_argument("--text", required=True, help="Text to synthesize.")
    parser.add_argument(
        "--gender",
        choices=sorted(VOICE_BY_GENDER.keys()),
        default="female",
        help="Selects a preset voice.",
    )
    parser.add_argument(
        "--output",
        default="speech.wav",
        help="Output WAV file name.",
    )
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")
    client = OpenAI(api_key=api_key)

    voice = VOICE_BY_GENDER[args.gender]

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=args.text,
        response_format="wav",
    )

    output_path = Path(__file__).with_name(args.output)
    with open(output_path, "wb") as f:
        f.write(response.read())

    print(f"Wrote {output_path.name}")

if __name__ == "__main__":
    main()
