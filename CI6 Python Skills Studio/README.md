# CI6 Python Skills Studio

A beginner-friendly Python web app distributed as a GitHub Release ZIP.

## What this app does
- Text Analyzer
- Cipher Generator (Caesar, Morse, Atbash, ROT13, Vigenere)
- Currency Converter
- Fuel Consumption Converter
- Date Distance Counter
- Scientific Prefix Converter

## End-user install (ZIP download)
1. Open the repo on GitHub.
2. Go to `Releases`.
3. Download the ZIP asset.
4. Unzip it (for example in `Downloads`).

### macOS
1. Open the unzipped folder.
2. Double-click `start_app.command`.
3. Open `http://127.0.0.1:5050` if browser does not open automatically.

If macOS blocks it: right-click `start_app.command` -> Open.

### Windows
1. Open the unzipped folder.
2. Double-click `start_app.bat`.
3. Open `http://127.0.0.1:5050` if browser does not open automatically.

### Linux
1. Open terminal in the unzipped folder.
2. Run:
```bash
chmod +x run.sh
./run.sh
```
3. Open `http://127.0.0.1:5050` if browser does not open automatically.

## Create a GitHub Release ZIP (maintainer steps)
1. Push your latest code to GitHub.
2. In GitHub repo, click `Releases` -> `Draft a new release`.
3. Tag version (example: `v1.0.0`).
4. Title it (example: `CI6 Python Skills Studio v1.0.0`).
5. Attach a ZIP file of the project folder.
6. Click `Publish release`.

## Local run from terminal (all OS)
```bash
cd "<project-folder>"
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
