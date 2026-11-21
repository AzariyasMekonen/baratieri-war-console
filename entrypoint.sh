#!/usr/bin/env bash
set -e

FLAG_VAL="${CHALLENGE_FLAG:-${FLAG:-${ADWA_FLAG:-AdwaCTF{5571_b4r4713r1_0rd3r5_d15rup73d}}}}"

# Ensure flag is planted in standard server-side paths accessible by command execution
echo "$FLAG_VAL" > /app/flag.txt 2>/dev/null || true
echo "$FLAG_VAL" > /flag.txt 2>/dev/null || true
echo "$FLAG_VAL" > /app/src/flag.txt 2>/dev/null || true

PORT_VAL="${PORT:-5001}"
echo "[+] Starting Baratieri War Council Console on port ${PORT_VAL}..."
exec python3 /app/src/app.py
