#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

TEST_FLAG="AdwaCTF{DYNAMIC_BARATIERI_TEST_$(date +%s)}"
OUT_DIR="$(pwd)/test_output"

echo "============================================================"
echo " [1/4] Direct Python Dynamic File Generation Test"
echo "============================================================"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

FLAG="$TEST_FLAG" USER_ID="operative_test_42" OUTPUT_DIR="$OUT_DIR" OUTPUT_FILENAME="app.py" python3 src/generate.py

echo "[+] Verifying generated distribution files..."
if [ ! -s "$OUT_DIR/app.py" ] || [ ! -s "$OUT_DIR/console_notice.txt" ]; then
    echo "FAIL: Missing or empty generated files in $OUT_DIR" >&2
    exit 1
fi
echo "SUCCESS: Direct Python generator produced app.py and console_notice.txt"

echo "[+] Verifying local solve with test_client against dynamic flag..."
RECOVERED=$(python3 solve/solve.py | tail -n 1)
if [[ "$RECOVERED" =~ "$TEST_FLAG" ]]; then
    echo "SUCCESS: Solved locally: $TEST_FLAG"
else
    echo "FAIL: Expected $TEST_FLAG but got $RECOVERED" >&2
    exit 1
fi

echo
echo "============================================================"
echo " [2/4] Container Engine Verification (Podman / Docker)"
echo "============================================================"
if command -v podman >/dev/null 2>&1; then
    CONTAINER_CLI="podman"
elif command -v docker >/dev/null 2>&1; then
    CONTAINER_CLI="docker"
else
    echo "Notice: Neither podman nor docker found, skipping container test."
    rm -rf "$OUT_DIR"
    exit 0
fi

IMAGE_NAME="adwactf/baratieri-console-generator:latest"
CONTAINER_TEST_FLAG="AdwaCTF{CONTAINER_BARATIERI_VERIFIED_1896}"

echo "[+] Building container with $CONTAINER_CLI..."
$CONTAINER_CLI build -t "$IMAGE_NAME" .

echo
echo "============================================================"
echo " [3/4] Testing Generator Mode (Ephemeral Container)"
echo "============================================================"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
chmod 777 "$OUT_DIR"

$CONTAINER_CLI run --rm \
  -e FLAG="$CONTAINER_TEST_FLAG" \
  -e USER_ID="sauria_infiltrator" \
  -e OUTPUT_PATH="/output/app.py" \
  -v "$OUT_DIR:/output:Z" \
  "$IMAGE_NAME"

if [ ! -s "$OUT_DIR/app.py" ] || [ ! -s "$OUT_DIR/console_notice.txt" ]; then
    echo "FAIL: Ephemeral container failed to write output files" >&2
    exit 1
fi
echo "SUCCESS: Generator mode verified (container exited 0 promptly and generated files)"

echo
echo "============================================================"
echo " [4/4] Testing Live Web Server Mode (SSTI Exploit via HTTP)"
echo "============================================================"
LIVE_PORT=5099
LIVE_FLAG="AdwaCTF{LIVE_HTTP_SSTI_PWNED_1896}"
CID=$($CONTAINER_CLI run -d -p "${LIVE_PORT}:5001" -e FLAG="$LIVE_FLAG" "$IMAGE_NAME")

cleanup() {
    $CONTAINER_CLI rm -f "$CID" >/dev/null 2>&1 || true
    rm -rf "$OUT_DIR"
}
trap cleanup EXIT

echo "[+] Waiting for web service to become ready on port $LIVE_PORT..."
for i in {1..30}; do
    if curl -s "http://127.0.0.1:${LIVE_PORT}/" >/dev/null 2>&1; then
        echo "[+] Web service is up!"
        break
    fi
    sleep 0.5
done

echo "[+] Executing SSTI exploit against live container..."
RECOVERED_LIVE=$(python3 solve/solve.py "http://127.0.0.1:${LIVE_PORT}" | tail -n 1)
if [[ "$RECOVERED_LIVE" =~ "$LIVE_FLAG" ]]; then
    echo "SUCCESS: Live SSTI exploit verified! Flag recovered: $LIVE_FLAG"
else
    echo "FAIL: Expected $LIVE_FLAG but got $RECOVERED_LIVE" >&2
    exit 1
fi

echo
echo "============================================================"
echo " ALL 4/4 TESTS PASSED SUCCESSFULLY!"
echo "============================================================"
