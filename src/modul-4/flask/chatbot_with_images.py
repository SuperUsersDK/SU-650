from pathlib import Path
import base64
import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, render_template_string


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
app = Flask(__name__)

messages = [
    {"role": "system", "content": "Du er en hjælpsom assistent."}
]

TEMPLATE = """
<!doctype html>
<title>Chatbot + Billeder</title>
<h1>Chatbot + Billedgenerering</h1>
<form method="post">
  <input type="text" name="message" placeholder="Skriv en besked" size="60" />
  <button type="submit">Send</button>
</form>

{% if chat %}
  <h3>Chat</h3>
  <ul>
    {% for role, content in chat %}
      <li><strong>{{ role }}:</strong> {{ content }}</li>
    {% endfor %}
  </ul>
{% endif %}

<hr />
<h2>Generér billede</h2>
<form method="post">
  <input type="text" name="image_prompt" placeholder="Billedprompt" size="60" />
  <button type="submit">Lav billede</button>
</form>

{% if image_data %}
  <h3>Genereret billede</h3>
  <img src="data:image/png;base64,{{ image_data }}" width="512" />
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    if request.method == "POST":
        message = request.form.get("message", "")
        image_prompt = request.form.get("image_prompt", "")

        if message:
            messages.append({"role": "user", "content": message})
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=200,
            )
            answer = resp.choices[0].message.content
            messages.append({"role": "assistant", "content": answer})

        if image_prompt:
            result = client.images.generate(
                model="gpt-image-1",
                prompt=image_prompt,
                size="1024x1024",
                n=1,
            )
            image_data = result.data[0].b64_json

    chat = [(m["role"], m["content"]) for m in messages if m["role"] != "system"]
    return render_template_string(TEMPLATE, chat=chat, image_data=image_data)


if __name__ == "__main__":
    app.run(debug=True)
