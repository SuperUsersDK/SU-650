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






api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    raise RuntimeError("Missing HUGGINGFACE_API_KEY in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://router.huggingface.co/v1",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "user", "content": "Hvad er hovedstaden i Frankrig?"}
    ]
)

print(response.choices[0].message.content)
