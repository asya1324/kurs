#!/bin/sh

# 1. HARDCODE THE PATH: This path is now confirmed to be correct.
export REQUESTS_CA_BUNDLE=/usr/local/lib/python3.12/site-packages/certifi/cacert.pem

# 2. Add system CAs as a fallback (optional, but robust)
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt


# ⚠️ Final Gunicorn Command: Added verbose flags and foreground execution
exec gunicorn itestoria.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 1 \
    --threads 4 \
    --log-level debug \
    --access-logfile '-' \
    --error-logfile '-'

python manage.py migrate --noinput
gunicorn itestoria.wsgi:application --bind 0.0.0.0:$PORT
