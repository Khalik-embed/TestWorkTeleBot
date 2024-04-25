#!/bin/bash

# Ожидание, пока Postgres полностью запустится
while !</dev/tcp/db/5432; do
  sleep 1
done

# Затем запускаем миграции и сервер Django
python bot_admin/manage.py migrate
python bot_admin/manage.py runserver 0.0.0.0:8001