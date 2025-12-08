#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Removing conflicting SQL migrations..."
# We remove this folder because it contains SQL migrations that conflict
# with your MongoDB setup and cause errors during the migrate command.
rm -rf main/migrations

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running standard Django migrations (Sessions/Auth)..."
# We still need this for Django's internal session management (stored in SQLite/SQL)
python manage.py migrate