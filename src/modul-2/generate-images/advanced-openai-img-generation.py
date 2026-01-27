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

# Advanced image generation: inpainting with a mask.
# The mask should be a PNG where transparent areas are editable.
image_path = Path(__file__).with_name("input_scene.png")
mask_path = Path(__file__).with_name("input_scene_mask.png")

prompt = (
    "Replace the sky with a dramatic sunset and add soft golden light. "
    "Keep the buildings and foreground unchanged."
)
with open(image_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
    result = client.images.edit(
        model="gpt-image-1",
        image=image_file,
        mask=mask_file,
        prompt=prompt,
        size="1024x1024",
        n=1,
    )

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

output_path = Path(__file__).with_name("generated_advanced.png")
with open(output_path, "wb") as f:
    f.write(image_bytes)

print(f"Wrote {output_path.name}")
