#!/bin/bash
set -e

host="db"
user="user"
dbname="task_manager"

echo "Waiting for PostgreSQL at $host..."

until pg_isready -h "$host" -U "$user" -d "$dbname"; do
  sleep 2
done

echo "PostgreSQL is up. Starting application..."
exec "$@"
