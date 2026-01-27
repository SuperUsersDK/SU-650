import argparse
import base64
import io
import sys
from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image

def load_root_env():
    src_dir = next(p for p in Path(__file__).resolve().parents if p.name == "src")
    root_dir = src_dir.parent
    env_file = str(root_dir / ".env")
    load_dotenv(env_file)


load_root_env()






IMAGE_MODEL = "gpt-image-1"

def main():
    parser = argparse.ArgumentParser(description="Make the main object appear in focus.")
    parser.add_argument("--image", required=True, help="Path to the input image.")
    parser.add_argument("--output", default="focused.png", help="Output image name.")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")
    client = OpenAI(api_key=api_key)

    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    prompt = (
        "Make the main subject crisp and in focus. "
        "Keep everything else unchanged."
    )

    with image_path.open("rb") as image_stream:
        result = client.images.edit(
            model=IMAGE_MODEL,
            image=image_stream,
            prompt=prompt,
            size="auto",
            n=1,
        )

    output_path = Path(__file__).with_name(args.output)
    output_bytes = base64.b64decode(result.data[0].b64_json)
    output_img = Image.open(io.BytesIO(output_bytes)).convert("RGB")
    if output_img.size != (width, height):
        output_img = output_img.resize((width, height), Image.LANCZOS)
    output_img.save(output_path, format="PNG")

    print(f"Wrote {output_path.name}")

if __name__ == "__main__":
    main()
