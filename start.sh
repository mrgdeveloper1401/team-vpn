#!/bin/sh

#python manage.py check_database
#python manage.py collectstatic --noinput
gunicorn dj_vpn.vpn.wsgi -b 0.0.0.0:8000