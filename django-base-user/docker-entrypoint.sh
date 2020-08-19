#!/bin/sh
python manage.py migrate

python manage.py collectstatic --no-input

gunicorn --workers=2 core.wsgi -b 0.0.0.0:8000 --reload --error-logfile '/django_base_user/log/gunicorn-error.log'
