#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

echo "Opening app in your browser..."
(
  sleep 1
  open "http://127.0.0.1:5050"
) &
python app.py
