#!/usr/bin/env bash
set -euo pipefail

cd /root/task 2>/dev/null || true

echo "Stopping docker-compose services..."
docker compose down || true

echo "Removing task volumes..."
docker volume rm cartnest-stale-snapshot-compare-agent_cartnest_pg_data || true
docker volume rm task_cartnest_pg_data || true

echo "Removing task networks..."
docker network rm cartnest-stale-snapshot-compare-agent_default || true
docker network rm task_default || true

echo "No custom task image is built for this task; nothing to remove."

echo "Pruning leftover Docker artifacts..."
docker system prune -a --volumes -f || true

echo "Removing task directory..."
rm -rf /root/task || true

echo "Cleanup completed successfully!"
