#!/bin/bash
if [ $1 == "uwsgi" ]; then
        shift
        /usr/bin/uwsgi --uid www-data --gid www-data --plugins=python3 --chdir=/var/www --socket=0.0.0.0:8000 $@
elif [ $1 == "worker" ]; then
    shift
    celery $@
elif [ $1 == "bash" ]; then
        bash
fi
