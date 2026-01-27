from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv


def load_root_env():
    src_dir = next(p for p in Path(__file__).resolve().parents if p.name == "SU-650")
    env_file = str(src_dir / ".env")
    load_dotenv(env_file)


load_root_env()

prompt = "Hvad er hovedstaden i Frankrig?"

openai_key = os.getenv("OPENAI_API_KEY")
hf_key = os.getenv("HUGGINGFACE_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

if not openai_key or not hf_key or not openrouter_key:
    raise RuntimeError("Missing one or more API keys in .env")

clients = [
    ("OpenAI", OpenAI(api_key=openai_key), "gpt-4o-mini"),
    ("HuggingFace", OpenAI(api_key=hf_key, base_url="https://router.huggingface.co/v1"), "meta-llama/Llama-3.1-8B-Instruct"),
    ("OpenRouter", OpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1"), "openai/gpt-4o-mini"),
]

for label, client, model in clients:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    print(f"{label}: {resp.choices[0].message.content}")
