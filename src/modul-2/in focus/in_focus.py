import argparse
import base64
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






MODEL = "gpt-4o-mini"

def main():
    parser = argparse.ArgumentParser(description="Detect main object focus in a photo.")
    parser.add_argument("--image", required=True, help="Path to the image file.")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")
    client = OpenAI(api_key=api_key)

    image_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")

    prompt = (
        "Identify the single main object in the photo and decide whether that "
        "object is in focus (sharp) or out of focus (blurred). "
        "Return JSON only with: main_object (string), in_focus (boolean), "
        "confidence_percent (number 0-100)."
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                    },
                ],
            }
        ],
        response_format={"type": "json_object"},
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
