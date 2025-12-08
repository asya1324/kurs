#!/bin/bash
set -e

# 1. Collect static files (CSS/Images)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 2. Apply Django migrations 
# (This is ONLY for the SQLite database that handles Sessions/Admin login)
# (It does NOT touch your MongoDB data)
echo "Applying internal SQLite migrations..."
python manage.py migrate --noinput

# 3. Start Gunicorn server
# We use exec to let Gunicorn take over the PID 1 for proper signal handling
echo "Starting Gunicorn..."
exec gunicorn itestoria.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 3 \
  --timeout 120