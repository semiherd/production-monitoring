#!/bin/sh
set -e
echo "Running Alembic migrations (auth-service)..."
alembic upgrade head
if [ "$SEED_USERS" = "true" ]; then
  echo "Seeding default users..."
  python seed_users.py || true
fi
echo "Starting Gunicorn (auth-service)..."
exec gunicorn wsgi:app --bind 0.0.0.0:5001
