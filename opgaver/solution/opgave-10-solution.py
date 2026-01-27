from pathlib import Path
import os
import time
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

SYSTEM_PROMPT = (
    "Du er en professionel intern supportassistent for medarbejdere.\n\n"
    "Opgave:\n"
    "Hjælp medarbejdere hurtigt, korrekt og præcist med spørgsmål om interne processer, IT og HR.\n\n"
    "Principper:\n"
    "- Giv korte, klare og handlingsorienterede svar.\n"
    "- Stil kun opklarende spørgsmål, hvis du mangler kritisk information.\n"
    "- Hvis du ikke er sikker, sig det tydeligt og foreslå næste skridt.\n"
    "- Antag et teknisk kompetent publikum.\n"
    "- Undgå unødvendige forklaringer og smalltalk.\n\n"
    "Svarstil:\n"
    "- Brug punktopstillinger når det giver overblik.\n"
    "- Brug konkrete trin, kommandoer og eksempler.\n"
    "- Hold svaret under 10 linjer, medmindre brugeren beder om detaljer.\n\n"
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
    {"role": "system", "content": SYSTEM_PROMPT},
]

while True:
    user_text = input("Du: ").strip()
    if user_text.lower() == "exit":
        break
    if not user_text:
        continue

    messages.append({"role": "user", "content": user_text})

    last_exc = None
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=MAX_TOKENS,
                presence_penalty=PRESENCE_PENALTY,
                frequency_penalty=FREQUENCY_PENALTY,
                timeout=30,
            )
            break
        except Exception as exc:
            last_exc = exc
            time.sleep(0.5 * (2 ** attempt))
    else:
        raise last_exc

    answer = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    print(answer)
