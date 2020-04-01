#!/bin/bash

WAITED_HOST="psql"
WAITED_PORT="5432"
LOG_LEVEL="info"
LOG_FILE="/var/logs/web/gunicorn.log"

cd /app/

# waiting up postgresql server
while [ $(timeout 2 bash -c "</dev/tcp/$WAITED_HOST/$WAITED_PORT" &>/dev/null 2>&1 ; echo $?) != 0 ]; do
    echo "Host '$WAITED_HOST' not started, waiting..."
    sleep 2
done

if [[ ! -e /migrated.tmp ]]; then
   echo "Migrating the database before starting the server"
   python manage.py makemigrations
   python manage.py migrate
   echo yes | python manage.py collectstatic

   if [[ $? -eq  0 ]]; then
       touch /migrated.tmp
   else
       exit
   fi
fi

# update database configuration
python run_server.py

# Start processes
gunicorn config.wsgi:application --reload --workers 3 --log-level $LOG_LEVEL --log-file $LOG_FILE --bind 0.0.0.0:8000
