#!/bin/sh

echo "apply database make-migrations"
python manage.py makemigrations --noinput

echo "apply database migrate"
python manage.py migrate --noinput

echo "apply collect-static"
python manage.py collectstatic --noinput

exec "$@"
