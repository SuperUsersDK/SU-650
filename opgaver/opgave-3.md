# Opgave 3 (mellem): Udtræk output-felter

Lav et API-kald og udskriv relevante outputfelter fra svaret.

Krav:
- Brug `OPENAI_API_KEY` fra `.env`.
- Prompt: "Hvad er hovedstaden i Frankrig?".
- Udskriv:
  - `object`
  - `finish_reason`
  - `prompt_tokens`, `completion_tokens`, `total_tokens`
  - selve svarteksten
