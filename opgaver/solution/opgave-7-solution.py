from pathlib import Path
import base64
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

client = OpenAI(api_key=api_key)

result = client.images.generate(
    model="gpt-image-1",
    prompt="Et lille rødt hus ved en sø i solnedgang, enkel stil",
    size="1024x1024",
    quality="high",
    n=1,
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

output_path = Path(__file__).parent / "generated_house.png"
output_path.write_bytes(image_bytes)

print(f"Wrote {output_path.name}")
