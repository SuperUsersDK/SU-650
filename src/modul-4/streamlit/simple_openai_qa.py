from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st


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

st.title("Simpel Q/A (OpenAI)")
question = st.text_input("Stil et spørgsmål")

if st.button("Svar") and question:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        temperature=0.7,
        max_tokens=200,
    )
    st.write(resp.choices[0].message.content)
