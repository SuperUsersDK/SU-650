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

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Skriv en kort beskrivelse af Paris."}
    ],
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.2,
    presence_penalty=0.2,
    max_tokens=120,
    seed=42,
)

print(response.choices[0].message.content)
