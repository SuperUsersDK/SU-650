# Opgave 11 (simpel): Mini‑RAG med keyword‑match

Lav en minimal RAG‑løsning, der henter svar fra lokale tekstfiler og kun svarer ud fra dem.

## Forudsætninger
- Brug `opgaver/boilerplate.py` som udgangspunkt.
- Opret mappen `opgaver/rag_data/` og læg 3 små tekstfiler i den (fx `it.txt`, `hr.txt`, `proces.txt`).

## Krav
- Læs alle `.txt`‑filer i `opgaver/rag_data/`.
- Vælg den **bedst matchende** fil ved simpel keyword‑score (fx antal overlappende ord).
- Send kun den valgte tekst som kontekst til modellen (inden for én prompt).
- Brug modellen `gpt-4o-mini`.
- Svaret skal være **kort og handlingsorienteret** (maks 6 linjer).
- Hvis intet matcher: returnér “Jeg har ikke grundlag nok i de givne dokumenter.”

## Output
- Print svaret til terminalen.
- Print også hvilken fil der blev valgt (filename).

## Bonus (valgfri)
- Fjern almindelige stopord (fx “og”, “i”, “på”, “at”) i keyword‑match.
