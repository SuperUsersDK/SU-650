# Opgave 8 (billedanalyse): Find et hus

Analyser et billede og afgør om der er et hus på billedet.

Krav:
- Hent selv et billede fra nettet og gem det lokalt.
- Brug `OPENAI_API_KEY` fra `.env`.
- Brug en multimodal model (fx `gpt-4o-mini`).
- Returner kun JSON med felterne:
  - `has_house` (boolean)
  - `confidence_percent` (0-100)
  - `reason` (kort forklaring)
- Print JSON til terminalen.
