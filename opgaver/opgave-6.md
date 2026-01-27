# Opgave 6 (avanceret): Chatbot i terminalen

Lav en simpel chatbot i terminalen, hvor brugeren kan skrive flere spørgsmål i træk.

Krav:
- Brug `OPENAI_API_KEY` fra `.env`.
- Brug `gpt-4o-mini`.
- Systemrolle: "Du er en hjælpsom kursusassistent.".
- Chatten skal køre i en løkke indtil brugeren skriver `exit`.
- Bevar historik, så modellen kan huske konteksten.
- Print kun modellens svar pr. tur.
