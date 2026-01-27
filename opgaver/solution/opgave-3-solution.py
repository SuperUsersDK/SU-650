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

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hvad er hovedstaden i Frankrig?"}],
)

choice = resp.choices[0]
usage = resp.usage

print("object:", resp.object)
print("finish_reason:", choice.finish_reason)
print("prompt_tokens:", usage.prompt_tokens)
print("completion_tokens:", usage.completion_tokens)
print("total_tokens:", usage.total_tokens)
print("answer:", choice.message.content)
