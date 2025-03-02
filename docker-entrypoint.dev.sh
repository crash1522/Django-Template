#!/bin/bash

# 데이터베이스 연결 대기
until PGPASSWORD=$DB_PASSWORD psql -h "db" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# 데이터베이스 마이그레이션
python manage.py migrate

# Django 개발 서버 실행 (디버그 모드)
python manage.py runserver 0.0.0.0:8000 