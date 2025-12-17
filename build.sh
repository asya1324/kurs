#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "NUKE: Removing conflicting SQL migrations..."
rm -rf main/migrations

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running SQLite migrations (Sessions only)..."
python manage.py migrate