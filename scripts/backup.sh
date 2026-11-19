#!/usr/bin/env bash
# Simple Postgres backup helper for Fly.io
# Usage: ./scripts/backup.sh

set -euo pipefail

APP="${1:-hermes-backend}"
STAMP=$(date +%Y%m%d-%H%M%S)
OUT="hermes-backup-${STAMP}.sql"

echo "Creating backup via fly postgres..."
fly postgres backup create --app hermes-db || true
echo "Backup requested. Check Fly.io dashboard for download link."
echo "For manual dump:"
echo "  fly ssh console -a $APP -C 'pg_dump \$DATABASE_URL' > $OUT"
echo "Done."
