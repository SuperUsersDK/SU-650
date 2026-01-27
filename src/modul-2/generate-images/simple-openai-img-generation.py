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






api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")
client = OpenAI(api_key=api_key)

prompt = "A bright watercolor landscape with rolling hills and a small cottage"
try:
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="high",
        n=1,
    )
except Exception as exc:
    if "gpt-image-1" in str(exc) or "verify" in str(exc).lower():
        result = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            response_format="b64_json",
            n=1,
        )
    else:
        raise

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

output_path = Path(__file__).with_name("generated_simple.png")
with open(output_path, "wb") as f:
    f.write(image_bytes)

print(f"Wrote {output_path.name}")
