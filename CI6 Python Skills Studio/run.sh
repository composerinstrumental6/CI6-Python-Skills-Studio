#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

if command -v xdg-open >/dev/null 2>&1; then
  (sleep 1; xdg-open "http://127.0.0.1:5050" >/dev/null 2>&1 || true) &
elif command -v open >/dev/null 2>&1; then
  (sleep 1; open "http://127.0.0.1:5050" >/dev/null 2>&1 || true) &
fi

python app.py
