# Opgave 9 (avanceret): Professionel chatbot

Lav en professionel chatbot med en stærk system prompt, inspireret af slides 136-144.

Krav:
- Brug `OPENAI_API_KEY` fra `.env`.
- Brug `gpt-4o-mini`.
- System prompt skal være professionel og præcis (rolle, regler, stil, prioritet).
- Chatten skal køre i en loop indtil brugeren skriver `exit`.
- Bevar historik, så modellen kan huske konteksten.
- Gør følgende parametre justerbare i kaldet (via variabler i koden):
  - `temperature`
  - `top_p`
  - `max_tokens`
  - `presence_penalty`
  - `frequency_penalty`

Output:
- Print kun modellens svar pr. tur.
