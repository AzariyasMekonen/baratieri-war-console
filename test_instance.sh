#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "============================================================"
echo " [1/3] Direct Python Flask Local Verification"
echo "============================================================"
TEST_FLAG_LOCAL="AdwaCTF{LOCAL_SOLVE_VERIFIED_$(date +%s)}"
echo "$TEST_FLAG_LOCAL" > flag.txt
RECOVERED_LOCAL=$(python3 solve/solve.py | tail -n 1)
if [[ "$RECOVERED_LOCAL" =~ "$TEST_FLAG_LOCAL" ]]; then
    echo "SUCCESS: Local Flask test_client solve verified: $TEST_FLAG_LOCAL"
else
    echo "FAIL: Expected $TEST_FLAG_LOCAL but got $RECOVERED_LOCAL" >&2
    exit 1
fi

echo
echo "============================================================"
echo " [2/3] Building Docker Instance Image"
echo "============================================================"
if command -v podman >/dev/null 2>&1; then
    CONTAINER_CLI="podman"
elif command -v docker >/dev/null 2>&1; then
    CONTAINER_CLI="docker"
else
    echo "Notice: Neither podman nor docker found, skipping container test."
    exit 0
fi

IMAGE_NAME="adwactf/baratieri-console:latest"
echo "[+] Building image with $CONTAINER_CLI..."
$CONTAINER_CLI build -t "$IMAGE_NAME" .
echo "SUCCESS: Docker image built successfully"

echo
echo "============================================================"
echo " [3/3] Testing Live Docker Instance Deployment & SSTI Exploit"
echo "============================================================"
HOST_PORT=5099
INSTANCE_FLAG="AdwaCTF{DOCKER_INSTANCE_SSTI_PWNED_1896}"

CID=$($CONTAINER_CLI run -d -p "${HOST_PORT}:5001" -e FLAG="$INSTANCE_FLAG" "$IMAGE_NAME")

cleanup() {
    echo "[+] Cleaning up container instance $CID..."
    $CONTAINER_CLI rm -f "$CID" >/dev/null 2>&1 || true
    rm -f flag.txt
}
trap cleanup EXIT

echo "[+] Waiting for container instance to accept connections on port $HOST_PORT..."
for i in {1..30}; do
    if curl -s "http://127.0.0.1:${HOST_PORT}/" >/dev/null 2>&1; then
        echo "[+] Container instance is UP and healthy!"
        break
    fi
    sleep 0.5
done

echo "[+] Launching automated SSTI exploit against http://127.0.0.1:${HOST_PORT}..."
RECOVERED_INSTANCE=$(python3 solve/solve.py "http://127.0.0.1:${HOST_PORT}" | tail -n 1)
if [[ "$RECOVERED_INSTANCE" =~ "$INSTANCE_FLAG" ]]; then
    echo "SUCCESS: Docker instance SSTI exploit verified! Flag: $INSTANCE_FLAG"
else
    echo "FAIL: Expected $INSTANCE_FLAG but got $RECOVERED_INSTANCE" >&2
    exit 1
fi

echo
echo "============================================================"
echo " ALL TESTS PASSED: DOCKER INSTANCE CHALLENGE VERIFIED!"
echo "============================================================"
