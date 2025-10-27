#!/bin/sh
set -e
if [ -n "$REDIS_PASSWORD" ]; then
  redis-server --port 6379 --bind 0.0.0.0 --appendonly yes --dir /data --requirepass "$REDIS_PASSWORD" &
else
  redis-server --port 6379 --bind 0.0.0.0 --appendonly yes --dir /data &
fi
sleep 2
exec gunicorn app:app --bind 0.0.0.0:5003
