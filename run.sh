#!/usr/bin/env bash
set -euo pipefail

cd /root/task

echo "[1/5] Installing Python dependencies..."
pip install -q -r requirements.txt

echo "[2/5] Starting PostgreSQL..."
docker compose up -d --wait

echo "[3/5] Verifying database readiness..."
for i in $(seq 1 20); do
  if docker compose exec -T postgres pg_isready -U cartnest -d cartnest_compare >/dev/null 2>&1; then
    echo "      postgres is accepting connections"
    break
  fi
  echo "      waiting for postgres ($i)..."
  sleep 2
done

echo "[4/5] Checking seeded snapshot rows..."
ROWS=$(docker compose exec -T postgres psql -U cartnest -d cartnest_compare -tAc "SELECT COUNT(*) FROM product_snapshots;")
echo "      product_snapshots rows: ${ROWS}"

echo "[5/5] Compiling package and running key-free selfcheck..."
python -m compileall -q agent
AGENT_TEST_MODE=1 python -m agent --selfcheck

echo "ready"
