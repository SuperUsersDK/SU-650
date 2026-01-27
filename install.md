# Install (Windows 11)

## 1) Install Python 3 and pip

1. Download the latest Python 3 installer from:
   https://www.python.org/downloads/windows/
2. Run the installer and **check**: "Add python.exe to PATH".
3. Finish the installation.

## 2) Verify installation

Open PowerShell and run:

```
python --version
pip --version
```

If `python` is not found, use the Python launcher instead:

```
py -3 --version
py -3 -m pip --version
```

## 3) Install project dependencies

From the project root, run:

```
pip install -r requirements.txt
```

If you are using the Python launcher:

```
py -3 -m pip install -r requirements.txt
```

## 4) Required Python packages

These are listed in `requirements.txt`:
- openai>=1.51.0
- pillow>=10.0.0
- python-dotenv>=1.0.1
- streamlit>=1.33.0
