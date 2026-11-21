#!/usr/bin/env bash
# Request a Fly.io Postgres backup. This script does not schedule backups.
# Usage: ./scripts/backup.sh [postgres-app-name]
# Verify completion in the Fly.io dashboard after the command returns.

set -Eeuo pipefail

DB_APP="${1:-${HERMES_DB_APP:-hermes-db}}"

if ! command -v fly >/dev/null 2>&1; then
  echo "Error: Fly CLI (fly) is not installed or not on PATH." >&2
  exit 127
fi

echo "Requesting Postgres backup for Fly app: ${DB_APP}"
fly postgres backup create --app "${DB_APP}"
echo "Fly CLI accepted the backup request."
echo "Important: verify that the backup completed successfully in the Fly.io dashboard."
