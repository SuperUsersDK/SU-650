from pathlib import Path
import os
import re
from openai import OpenAI
from dotenv import load_dotenv


def load_root_env():
    src_dir = next(
        p for p in Path(__file__).resolve().parents if p.name == "SU-650"
    )
    env_file = str(src_dir / ".env")
    load_dotenv(env_file)


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9æøåÆØÅ]+", text.lower())
    stopwords = {
        "og",
        "i",
        "på",
        "at",
        "en",
        "et",
        "de",
        "det",
        "der",
        "som",
        "til",
        "for",
        "med",
        "af",
        "er",
        "har",
        "vi",
        "du",
        "den",
        "fra",
        "kan",
        "skal",
    }
    return [w for w in words if w not in stopwords]


def score_document(query_words: set[str], doc_text: str) -> int:
    doc_words = set(tokenize(doc_text))
    return len(query_words & doc_words)


def load_documents(data_dir: Path) -> list[tuple[str, str]]:
    docs = []
    for path in sorted(data_dir.glob("*.txt")):
        docs.append((path.name, path.read_text(encoding="utf-8")))
    return docs


def main() -> None:
    load_root_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")

    client = OpenAI(api_key=api_key)

    data_dir = Path(__file__).resolve().parents[1] / "rag_data"
    if not data_dir.exists():
        raise RuntimeError("Missing opgaver/rag_data with .txt files")

    query = input("Spørgsmål: ").strip()
    if not query:
        print("Ingen spørgsmål angivet.")
        return

    query_words = set(tokenize(query))
    docs = load_documents(data_dir)

    best = None
    best_score = -1
    for filename, text in docs:
        s = score_document(query_words, text)
        if s > best_score:
            best_score = s
            best = (filename, text)

    if not best or best_score <= 0:
        print("Jeg har ikke grundlag nok i de givne dokumenter.")
        return

    filename, context = best

    prompt = (
        "Du er en hjælpsom intern assistent. Svar kun ud fra konteksten.\n"
        "Svar kort og handlingsorienteret (maks 6 linjer).\n\n"
        f"Kontekst fra {filename}:\n{context}\n\n"
        f"Spørgsmål: {query}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    print(response.choices[0].message.content.strip())
    print(f"\nValgt fil: {filename}")


if __name__ == "__main__":
    main()