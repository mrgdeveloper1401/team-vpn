#!/bin/sh

#python manage.py check_database
gunicorn dj_vpn.vpn.wsgi -b 0.0.0.0:8000