#!/usr/bin/env bash
set -e

# Always plant dynamic flag and generate distribution files first
python3 /app/src/generate.py

# If running explicitly in generator mode (invoked by file generator driver via OUTPUT_PATH or arg)
if [ -n "${OUTPUT_PATH:-}" ] || [ "${1:-}" = "generate" ] || [ "${MODE:-}" = "generator" ]; then
    echo "[+] Generated files for challenge distribution. Exiting generator mode."
    exit 0
fi

# Otherwise start the live web service
echo "[+] Starting Baratieri War Council Console on port ${PORT:-5001}..."
exec python3 /app/src/app.py
