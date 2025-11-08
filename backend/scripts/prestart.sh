#!/usr/bin/env bash
set -euo pipefail

echo "Running database migrations..."
alembic upgrade head

echo "Initializing superuser..."
python -c "from app.core.init_db import main; main()"
