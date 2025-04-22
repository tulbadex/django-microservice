#!/bin/bash
set -e

# Wait for the database to be ready
# if [ "$DB_ENGINE" = "postgres" ]; then
#     echo "Waiting for PostgreSQL..."
#     while ! nc -z $DB_HOST $DB_PORT; do
#         sleep 0.1
#     done
#     echo "PostgreSQL started"
# fi

# Apply database migrations
echo "Applying database migrations..."
# python manage.py makemigrations
python manage.py migrate

# Create log directory
mkdir -p /app/logs

# Start the application
echo "Starting application..."

# Execute the command passed to the script
exec "$@"