# Text To Speech Example

This script uses the OpenAI Python SDK and reads `OPENAI_API_KEY` from the root `.env` file.

## Setup

1) Ensure the API key exists at `./.env`:

```
OPENAI_API_KEY=your_key_here
```

2) Install dependencies (if not already installed):

```
pip install openai
```

## Run

Female voice:

```
python3 text_to_speech.py --text "Hello from OpenAI" --gender female --output female.wav
```

Male voice:

```
python3 text_to_speech.py --text "Hello from OpenAI" --gender male --output male.wav
```

The output file is written in this folder.
