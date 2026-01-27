<<<<<<< HEAD
# AGENTS

## Project overview
- Educational content for a Generative AI / LLM course (see `README.md`).
- Supporting materials include slides (`SU-650.pptx`) and setup notes (`setup.md`).
- Python dependencies are listed in `requirements.txt`.

## Project structure & module organization
- `src/` hosts the course material and code samples, grouped by provider (`openai`, `openrouter`, `huggingface`) and by `examples/` or `exercises/` modules.
- `src/demo/` contains small demo scripts tied to the module flow.
- Image/audio assets and sample outputs live alongside the scripts (e.g., `src/openai/examples/analyse-images/`).
- Root files include course collateral (`SU-650.pptx`) and setup notes (`setup.md`).

## Working conventions
- Always use `python3` for Python commands (never `python`).
- Keep changes small and focused; this repo is mostly content.

## Setup (quick)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Build, test, and development commands
- `python3 src/openai/examples/analyse-images/simple.py` runs a single example script (swap paths under `src/` as needed).
- `streamlit run src/openai/exercises/final/final_streamlit_student.py` launches the Streamlit final exercise.

## Coding style & naming conventions
- Use 4-space indentation for Python, with snake_case for files and functions.
- Keep example scripts small and focused; prefer descriptive filenames like `simple.py` and `advanced.py` in each example folder.
- Environment variables are read from a root `.env` file using `python-dotenv`.

## Testing guidelines
- There is no dedicated test suite yet. If adding tests, place them near the module they cover (e.g., `src/openai/exercises/module3_api_integration/tests/`) and document how to run them.

## Commit & pull request guidelines
- Commit messages in this repo are short, imperative, and sentence-case (e.g., "Move sources under src and consolidate env helpers").
- For PRs, include a brief description of the module(s) touched, note any new dependencies, and link to the relevant lesson or slide if applicable.

## Configuration & secrets
- Add API keys in `.env` if needed:
  - `OPENAI_API_KEY`
  - `OPENROUTER_API_KEY`
- Do not commit API keys or generated media outputs unless they are intentional course artifacts.
=======
# AGENTS

## Project overview
- Educational content for a Generative AI / LLM course (see `README.md`).
- Supporting materials include slides (`SU-650.pptx`) and setup notes (`setup.md`).
- Python dependencies are listed in `requirements.txt`.

## Working conventions
- Always use `python3` for Python commands (never `python`).
- Keep changes small and focused; this repo is mostly content.

## Setup (quick)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment
- Add API keys in `.env` if needed:
  - `OPENAI_API_KEY`
  - `OPENROUTER_API_KEY`

## Notes
- There is no application entrypoint in `src/` at the moment.
- If you add code examples, keep them in their own folder and document how to run them.
>>>>>>> 6efae9e (Fix scripts and run artifacts)
