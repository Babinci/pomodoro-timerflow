#!/bin/bash

CONTAINER_NAME="pomodoro-app-container"

# Check if container is running
if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Container $CONTAINER_NAME is not running. Start it first."
    exit 1
fi

if [ "$1" = "makemigrations" ]; then
    if [ -z "$2" ]; then
        echo "Error: Migration message is required"
        echo "Usage: $0 makemigrations \"your migration message\""
        exit 1
    fi
    docker exec -it $CONTAINER_NAME python /app/app/manage_db.py makemigrations "$2"
elif [ "$1" = "migrate" ]; then
    docker exec -it $CONTAINER_NAME python /app/app/manage_db.py migrate
elif [ "$1" = "showmigrations" ]; then
    docker exec -it $CONTAINER_NAME python /app/app/manage_db.py showmigrations
else
    echo "Usage: $0 [makemigrations \"message\"|migrate|showmigrations]"
    exit 1
fi