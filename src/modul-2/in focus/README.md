# In-Focus Example

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

```
python3 in_focus.py --image path/to/photo.jpg
```

## Output

The script prints JSON with:
- `main_object`: the primary subject in the photo
- `in_focus`: `true`/`false` for sharpness
- `confidence_percent`: 0-100 confidence score
