# Opgave 4 (mellem-svær): Samme prompt på flere leverandører

Kør samme prompt mod tre leverandører (OpenAI, Hugging Face, OpenRouter).

Krav:
- Brug API-nøgler fra `.env`:
  - `OPENAI_API_KEY`
  - `HUGGINGFACE_API_KEY`
  - `OPENROUTER_API_KEY`
- Brug samme prompt og print svarene med tydelige labels.
- Brug modeller:
  - OpenAI: `gpt-4o-mini`
  - Hugging Face: `meta-llama/Llama-3.1-8B-Instruct`
  - OpenRouter: `openai/gpt-4o-mini`
