# Transcribe Example

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

## Input

Place a WAV file named `speech.wav` in this folder (or update the script to point to your file).

## Run

```
python3 transcribe.py
```

The transcript is saved to `transcribe.txt` in this folder.
