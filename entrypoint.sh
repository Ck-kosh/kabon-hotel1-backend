#!/usr/bin/env sh
set -eu

python manage.py migrate --no-input
python manage.py collectstatic --no-input
exec gunicorn kabon_hotel.wsgi:application --bind 0.0.0.0:"${PORT:-8000}"