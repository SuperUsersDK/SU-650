from pathlib import Path
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

TEMPLATE = """
<!doctype html>
<title>Simpel Q/A</title>
<h1>Simpel Q/A (OpenAI)</h1>
<form method="post">
  <input type="text" name="question" placeholder="Stil et spørgsmål" size="60" />
  <button type="submit">Svar</button>
</form>
{% if answer %}
  <h3>Svar:</h3>
  <p>{{ answer }}</p>
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": question}],
                temperature=0.7,
                max_tokens=200,
            )
            answer = resp.choices[0].message.content
    return render_template_string(TEMPLATE, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
