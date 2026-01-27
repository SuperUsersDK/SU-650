from pathlib import Path
import argparse
import base64
import json
import os
from openai import OpenAI
from dotenv import load_dotenv


def load_root_env():
    root_dir = next(p for p in Path(__file__).resolve().parents if p.name == "SU-650")
    env_file = str(root_dir / ".env")
    load_dotenv(env_file)


load_root_env()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

parser = argparse.ArgumentParser(description="Analyze image for presence of a house.")
parser.add_argument("--image", required=True, help="Path to the image file.")
args = parser.parse_args()

image_path = Path(args.image)
if not image_path.exists():
    raise FileNotFoundError(f"Image not found: {image_path}")

client = OpenAI(api_key=api_key)

image_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")

prompt = (
    "Check if the image contains a house. Return ONLY JSON with keys: "
    "has_house (boolean), confidence_percent (0-100), reason (short string)."
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            ],
        }
    ],
    response_format={"type": "json_object"},
)

text = response.choices[0].message.content
print(json.dumps(json.loads(text), ensure_ascii=False, indent=2))
