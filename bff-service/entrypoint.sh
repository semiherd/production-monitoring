#!/bin/sh
set -e
CERT_DIR="${CERT_DIR:-/certs}"
CERT_FILE="${CERT_FILE:-$CERT_DIR/server.crt}"
KEY_FILE="${KEY_FILE:-$CERT_DIR/server.key}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8443}"
mkdir -p "$CERT_DIR"
if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
  echo "Generating self-signed certificate..."
  openssl req -x509 -nodes -days 365 -newkey rsa:2048     -keyout "$KEY_FILE" -out "$CERT_FILE" -subj "/CN=localhost"
fi
exec gunicorn wsgi:app --bind $HOST:$PORT --certfile "$CERT_FILE" --keyfile "$KEY_FILE"
