#!/bin/sh

echo "Waiting for Postgis .."

while ! nc -z postgis 5432; do
    sleep 0.1
done

echo "Postgis started."

python manage.py run -h 0.0.0.0