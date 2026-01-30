from pathlib import Path
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

DEBUG = True
TOP_K = 3
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
MIN_SCORE_THRESHOLD = 1


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


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def score_chunk(query_words: set[str], chunk_text: str) -> int:
    chunk_words = set(tokenize(chunk_text))
    return len(query_words & chunk_words)


def load_chunks(data_dir: Path) -> list[dict]:
    all_chunks = []
    for path in sorted(data_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        for idx, chunk in enumerate(chunks, start=1):
            all_chunks.append(
                {
                    "filename": path.name,
                    "chunk_id": idx,
                    "text": chunk,
                }
            )
    return all_chunks


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
    chunks = load_chunks(data_dir)

    for ch in chunks:
        ch["score"] = score_chunk(query_words, ch["text"])

    chunks.sort(key=lambda c: c["score"], reverse=True)
    top_chunks = chunks[:TOP_K]
    

    if not top_chunks or top_chunks[0]["score"] < MIN_SCORE_THRESHOLD:
        print("Jeg har ikke grundlag nok i de givne dokumenter.")
        return

    if DEBUG:
        print("DEBUG: valgte chunks")
        for ch in top_chunks:
            print(
                f"- {ch['filename']}#chunk{ch['chunk_id']} "
                f"(score={ch['score']})"
            )
        print()

    context_blocks = []
    for ch in top_chunks:
        label = f"{ch['filename']}#chunk{ch['chunk_id']}"
        context_blocks.append(f"[{label}]\n{ch['text']}")

    context_text = "\n\n".join(context_blocks)

    prompt = (
        "Du er en hjælpsom intern assistent. Svar kun ud fra konteksten.\n"
        "Svar kort (maks 8 linjer) og giv 1-3 konkrete anbefalinger.\n"
        "Hvis kilder er i konflikt, sig det eksplicit og foreslå næste skridt.\n"
        "Afslut med kildeangivelse i formatet: Kilde: filnavn#chunkX\n\n"
        f"Kontekst:\n{context_text}\n\n"
        f"Spørgsmål: {query}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    print(response.choices[0].message.content.strip())


if __name__ == "__main__":
    main()