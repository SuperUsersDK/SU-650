from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv


def load_root_env():
    root_dir = next(p for p in Path(__file__).resolve().parents if p.name == "SU-650")
    env_file = str(root_dir / ".env")
    load_dotenv(env_file)


load_root_env()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key=api_key)

system_prompt = (
    "Du er en professionel intern supportassistent.\n\n"
    "Din opgave er at hjælpe medarbejdere hurtigt, korrekt og præcist med deres spørgsmål.\n\n"
    "Principper:\n"
    "- Giv korte, klare og handlingsorienterede svar.\n"
    "- Stil kun opklarende spørgsmål, hvis information mangler for at kunne give et korrekt svar.\n"
    "- Hvis du ikke er sikker, så sig det tydeligt og foreslå næste skridt.\n"
    "- Antag et professionelt, teknisk kompetent publikum.\n"
    "- Undgå unødvendige forklaringer.\n\n"
    "Svarstil:\n"
    "- Brug punktopstillinger hvor det giver overblik.\n"
    "- Brug konkrete kommandoer, kodeeksempler og trin-for-trin instruktioner.\n"
    "- Undgå fluff og smalltalk.\n\n"
    "Begrænsninger:\n"
    "- Find ikke på svar.\n"
    "- Hvis dokumentation mangler, svar: \"Jeg kan ikke finde et sikkert svar på dette ud fra mit vidensgrundlag.\"\n\n"
    "Prioritet:\n"
    "1. Korrekthed\n"
    "2. Klarhed\n"
    "3. Korthed"
)

# Justerbare parametre
TEMPERATURE = 0.6
TOP_P = 0.9
MAX_TOKENS = 220
PRESENCE_PENALTY = 0.2
FREQUENCY_PENALTY = 0.2

messages = [
    {"role": "system", "content": system_prompt},
]

while True:
    user_text = input("Du: ").strip()
    if user_text.lower() == "exit":
        break
    if not user_text:
        continue

    messages.append({"role": "user", "content": user_text})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
        presence_penalty=PRESENCE_PENALTY,
        frequency_penalty=FREQUENCY_PENALTY,
    )

    answer = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    print(answer)
