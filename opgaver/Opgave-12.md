# Opgave 12 (avanceret): RAG med chunking + kildeangivelse

Byg en mere robust RAG‑pipeline, der chunker dokumenter, scorer chunks og svarer med kilder.

## Forudsætninger
- Brug `opgaver/boilerplate.py` som udgangspunkt.
- Brug samme `opgaver/rag_data/` som i opgave 11 (mindst 3 filer).

## Krav
- Del hver fil op i chunks på ca. 300–500 tegn (med overlap på 50–100 tegn).
- Lav en simpel relevance‑score pr. chunk (keyword‑overlap eller cosine‑sim på embeddings).
- Vælg **top‑3 chunks** samlet set og send dem til modellen.
- Brug modellen `gpt-4o-mini`.
- Svaret skal:
  - Være kort (max 8 linjer)
  - Indeholde 1–3 konkrete anbefalinger
  - Indeholde kildeangivelse i formatet: `Kilde: filnavn#chunkX`
- Hvis der er konflikt mellem kilder, skal modellen sige det eksplicit og foreslå næste skridt.

## Output
- Print svaret.
- Print de valgte chunks og deres score i debug‑mode (fx via en `DEBUG = True` variabel).

## Bonus (valgfri)
- Tilføj “svar‑sikkerhed”: hvis top‑score er under en tærskel, så afvis og bed om mere kontekst.
