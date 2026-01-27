from pathlib import Path
import os
import time
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

prompt = "Giv 3 bullets om tokens."

last_exc = None
for attempt in range(3):
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=120,
        )
        break
    except Exception as exc:
        last_exc = exc
        time.sleep(0.5 * (2 ** attempt))
else:
    raise last_exc

usage = resp.usage
log_path = Path(__file__).with_name("usage.log")
log_path.write_text(
    f"prompt_tokens={usage.prompt_tokens} completion_tokens={usage.completion_tokens} total_tokens={usage.total_tokens}\n",
    encoding="utf-8",
)

print(resp.choices[0].message.content)
