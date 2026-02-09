#!/bin/sh

set -e

echo "Running migrations..."
python manage.py migrate || echo "Migration failed"
echo "Migration is completed!"

echo "Starting collectstatic..."
python manage.py collectstatic --noinput
echo "Collectstatic is completed!"

exec gunicorn django_server.wsgi:application --bind 0.0.0.0:8000
