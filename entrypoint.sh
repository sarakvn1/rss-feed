#!/bin/bash
if [ $1 == "uwsgi" ]; then
        shift
        python3 /var/www/manage.py collectstatic --noinput
        python3 /var/www/manage.py migrate --check
        /usr/bin/uwsgi --uid www-data --gid www-data --plugins=python3 --chdir=/var/www --socket=0.0.0.0:8000 $@
elif [ $1 == "worker" ]; then
    shift
    celery $@
elif [ $1 == "bash" ]; then
        bash
fi
