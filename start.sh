#!/bin/bash
set -e

# run migrations
/app/wait-for-it.sh $POSTGRES_HOST -- alembic upgrade head

# start app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
