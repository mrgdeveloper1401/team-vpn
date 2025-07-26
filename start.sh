#!/bin/sh

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn dj_vpn.vpn.wsgi -b 0.0.0.0:8000 -w 4