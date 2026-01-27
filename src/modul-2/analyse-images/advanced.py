import base64
import json
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

# Advanced image analysis: structured extraction as JSON.
# Replace with a local file path if needed.
image_path = Path(__file__).with_name("receipt.jpg")

with open(image_path, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Extract key fields from the receipt and return JSON only. "
                        "If a field is missing, return null. Use this schema:\n"
                        "{\n"
                        "  \"merchant_name\": string|null,\n"
                        "  \"date\": string|null,\n"
                        "  \"currency\": string|null,\n"
                        "  \"total\": number|null,\n"
                        "  \"line_items\": [{\"description\": string, \"amount\": number}]\n"
                        "}\n"
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                },
            ],
        }
    ],
    response_format={"type": "json_object"},
)

result_text = response.choices[0].message.content
output_path = Path(__file__).with_name("advanced-result.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(json.loads(result_text), f, ensure_ascii=False, indent=2)

print(result_text)
print(f"Wrote {output_path.name}")
