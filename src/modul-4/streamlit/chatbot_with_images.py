from pathlib import Path
import base64
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

st.title("Chatbot + billedgenerering")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Du er en hjælpsom assistent."}
    ]

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    st.chat_message(msg["role"]).write(msg["content"])

user_text = st.chat_input("Skriv en besked")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.7,
        max_tokens=200,
    )
    answer = resp.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

st.divider()
st.subheader("Generér billede")
image_prompt = st.text_input("Billedprompt")

if st.button("Lav billede") and image_prompt:
    result = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024",
        n=1,
    )
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    st.image(image_bytes, caption="Genereret billede")
