from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv


def load_root_env():
    src_dir = next(p for p in Path(__file__).resolve().parents if p.name == "SU-650")
    env_file = str(src_dir / ".env")
    load_dotenv(env_file)


load_root_env()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key=api_key)

messages = [
    {"role": "system", "content": "Du er en kort og præcis underviser."},
    {"role": "user", "content": "Forklar kort hvad et API er."},
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.7,
    max_tokens=120,
)

print(response.choices[0].message.content)
