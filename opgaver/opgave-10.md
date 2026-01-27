# Opgave 10 (afsluttende, 30–60 min): LLM-brug i praksis

## Formål
Du skal demonstrere, at du kan bruge LLM’er korrekt og ansvarligt – med gode prompts, styring af output, og håndtering af usikkerhed.

## Scenarie
Du er rådgiver for en lille virksomhed, der vil indføre en intern AI-assistent til medarbejdere. Assistenten skal:
- Besvare spørgsmål om interne processer.
- Skrive korte, handlingsorienterede svar.
- Være bevidst om begrænsninger og aldrig finde på svar.

Du må ikke kode i denne opgave. Fokus er på korrekt brug af LLM’er.

## Leverancer
Lav et dokument (1–2 sider), der indeholder:

### 1) System prompt (professionel)
Skriv en stærk system prompt, der:
- Definerer rolle og ansvar.
- Indeholder regler (korrekthed, korthed, ingen hallucination).
- Har tydelig svarstil (bullet points, konkrete trin, mv.).

### 2) Promptstrategi
Beskriv din promptstrategi i 5–7 punkter:
- Hvordan du styrer tone og format.
- Hvordan du håndterer uklarheder (opklarende spørgsmål).
- Hvordan du styrer risiko (bias, hallucinationer, datalæk).

### 3) 3 testcases med forventet output
Lav tre konkrete spørgsmål, som medarbejdere kan stille, fx:
- IT-support
- HR/personalepolitik
- Projektprocesser

For hver testcase skal du:
- Skrive det præcise user prompt.
- Beskrive det forventede output-format (ikke selve svaret).

### 4) Fejlhåndtering
Beskriv hvordan du vil håndtere:
- Manglende data
- Modstridende information
- Usikkerhed i svar
- Timeout og netværksproblemer

## Ekstra udfordring (valgfri)
Design en kort evalueringsliste (5–7 kriterier), som en kollega kan bruge til at vurdere, om chatbotten svarer korrekt og professionelt.

## Python template (valgfri)
Der ligger en template i `opgaver/opgave-10-template.py`, som kan bruges til at implementere chatbotten i praksis.

---
**Aflevering:** Gem dokumentet som `opgave-10-besvarelse.md`.
