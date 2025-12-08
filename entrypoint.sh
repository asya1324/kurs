#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Apply migrations
echo "Applying database migrations (SQLite for Sessions/Auth)..."
python manage.py migrate --no-input

# Debugging: Show what command is being attempted
echo "Starting application..."
echo "Received command args: '$@'"

# Determine the port: Use the PORT env var if set (Render), otherwise 8000 (Local)
PORT="${PORT:-8000}"

# If no command is provided (CMD is empty), run Gunicorn
if [ -z "$1" ]; then
    echo "No command provided. Defaulting to Gunicorn on port $PORT..."
    exec gunicorn itestoria.wsgi:application --bind "0.0.0.0:$PORT"
else
    echo "Executing received command: $@"
    exec "$@"
fi