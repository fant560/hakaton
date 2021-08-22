#!/bin/sh
sleep 15
python manage.py makemigrations --noinput || exit 1
python manage.py migrate --noinput || exit 1
python manage.py runserver 0.0.0.0:8000 || exit 1
