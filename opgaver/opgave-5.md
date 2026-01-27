# Opgave 5 (svær): Retry + usage log

Lav et API-kald med retry og log usage til en fil.

Krav:
- Brug `OPENAI_API_KEY` fra `.env`.
- Prompt: "Giv 3 bullets om tokens.".
- Implementer retry (3 forsøg, exponential backoff).
- Log `prompt_tokens`, `completion_tokens`, `total_tokens` til `opgaver/solution/usage.log`.
- Print svaret til sidst.
