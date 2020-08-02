#!/bin/bash

set -euo pipefail

SQL_HOST=${SQL_HOST:-db}
SQL_PORT=${SQL_PORT:-5432}

echo "Waiting for database"
scripts/wait-for-it.sh $SQL_HOST:$SQL_PORT

echo "Running migrations"
python manage.py migrate

python manage.py runserver
