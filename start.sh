#!/bin/bash
export PATH=/usr/local/bin/:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin:
fuser -k 7000/tcp
python3 manage.py collectstatic --noinput
gunicorn3 --daemon --env DJANGO_SETTINGS_MODULE=Project.settings Project.wsgi -b 0:7000 --workers 8 --log-level debug --max-requests 0 --timeout 1800 --keep-alive 1800 --reload &
